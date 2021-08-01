# Generated by Django 3.2.4 on 2021-07-04 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('communications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_room', to='profiles.profile'),
        ),
        migrations.AddField(
            model_name='room',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_room', to='profiles.profile'),
        ),
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_messages', to='profiles.profile'),
        ),
        migrations.AddField(
            model_name='message',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_messages', to='profiles.profile'),
        ),
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='messages', to='communications.room'),
        ),
    ]
