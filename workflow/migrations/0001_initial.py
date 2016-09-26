# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import workflow.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.CharField(default=workflow.models.generate_random_order_id_with_full_datetime_prefix, max_length=26, serialize=False, editable=False, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderVM',
            fields=[
                ('id', models.CharField(default=workflow.models.generate_random_vm_id_with_full_datetime_prefix, max_length=23, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=16)),
                ('sockets', models.IntegerField()),
                ('cpus_per_socket', models.IntegerField()),
                ('memory_GB', models.IntegerField()),
                ('nics', models.CharField(max_length=1024)),
                ('order', models.ForeignKey(related_name='VMs', to='workflow.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.CharField(default=workflow.models.generate_uuid_hex, max_length=36, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('owner', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ordervm',
            name='project',
            field=models.ForeignKey(editable=False, to='workflow.Project'),
        ),
        migrations.AddField(
            model_name='order',
            name='project',
            field=models.ForeignKey(to='workflow.Project'),
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('owner', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='ordervm',
            unique_together=set([('project', 'name')]),
        ),
    ]
