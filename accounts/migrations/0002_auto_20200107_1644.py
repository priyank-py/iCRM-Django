# Generated by Django 2.2.7 on 2020-01-07 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('leads', '0001_initial'),
        ('employees', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead_invoice', to='leads.Lead', verbose_name='Lead'),
        ),
        migrations.AddField(
            model_name='installmentdata',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Invoice', verbose_name=''),
        ),
        migrations.AddField(
            model_name='clientinvoice',
            name='counselor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.Employee', verbose_name='BDE Name'),
        ),
        migrations.AddField(
            model_name='clientinvoice',
            name='lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.CorporateAndInstitutionLead', verbose_name='Client'),
        ),
        migrations.AddField(
            model_name='clientinstallmentdata',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.ClientInvoice', verbose_name=''),
        ),
        migrations.AddField(
            model_name='clientbill',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.ClientInvoice', verbose_name=''),
        ),
        migrations.AddField(
            model_name='bill',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='source_invoice', to='accounts.Invoice'),
        ),
    ]
