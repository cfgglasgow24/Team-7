# Generated by Django 4.1.3 on 2023-03-07 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_customuser_how_you_found_us_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='how_you_found_us',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.how_did_you_meet_us'),
        ),
        migrations.AlterField(
            model_name='mentee',
            name='education',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.education'),
        ),
        migrations.AlterField(
            model_name='mentee',
            name='occupation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.occupation'),
        ),
    ]
