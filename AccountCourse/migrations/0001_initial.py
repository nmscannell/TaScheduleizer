# Generated by Django 2.1.7 on 2019-05-08 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.Account')),
                ('Course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.Course')),
            ],
        ),
    ]
