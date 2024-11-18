from django.core.mail import send_mail

def email():
        send_mail(
            'Test Email',
            'This is a test email.',
            'info@elitenest.co',
            ['zahidhsn760@gmail.com'],
            fail_silently=False,
        )
        return("email sent")


email()
