# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_auto_20180612_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='books',
            field=models.ManyToManyField(related_name='store', to='hello.Book'),
        ),
    ]
