# Generated by Django 4.1.2 on 2023-04-09 17:47

from django.db import migrations, models
import django.db.models.deletion
import store.validators


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='store/images', validators=[store.validators.validate_file_size]),
        ),
        migrations.CreateModel(
            name='CustomerImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='store/images')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='picture', to='store.customer')),
            ],
        ),
    ]
