# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0006_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pubdate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
