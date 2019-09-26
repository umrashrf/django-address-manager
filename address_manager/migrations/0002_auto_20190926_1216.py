# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-26 16:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='unit_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address_manager.AddressUnitList'),
        ),
    ]