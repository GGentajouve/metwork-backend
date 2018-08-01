# Generated by Django 2.0.7 on 2018-07-30 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fragmentation', '0002_auto_20180625_1414'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fragannotation',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='fragannotationcompare',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='fragannotationdb',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='fragmol',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='fragmolsample',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='fragmolsim',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterField(
            model_name='fragannotationdb',
            name='db_id',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='fragannotationdb',
            name='db_source',
            field=models.CharField(default='unkown', max_length=64),
        ),
        migrations.AlterField(
            model_name='fragannotationdb',
            name='name',
            field=models.CharField(default='', max_length=64),
        ),
    ]