# Generated by Django 3.2 on 2021-04-12 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(choices=[('BANGALORE', 'Bangalore'), ('CHENNAI', 'Chennai'), ('DELHI', 'Delhi'), ('HYDERABAD', 'Hyderabad'), ('KOLKATA', 'Kolkata'), ('MUMBAI', 'Mumbai')], max_length=30)),
                ('state', models.CharField(max_length=30, null=True)),
                ('zipcode', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('cast', models.CharField(blank=True, max_length=100, null=True)),
                ('director', models.CharField(blank=True, max_length=50, null=True)),
                ('language', models.CharField(choices=[('ENGLISH', 'English'), ('BENGALI', 'Bengali'), ('HINDI', 'Hindi'), ('TAMIL', 'Tamil'), ('TELUGU', 'Telugu'), ('KANNADA', 'Kannada')], max_length=10)),
                ('run_length', models.IntegerField(blank=True, null=True)),
                ('certificate', models.CharField(choices=[('U', 'U'), ('UA', 'U/A'), ('A', 'A'), ('R', 'R')], max_length=2)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media')),
            ],
        ),
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Default Cinema', max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.city')),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_time', models.DateTimeField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('theater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.theater')),
            ],
        ),
    ]