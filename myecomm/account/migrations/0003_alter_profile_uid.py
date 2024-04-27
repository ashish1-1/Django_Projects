# Generated by Django 5.0.2 on 2024-04-09 16:54

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_profile_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='uid',
            field=models.UUIDField(default=uuid.UUID('55a18ac0-f68c-46ee-897e-f4306f81c146'), editable=False, primary_key=True, serialize=False),
        ),
    ]
