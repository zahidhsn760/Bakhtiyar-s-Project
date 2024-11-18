
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Client, ClientReq, Product,DeliveryAddress,Agreement,CustomAdmin,AgreementSignature
from django.shortcuts import get_object_or_404
from decimal import Decimal
import json
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.hashers import make_password,check_password
from django.utils.safestring import mark_safe
import json
from django.utils.datastructures import MultiValueDictKeyError

from django.db.models import F, Exists, OuterRef
from .decorators import admin_login_required
def register_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Basic validation
        if not username or not email or not password or not confirm_password:
            messages.error(request, 'All fields are required.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif CustomAdmin.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif CustomAdmin.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            admin_user = CustomAdmin(username=username, email=email)
            admin_user.password = make_password(password)
            admin_user.save()
            messages.success(request, 'Admin registered successfully.')
            return redirect('admin_login')

    return render(request, 'register_admin.html')

def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            admin_user = CustomAdmin.objects.get(username=username)
            # Check if the provided password matches the stored hashed password
            if check_password(password, admin_user.password) and admin_user.is_active:
                request.session['admin_user_id'] = admin_user.id
                messages.success(request, 'Logged in successfully.')
                return redirect('view_client_requests')
            else:
                messages.error(request, 'Invalid username or password.')
        except CustomAdmin.DoesNotExist:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login_admin.html')

def logout_admin(request):
    if 'admin_user_id' in request.session:
        del request.session['admin_user_id']
        messages.success(request, 'Logged out successfully.')
    return redirect('admin_login')
# Create your views here.
# def first_page(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('First_Name')
#         last_name = request.POST.get('Last_Name')
#         email = request.POST.get('Email')
#         phone_number = request.POST.get('phone_number')
#         address = request.POST.get('Address')
#         city_state_zip = request.POST.get('city-state-zip')
#         message = request.POST.get('message')
        
#         # Save the data to the model
#         client = Client(
#             First_Name=first_name,
#             Last_Name=last_name,
#             Email=email,
#             phone_number=phone_number,
#             Address=address,
#             message=message,
#             city_state_zip=city_state_zip
#         )
#         client.save()
#         # Redirect to the product selection page with client_id
#         return redirect('second_page', client_id=client.id)
    
#     return render(request, 'first_page.html')
def second_page(request):
    
    if request.method == 'POST':

      
        
        # Create a new client with personal information from the form
        client = Client.objects.create(
            First_Name=request.POST.get('first_name'),
            Last_Name=request.POST.get('last_name'),
            Email=request.POST.get('email'),
            phone_number=request.POST.get('phone_number'),
            # Address=request.POST.get('Address'),
            # city_state_zip=f"{request.POST.get('city')}, {request.POST.get('region')} {request.POST.get('postal_code')}"
        )

        # Get selected product IDs from each section
        selected_floor = request.POST.get('selected_floor')
        selected_roof = request.POST.get('selected_roof')
        selected_glass = request.POST.get('selected_glass')
        selected_veranda = request.POST.get('selected_veranda')

        # Get quantities for each product
        quantities = {key: request.POST.get(key) for key in request.POST.keys() if key.startswith('quantities_')}
        
        # client = Client.objects.get(id=client_id)

        products = []
        total_price = Decimal(0)

        # Function to process selected product
        def process_selected_product(product_id, quantity_key):
            product = Product.objects.get(id=product_id)
            quantity = int(quantities.get(quantity_key, 1))
           # product_total_price = Decimal(product.price) * Decimal(quantity)
            product_total_price = Decimal(product.price)
            return product, quantity, product_total_price

        # Process floor product
        if selected_floor:
            product, floor_quantity, product_total_price = process_selected_product(selected_floor, f'quantities_{selected_floor}')
            total_price += product_total_price
            products.append({
                'id': product.id,
                'name': product.name,
                'quantity': floor_quantity,
                'price': float(product_total_price)
            })

        # Process roof product
        if selected_roof:
            product, quantity, product_total_price = process_selected_product(selected_roof, f'quantities_{selected_roof}')
            total_price += product_total_price
            products.append({
                'id': product.id,
                'name': product.name,
                'quantity': floor_quantity,
                'price': float(product_total_price)
            })

        # Process glass product
        if selected_glass:
            product, quantity, product_total_price = process_selected_product(selected_glass, f'quantities_{selected_glass}')
            total_price += product_total_price
            products.append({
                'id': product.id,
                'name': product.name,
                'quantity': floor_quantity,
                'price': float(product_total_price)
            })

        # Process veranda product
        if selected_veranda:
            product, quantity, product_total_price = process_selected_product(selected_veranda, f'quantities_{selected_veranda}')
            total_price += product_total_price
            products.append({
                'id': product.id,
                'name': product.name,
                'quantity': floor_quantity,
                'price': float(product_total_price)
            })
        
        # Store the client request
        ClientReq.objects.create(
            client=client,
            products=products,
            total_price=float(total_price)
        )

        # Save delivery address
        DeliveryAddress.objects.create(
            client=client,
            # address_line_1=request.POST.get('address'),
            city=request.POST.get('city'),
            # postal_code=request.POST.get('postal-code'),
            country = request.POST.get('state_name'),
            deliveryPrice=Decimal(request.POST.get('state')),
    
            additional_info=request.POST.get('delivery-info'),
            quantity=floor_quantity,
            totaldeliveryPrice=Decimal(request.POST.get('state')) * Decimal(floor_quantity),
        )

        return redirect('marble',client_id=client.id)

    else:
        # Fetch all products in a single query to optimize the DB hits
        all_products = Product.objects.all()

        # Group the products by section and subsection
        products_by_section = {
            'Floor': {
                '20ft': all_products.filter(section='Floor', subsection='20ft'),
                '30ft': all_products.filter(section='Floor', subsection='30ft'),
                '40ft': all_products.filter(section='Floor', subsection='40ft')
            },
            'Roof': {
                'Standard Roof': all_products.filter(section='Roof', subsection='Standard Roof'),
                'Upgraded Roof': all_products.filter(section='Roof', subsection='Upgraded Roof')
            },
            'Extra_50mm_Glass_wool_Floor': {
                '20ft': all_products.filter(section='Extra_50mm_Glass_wool_Floor', subsection='20ft'),
                '30ft': all_products.filter(section='Extra_50mm_Glass_wool_Floor', subsection='30ft'),
                '40ft': all_products.filter(section='Extra_50mm_Glass_wool_Floor', subsection='40ft')
            },
            'Veranda': all_products.filter(section='Veranda'),

        }
              # Provide quantity range
        quantity_range = range(1, 11)

        # Debugging: Print products_by_section to check structure
        #print(products_by_section)

        return render(request, 'second_page.html', {
            'products_by_section': products_by_section,
            # 'client_id': client_id,
            'quantity_range': quantity_range,
        })
STATES = [
    "Alabama", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
    "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
    "Washington", "West Virginia", "Wisconsin", "Wyoming"
]
@admin_login_required
def view_client_requests(request):
    clients = Client.objects.annotate(
        latest_request_date=F('clientreq__date_requested'),
        is_signed=Exists(
            Agreement.objects.filter(client_id=OuterRef('id'), is_signed=True)
        )
    ).order_by('-latest_request_date')

    # Optional: Filtering by date
    date_filter = request.GET.get('date')
    if date_filter:
        clients = clients.filter(clientreq__date_requested__date=date_filter)
     # Filter by state name if provided
    state_filter = request.GET.get('state')
    if state_filter:
        clients = clients.filter(deliveryaddress__country=state_filter)

    return render(request, 'admin.html', {'clients': clients, 'states': STATES})


def get_product_details(client):
    client_requests = ClientReq.objects.filter(client=client)
    product_details = []

    for req in client_requests:
        for product in req.products:  # Assuming req.products is a list of dictionaries
            total = product['price'] * product['quantity']
            product_details.append({
                'name': product['name'],
                'price': product['price'],
                'quantity': product['quantity'],
                'total': total
            })
    
    return product_details

from django.db.models import Sum
@admin_login_required
def client_details(request, client_id):
    # Retrieve the specific client
    
    client = get_object_or_404(Client, id=client_id)
    client_requests = ClientReq.objects.filter(client=client)

    # Get the first delivery address related to the client, if it exists
    delivery_address = DeliveryAddress.objects.filter(client=client).first()
    #print(delivery_address.deliveryPrice)
    # Prepare product details
    product_details = []
    for req in client_requests:
        for product in req.products:  # Assuming req.products is a list of dictionaries
            total = product['price'] * product['quantity']
           
            
            product_details.append({
                'name': product['name'],
                'price': product['price'],
                'quantity': product['quantity'],
                'total': total
            })
    
    # Convert deliveryPrice to float before adding
    # delivery_price_float = float(delivery_address.deliveryPrice)
    if delivery_address and delivery_address.totaldeliveryPrice is not None:
        try:
            delivery_price_float = float(delivery_address.totaldeliveryPrice)
        except ValueError:
            # Handle the case where deliveryPrice is not a valid float
            delivery_price_float = 0.0
    else:
        delivery_price_float = 0.0 
    # Calculate the total sum of all products
    total_sum = sum([product['total'] for product in product_details]) + delivery_price_float

    return render(request, 'client_detail.html', {
        'client': client,
        'client_requests': client_requests,
        'delivery_address': delivery_address,
        'product_details': product_details,
        'total_sum': total_sum,
    })
@admin_login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        client.delete()
        return redirect('view_client_requests')# Redirect to the list of products after deletion
@admin_login_required
def add_product(request):
    sections = Product.SECTIONS  # Use the SECTIONS constant from the model
    subsections = Product.SUBSECTIONS  # Use the SUBSECTIONS constant from the model

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        section = request.POST.get('section')
        size = request.POST.get('size')  # Fetch the size if provided

        try:
            image = request.FILES['image']
        except MultiValueDictKeyError:
            image = None

        # Ensure required fields are filled
        if name and price and image and description and section:
            product = Product(
                name=name,
                description=description,
                price=price,
                image=image,
                section=section
            )

            # Only assign size if section is "Roof"
            if section == "Roof" and size:
                product.size = size

            # Only assign subsection if section is not "Veranda"
            if section != "Veranda":
                subsection = request.POST.get('subsection')
                if subsection:
                    product.subsection = subsection

            product.save()

            return redirect('product_list')  # Redirect to a page that shows the list of products
        else:
            error_message = 'All fields are required.'
            return render(request, 'add_product.html', {
                'error': error_message,
                'sections': sections,
                'subsections': mark_safe(json.dumps(subsections)),  # Serialize subsections as JSON
            })

    return render(request, 'add_Product.html', {
        'sections': sections,
        'subsections': mark_safe(json.dumps(subsections)),  # Serialize subsections as JSON
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import mark_safe
from .models import Product  # Ensure the correct import of the Product model

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
@admin_login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    sections = Product.SECTIONS
    subsections = Product.SUBSECTIONS
    
    subsections_json = mark_safe(json.dumps(subsections))

    if request.method == 'POST':
        # Gather form data
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        section = request.POST.get('section')
        size = request.POST.get('size')
        
        # Check if an image is uploaded
        if 'image' in request.FILES:
            product.image = request.FILES['image']

        # Update product attributes
        product.name = name
        product.description = description
        product.price = price
        product.section = section

        # Assign size only if section is "Roof"
        if section == "Roof":
            product.size = size
        else:
            product.size = None

        # Assign subsection only if section is not "Veranda"
        if section != "Veranda":
            product.subsection = request.POST.get('subsection')
        else:
            product.subsection = None
        
        # Ensure required fields are filled
        if product.name and product.price and product.description and product.section:
            product.save()
            return redirect('product_list')
        else:
            error_message = 'All fields are required.'
            return render(request, 'edit_product.html', {
                'product': product,
                'sections': sections,
                'subsections': subsections_json,
                'error': error_message,
            })

    return render(request, 'edit_product.html', {
        'product': product,
        'sections': sections,
        'subsections': subsections_json,
    })
@admin_login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')  # Redirect to the list of products after deletion

@admin_login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})



# def send_email(request, client_id):
#     client = get_object_or_404(Client, id=client_id)
#     subject = 'Your Order Details'
#     message = f'Dear {client.First_Name} {client.Last_Name},\n\nThank you for your order! We will get back to you soon.\n\nBest regards,\nYour Company'
#     recipient_list = [client.Email]
#     print(recipient_list)
#     try:
#         send_mail(subject, message, 'info@elitenest.co', recipient_list)
#         messages.success(request, 'Email sent successfully!')
#     except Exception as e:
#         messages.error(request, f'Failed to send email: {str(e)}')
#         print(f'Failed to send email: {str(e)}')  # Log the error

#     return redirect('client_details', client_id=client_id)


def marble(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        selected_card_value = request.POST.get('selectCard')
        selected_card_value1 = request.POST.get('selectCard1')
        
        # Attempt to get the existing DeliveryAddress for this client
        delivery_address, created = DeliveryAddress.objects.get_or_create(client=client)
        
        # Optionally, you can use the 'created' flag if needed
        if created:
            print(f"Created new DeliveryAddress for client {client_id}")
        else:
            print(f"Updated existing DeliveryAddress for client {client_id}")
        
        # Update the existing record or create a new one if it doesn't exist
        delivery_address.Floor_code = f"{selected_card_value},{selected_card_value1}"
        delivery_address.save()
        
        # Return the redirect call
        return redirect('welcome', client_id=client_id)
    
    return render(request, 'Floor_Marbal.html', {'client': client})





def welcome(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    
    # Retrieve the latest ClientReq for the client (or the first one if sorting is not required)
    client_req = ClientReq.objects.filter(client=client).order_by('-date_requested').first()
    
    # Get the date from ClientReq or use the current date as a fallback
    request_date = client_req.date_requested if client_req else timezone.now()
    
    return render(request, 'wellcom-agreement.html', {
        'client': client,
        'request_date': request_date
    })

from django.urls import reverse
import logging
logger = logging.getLogger(__name__)
from urllib.parse import urlencode

def agreement(request, client_id):
    # Get the client by their ID
    client = get_object_or_404(Client, id=client_id)

    # Get the latest client request
    client_request = ClientReq.objects.filter(client=client).order_by('-date_requested').first()

    # Extract products and total price from the client request
    products = client_request.products if client_request else []
    total_price = client_request.total_price if client_request else 0
    delivery_address = DeliveryAddress.objects.filter(client=client).order_by('-id').first()

    # Get delivery charge from the delivery address (if available)
    delivery_charge = delivery_address.deliveryPrice if delivery_address and delivery_address.deliveryPrice else 0

    # Add delivery charge to the total price
    total_price += delivery_charge
 

    # Get or create the agreement instance for the client
    agreement, created = Agreement.objects.get_or_create(client=client)

    if request.method == 'POST':
        # Handle signature saving
        signature_text = request.POST.get('signature_text')
        signature_image = request.FILES.get('signature_image')

        if signature_text:
            agreement.signature_text = signature_text
        if signature_image:
            agreement.signature_image = signature_image

        agreement.is_signed = True
        agreement.signed_date = timezone.now()
        agreement.save()

        base_url = reverse('agreement', args=[client_id])

        params = {
            'token': 'secure_token_123',
            'ref': client.Email,
            'type': 'agreement',
        }

        # Construct the full URL with query parameters
        agreement_url = request.build_absolute_uri(f"{base_url}?{urlencode(params)}")

        # Render the email content from a template
        email_context = {
            'client_name': client.First_Name,
            'agreement_url': agreement_url,
        }
        html_content = render_to_string('email.html', email_context)
        text_content = strip_tags(html_content)

        try:
            # Log the email details
            logger.debug(f'Sending email to: {client.Email}')
            logger.debug('Subject: Your Quote and Agreement from Expanders')
            logger.debug(f'HTML Content: {html_content}')
            logger.debug(f'Text Content: {text_content}')

            # Send the email
            send_mail(
                subject='Confirmation of Your Signed Agreement with ELITE NEST',
                message=text_content,
                from_email='ELITE NEST <info@elitenest.co>',
                recipient_list=[client.Email],
                html_message=html_content,
                fail_silently=False,
            )

            logger.debug('Email sent successfully!')
            messages.success(request, 'Email sent successfully!')
        except Exception as e:
            logger.error(f'Failed to send email: {str(e)}')
            messages.error(request, f'Failed to send email: {str(e)}')

        return redirect('success')

    return render(request, 'agreement_page.html', {
        'client': client,
        'products': products,
        'total_price': total_price,
        'agreement': agreement,
        'delivery_charge': delivery_charge,
    })


def view_agreement(request, client_id):
    agreement = get_object_or_404(Agreement, client_id=client_id, is_signed=True)
    return render(request, 'agreement_page.html', {'agreement': agreement})
    
    
    
    
def success(request):
    
    return render(request, 'success.html')
    

from django.http import JsonResponse
from django.core.files.base import ContentFile
import base64
from django.core.cache import cache

@csrf_exempt
def special_client(request):
    cache.clear()
    if request.method == 'POST':
        logger.debug("POST request received")
        signature_image_data_url = request.POST.get('signature_image')
        if signature_image_data_url:
            logger.debug("Received signature image data URL")

            # Remove the prefix 'data:image/png;base64,' from the data URL
            if signature_image_data_url.startswith('data:image/png;base64,'):
                image_data = signature_image_data_url.split(',')[1]
                signature_image = ContentFile(base64.b64decode(image_data), name='signature.png')

                # Create a new signature instance
                signature = AgreementSignature.objects.create(signature_image=signature_image)
                signature.is_signed = True
                signature.signed_date = timezone.now()
                signature.save()
                logger.debug("Signature saved successfully")
                base_url = reverse('special_client')
                params = {
                    'token': 'secure_token_123',
                    'ref': 'schwenger@prodigy.net',  # Replace with dynamic email if needed
                    'type': 'agreement',
                }
                agreement_url = request.build_absolute_uri(f"{base_url}?{urlencode(params)}")
    
                # Render the email content
                email_context = {
                    'agreement_url': agreement_url,
                }
                html_content = render_to_string('email1.html', email_context)
                text_content = strip_tags(html_content)
    
                try:
                    send_mail(
                        subject='Confirmation of Your Signed Agreement with ELITE NEST',
                        message=text_content,
                        from_email='ELITE NEST <info@elitenest.co>',
                        recipient_list=['schwenger@prodigy.net','bakhtyarkhan848@gmail.com'],  # Ensure this is a list
                        html_message=html_content,
                        fail_silently=False,
                    )
                    messages.success(request, 'Email sent successfully!')
                except Exception as e:
                    messages.error(request, f'Failed to send email: {str(e)}')

                return redirect('success')
        #     else:
        #         logger.error("Invalid image data URL format.")
        #         return JsonResponse({'success': False, 'message': 'Invalid image data URL format.'})
        # else:
        #     logger.error("No signature image received.")
        #     return JsonResponse({'success': False, 'message': 'No signature image received.'})

    # Handling GET request to display the agreement
    signature = AgreementSignature.objects.first()  # Get the existing signature if it exists
    return render(request, 'client_agreement.html', {'signature': signature})