# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-25 20:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dynamic_scraper', '0026_auto_20181125_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_number', models.CharField(max_length=500)),
                ('address1', models.CharField(max_length=100)),
                ('address2', models.CharField(blank=True, max_length=100)),
                ('unit_number', models.CharField(blank=True, max_length=500)),
                ('city', models.CharField(max_length=250)),
                ('state', models.CharField(max_length=250)),
                ('country', models.CharField(max_length=250)),
                ('zipcode', models.CharField(max_length=50)),
                ('note', models.TextField(blank=True)),
                ('checker_runtime', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dynamic_scraper.SchedulerRuntime')),
            ],
        ),
        migrations.CreateModel(
            name='AddressUnitList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='AddressWebsite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('scraper', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dynamic_scraper.Scraper')),
                ('scraper_runtime', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dynamic_scraper.SchedulerRuntime')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address_manager.AddressWebsite'),
        ),
        migrations.AddField(
            model_name='address',
            name='unit_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address_manager.AddressUnitList'),
        ),
    ]
