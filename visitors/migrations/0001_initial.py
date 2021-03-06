# Generated by Django 3.0.2 on 2020-01-24 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=20)),
                ('user_agent', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('path', models.CharField(max_length=255)),
                ('host', models.CharField(max_length=255)),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visitors.Visitor')),
            ],
        ),
    ]
