# Generated by Django 4.1.2 on 2022-11-05 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_address_zip'),
    ]

    operations = [
        migrations.RunSQL(""" INSERT INTO store_collection(title)
                              VALUES('MasterCheif')
                           """,
                           
                          """
                          DELETE FROM store_collection
                          WHERE title = 'MasterCheif'
                          
                          """)
    ]
