# Generated by Django 3.2 on 2021-04-14 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_alter_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('SUCC', 'Success'), ('FAIL', 'Failed'), ('PROG', 'Progress'), ('NULL', 'Null')], default='NULL', max_length=20, null=True),
        ),
    ]
