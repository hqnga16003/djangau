# Generated by Django 4.2.11 on 2024-04-01 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_remove_course_category_remove_course_tags_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time', models.DurationField()),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Drivers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='category',
            name='active',
        ),
        migrations.CreateModel(
            name='Trips',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('departure_date', models.DateField()),
                ('departure_time', models.TimeField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='myapp.buses')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='myapp.drivers')),
            ],
            options={
                'unique_together': {('bus', 'departure_date', 'departure_time')},
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('customer_name', models.CharField(max_length=255)),
                ('quantity_ticket', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('booking_date', models.DateField()),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='myapp.trips')),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('customer_name', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('rating', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')])),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='myapp.trips')),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='buses',
            name='id_arrival_point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrival_routes', to='myapp.location'),
        ),
        migrations.AddField(
            model_name='buses',
            name='id_departure_point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure_routes', to='myapp.location'),
        ),
    ]
