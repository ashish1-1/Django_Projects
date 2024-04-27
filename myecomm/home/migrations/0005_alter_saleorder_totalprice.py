# Generated by Django 5.0.2 on 2024-04-14 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_orderlines_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleorder',
            name='totalPrice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True),
        ),
    ]
