# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-25 14:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metabolization', '0001_initial'),
        ('fragmentation', '0001_initial'),
        ('base', '0002_auto_20180625_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleannotationproject',
            name='frag_annotations_init',
            field=models.ManyToManyField(to='fragmentation.FragAnnotationDB'),
        ),
        migrations.AddField(
            model_name='sampleannotationproject',
            name='frag_compare_conf',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='fragmentation.FragCompareConf'),
        ),
        migrations.AddField(
            model_name='sampleannotationproject',
            name='frag_sample',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='fragmentation.FragSample'),
        ),
        migrations.AddField(
            model_name='sampleannotationproject',
            name='frag_sim_conf',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='fragmentation.FragSimConf'),
        ),
        migrations.AddField(
            model_name='sampleannotationproject',
            name='react_processes',
            field=models.ManyToManyField(to='metabolization.ReactProcess'),
        ),
        migrations.AddField(
            model_name='sampleannotationproject',
            name='reactions_conf',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='metabolization.ReactionsConf'),
        ),
    ]