# Generated by Django 4.2.11 on 2024-04-24 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_user_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_date', models.DateField()),
                ('departure_time', models.TimeField()),
                ('surcharge', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('arrival_date', models.DateField(blank=True, null=True)),
                ('arrival_time', models.TimeField(blank=True, null=True)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bus_schedules', to='myapp.bus')),
                ('bus_route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_schedules', to='myapp.busroute')),
            ],
            options={
                'unique_together': {('bus', 'departure_date', 'departure_time')},
            },
        ),
    ]