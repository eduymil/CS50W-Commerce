# Generated by Django 4.0.3 on 2022-04-04 07:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_listing_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
