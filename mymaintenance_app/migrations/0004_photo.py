# Generated by Django 3.1.6 on 2021-04-18 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mymaintenance_app', '0003_auto_20210416_2319'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('work_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mymaintenance_app.workorder')),
            ],
        ),
    ]
