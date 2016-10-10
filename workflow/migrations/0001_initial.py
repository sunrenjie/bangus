# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import workflow.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('viewflow', '0005_rename_flowcls'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.CharField(primary_key=True, default=workflow.models.generate_random_order_id_with_full_datetime_prefix, max_length=26, editable=False, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('vms_verified', models.BooleanField(default=False)),
                ('vms_confirmed', models.BooleanField(default=False)),
                ('vms_deployed', models.BooleanField(default=False)),
                ('vms_software_installed', models.BooleanField(default=False)),
                ('security_fixed', models.BooleanField(default=False)),
                ('security_confirmed', models.BooleanField(default=False)),
                ('external_ip', models.CharField(max_length=1024)),
                ('external_ip_confirmed', models.BooleanField(default=False)),
                ('external_ip_deployed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderCompleteProjectProcess',
            fields=[
                ('process_ptr', models.OneToOneField(to='viewflow.Process', parent_link=True, primary_key=True, auto_created=True, serialize=False)),
                ('order', models.ForeignKey(blank=True, null=True, to='workflow.Order')),
            ],
            options={
                'permissions': [('can_start_order', 'Can initiate an order process'), ('can_amend_order', 'Can amend an order'), ('can_verify_order', 'Can verify that an order is technically possible'), ('can_confirm_order', 'Can confirm an order'), ('can_deploy_virtual_machines', 'Can deploy virtual machines'), ('can_install_vm_software', 'Can install software for the VMs'), ('can_fix_security_issues', 'Can fix security issues for the VMs'), ('can_confirm_security_status', 'Can confirm that the VMs are secure according to security scan'), ('can_request_external_ip', 'Can request external IP'), ('can_confirm_external_ip', 'Can confirm external IP'), ('can_deploy_external_ip', 'Can implemet external IP')],
                'verbose_name_plural': 'Order complete project process list',
            },
            bases=('viewflow.process',),
        ),
        migrations.CreateModel(
            name='OrderVM',
            fields=[
                ('id', models.CharField(primary_key=True, default=workflow.models.generate_random_vm_id_with_full_datetime_prefix, max_length=23, editable=False, serialize=False)),
                ('name', models.CharField(max_length=16)),
                ('sockets', models.IntegerField()),
                ('cpus_per_socket', models.IntegerField()),
                ('memory_GB', models.IntegerField()),
                ('disks', models.CharField(max_length=32)),
                ('nics', models.CharField(max_length=1024)),
                ('order', models.ForeignKey(related_name='VMs', to='workflow.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.CharField(primary_key=True, default=workflow.models.generate_uuid_hex, max_length=36, editable=False, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('owner', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BangusTask',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('viewflow.task',),
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
