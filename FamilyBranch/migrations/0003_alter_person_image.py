# Generated by Django 5.0 on 2023-12-28 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FamilyBranch', '0002_person_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/person_images/'),
        ),
    ]
