# Generated by Django 4.1.2 on 2023-02-07 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_alter_customer_options_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can cancel order')]},
        ),
    ]
