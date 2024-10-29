# Generated by Django 5.1.2 on 2024-10-28 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_remove_todo_delete'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='priority',
            field=models.CharField(choices=[('HIGH', 'High'), ('MEDIUM', 'Medium'), ('LOW', 'Low')], default='MEDIUM', max_length=10),
        ),
        migrations.AddField(
            model_name='todo',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed')], default='PENDING', max_length=20),
        ),
    ]
