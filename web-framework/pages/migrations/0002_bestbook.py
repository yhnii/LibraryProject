# Generated by Django 2.1.7 on 2019-02-21 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bestbook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('gender', models.IntegerField()),
                ('ranking', models.IntegerField()),
                ('bCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.Book')),
            ],
        ),
    ]
