# Generated by Django 5.1.1 on 2024-10-21 14:28

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgreementSignature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature_image', models.ImageField(upload_to='signature1/')),
                ('is_signed', models.BooleanField(default=False)),
                ('signed_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_Name', models.CharField(max_length=50)),
                ('Last_Name', models.CharField(max_length=50)),
                ('Email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('Address', models.CharField(max_length=100000)),
                ('city_state_zip', models.CharField(max_length=100000)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CustomAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='products/')),
                ('section', models.CharField(choices=[('Floor', 'Floor'), ('Roof', 'Roof'), ('Extra_50mm_Glass_wool_Floor', 'Extra_50mm_Glass_wool_Floor'), ('Veranda', 'Veranda')], max_length=50)),
                ('subsection', models.CharField(blank=True, max_length=50)),
                ('size', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature_text', models.CharField(blank=True, max_length=255, null=True)),
                ('signature_image', models.ImageField(blank=True, null=True, upload_to='signatures/')),
                ('signed_date', models.DateTimeField(auto_now_add=True)),
                ('is_signed', models.BooleanField(default=False)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
            ],
        ),
        migrations.CreateModel(
            name='ClientReq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.JSONField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_requested', models.DateTimeField(default=django.utils.timezone.now)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(max_length=100)),
                ('region', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_code', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=100)),
                ('deliveryPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('Floor_code', models.TextField(blank=True, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.client')),
            ],
        ),
    ]
