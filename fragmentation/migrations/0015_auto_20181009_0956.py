# Generated by Django 2.1.2 on 2018-10-09 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_array1dmodel_array2dmodel'),
        ('fragmentation', '0014_auto_20181009_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='fragsample',
            name='cosine_matrix',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cosine_matrix', to='base.Array2DModel'),
        ),
        migrations.AddField(
            model_name='fragsample',
            name='mass_delta_double',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mass_delta_double', to='base.Array1DModel'),
        ),
        migrations.AddField(
            model_name='fragsample',
            name='mass_delta_single',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mass_delta_single', to='base.Array1DModel'),
        ),
    ]
