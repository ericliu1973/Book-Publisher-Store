# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0009_auto_20180624_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='stock_number',
            field=models.IntegerField(default=0),
        ),
    ]
