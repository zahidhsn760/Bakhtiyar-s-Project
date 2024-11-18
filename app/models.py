from django.db import models
import json
# Create your models here.


# class admin(models.model):
#     Username=models.CharField( max_length=50)
#     Password=models.CharField(max_length=10)

from django.conf import settings

from django.contrib.auth.hashers import make_password,check_password

class CustomAdmin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Ensure passwords are hashed before saving
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(CustomAdmin, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
class Client(models.Model):
    First_Name= models.CharField(max_length=50)
    Last_Name=models.CharField(max_length=50)
    Email=models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=15)  # Adjust max_length as needed
    Address=models.CharField(max_length=100000)
    city_state_zip=models.CharField(max_length=100000)
    message = models.TextField()
    
    def get_delivery_address(self):
        return self.deliveryaddress_set.first() 
class Agreement(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    signature_text = models.CharField(max_length=255, blank=True, null=True)
    signature_image = models.ImageField(upload_to='signatures/', blank=True, null=True)
    signed_date = models.DateTimeField(auto_now_add=True)
    is_signed = models.BooleanField(default=False)

    def __str__(self):
        return f"Agreement for {self.client.First_Name} {self.client.Last_Name}"
from django.db import models

class Product(models.Model):
    SECTIONS = [
        ('Floor', 'Floor'),
        ('Roof', 'Roof'),
        ('Extra_50mm_Glass_wool_Floor', 'Extra_50mm_Glass_wool_Floor'),
        ('Veranda', 'Veranda'),
    ]

    SUBSECTIONS = {
        'Floor': [('20ft', '20ft'), ('30ft', '30ft'), ('40ft', '40ft')],
        'Roof': [('Standard Roof', 'Standard Roof'), ('Upgraded Roof', 'Upgraded Roof')],
        'Extra_50mm_Glass_wool_Floor':[('20ft', '20ft'), ('30ft', '30ft'), ('40ft', '40ft')],
        'Veranda': []
    }

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    section = models.CharField(max_length=50, choices=SECTIONS)
    subsection = models.CharField(max_length=50, blank=True)  # Subsection based on section
    size = models.CharField(max_length=50, blank=True, null=True)  # Size for Roof section

    def save(self, *args, **kwargs):
        # Ensure subsection matches the section chosen, unless the section is 'Veranda'
        if self.section != 'Veranda':  # Only check subsections for non-Veranda sections
            valid_subsections = dict(self.SUBSECTIONS).get(self.section, [])
            if self.subsection not in [sub[0] for sub in valid_subsections]:
                raise ValueError('Invalid subsection for the selected section')
        else:
            self.subsection = ''  # Clear subsection for Veranda

        # Set size only for the Roof section
        if self.section == 'Roof':
            if not self.size:
                raise ValueError('Size is required for Roof products')
        else:
            self.size = None  # Clear the size for other sections

        super(Product, self).save(*args, **kwargs)

from django.utils import timezone
class ClientReq(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
  

    products = models.JSONField()  # Store product details in JSON format
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_requested = models.DateTimeField(default=timezone.now)
    def save(self, *args, **kwargs):
        # Convert Decimal to float for JSON serialization
        self.products = [
            {**item, 'price': float(item['price'])} for item in self.products
        ]
        self.total_price = float(self.total_price)  # Convert Decimal to float
        super().save(*args, **kwargs)

class DeliveryAddress(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,  blank=True, null=True )
    # address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True, null=True)
    # postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    deliveryPrice=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    totaldeliveryPrice=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    additional_info = models.TextField(blank=True, null=True)
    Floor_code=models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.country}"
        
        
        
        
        

class AgreementSignature(models.Model):
    signature_image = models.ImageField(upload_to='signature1/')  # Store signature images
    is_signed = models.BooleanField(default=False)  # Field to indicate if the agreement is signed
    signed_date = models.DateTimeField(null=True, blank=True)  # Field to store the date of signing

    def __str__(self):
        return f"Agreement Signed on {self.date_signed}"