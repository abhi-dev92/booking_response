# Generated by Django 5.0.4 on 2025-04-15 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xml_manager', '0002_alter_xmlfile_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xmlfile',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
