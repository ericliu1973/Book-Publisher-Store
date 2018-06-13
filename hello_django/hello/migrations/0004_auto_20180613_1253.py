# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_auto_20180613_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='email',
            field=models.EmailField(max_length=254, default='xxx@xxx.com'),
        ),
        migrations.AddField(
            model_name='author',
            name='nation',
            field=models.CharField(max_length=50, default='ca'),
        ),
    ]
