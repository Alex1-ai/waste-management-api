# Generated by Django 4.2.5 on 2024-05-31 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trash',
            old_name='takeout_date',
            new_name='take_out_date',
        ),
    ]
