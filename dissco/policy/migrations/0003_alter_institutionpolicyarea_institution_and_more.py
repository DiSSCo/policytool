# Generated by Django 4.0.4 on 2022-06-13 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_institutionuser'),
        ('policy', '0002_alter_policycomponent_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institutionpolicyarea',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='policies', to='common.institution'),
        ),
        migrations.AlterField(
            model_name='institutionpolicycomponent',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='common.institution'),
        ),
        migrations.AlterField(
            model_name='institutionpolicycomponent',
            name='policy_component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institution_policy_components', to='policy.policycomponent'),
        ),
        migrations.AlterField(
            model_name='institutionpolicylanguage',
            name='institution_policy_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='languages', to='policy.institutionpolicyarea'),
        ),
        migrations.AlterField(
            model_name='institutionpolicyowner',
            name='institution_policy_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owners', to='policy.institutionpolicyarea'),
        ),
        migrations.AlterField(
            model_name='policycomponent',
            name='policy_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='policy.policyarea'),
        ),
        migrations.AlterField(
            model_name='policycomponentoption',
            name='policy_component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='policy.policycomponent'),
        ),
        migrations.AlterField(
            model_name='servicecomponent',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='policy.service'),
        ),
    ]
