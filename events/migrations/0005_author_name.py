# Generated by Django 2.1.5 on 2019-02-13 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_remove_author_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='name',
            field=models.CharField(default='default', max_length=120, verbose_name='Author Name'),
            preserve_default=False,
        ),
    ]
