# Generated by Django 3.2 on 2021-04-14 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_auto_20210414_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('SUCC', 'Success'), ('FAIL', 'Failed'), ('PROG', 'Progress'), ('NULL', 'Null')], default='Null', max_length=20, null=True),
        ),
    ]
