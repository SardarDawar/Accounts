# Generated by Django 2.2.4 on 2020-03-23 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webaccount', '0004_check'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client_Company_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=300)),
                ('CR', models.CharField(max_length=300)),
                ('location', models.CharField(max_length=300)),
                ('contact_number', models.CharField(max_length=300)),
                ('Number_of_branches', models.IntegerField()),
                ('Number_of_employees', models.IntegerField()),
                ('Services', models.CharField(choices=[('BookKeeping', 'BookKeeping'), ('VAT', 'VAT')], max_length=300)),
                ('QR_code', models.FileField(upload_to='')),
                ('new', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=False)),
                ('pending', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('disabled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Client_Personal_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=300)),
                ('Email', models.EmailField(max_length=300)),
                ('Phone_Number', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Required_Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=300)),
                ('file_type', models.CharField(choices=[('pdf', 'pdf'), ('docs', 'docs'), ('image', 'image')], max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription_Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Services', models.CharField(choices=[('BookKeeping', 'BookKeeping'), ('VAT', 'VAT')], max_length=300)),
                ('Number_of_subaccounts', models.IntegerField()),
                ('package_price', models.IntegerField()),
                ('Relationship_Manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Required_Documents', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webaccount.Required_Documents')),
            ],
        ),
        migrations.DeleteModel(
            name='check',
        ),
        migrations.AddField(
            model_name='client_company_info',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webaccount.Client_Personal_Info'),
        ),
        migrations.AddField(
            model_name='client_company_info',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webaccount.sector'),
        ),
    ]
