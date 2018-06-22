# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hello', '0005_auto_20180621_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('body', models.TextField()),
                ('pubdate', models.DateField(auto_now_add=True)),
                ('book', models.ForeignKey(related_name='comment', to='hello.Book')),
                ('person', models.ForeignKey(related_name='comment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('pubdate',),
            },
        ),
    ]
