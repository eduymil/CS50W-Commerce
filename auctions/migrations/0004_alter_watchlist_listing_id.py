# Generated by Django 4.0.3 on 2022-04-04 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_watchlist_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='listing_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='auctions.listing'),
        ),
    ]
