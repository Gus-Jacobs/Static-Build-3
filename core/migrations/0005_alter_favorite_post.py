# Generated by Django 4.2.3 on 2023-08-13 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_favorite_post_alter_favorite_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.post'),
        ),
    ]
