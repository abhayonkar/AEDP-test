# Generated by Django 5.2.4 on 2025-07-18 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_alter_industry_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='curriculum_file',
            field=models.FileField(blank=True, null=True, upload_to='curricula/', verbose_name='Upload Curriculum'),
        ),
        migrations.AddField(
            model_name='program',
            name='degree',
            field=models.CharField(choices=[('B.Com', 'B.Com'), ('B.A.', 'B.A.'), ('B.Sc.', 'B.Sc.'), ('B.M.S.', 'B.M.S.'), ('B.Tech', 'B.Tech'), ('B.B.A.', 'B.B.A.'), ('M.Com.', 'M.Com.'), ('M.A.', 'M.A.'), ('M.Sc.', 'M.Sc.'), ('M.B.A', 'M.B.A'), ('M.Tech', 'M.Tech'), ('Others', 'Others')], default='', max_length=20, verbose_name='Degree'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='program',
            name='other_degree',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Other Degree (if selected Others)'),
        ),
        migrations.AddField(
            model_name='program',
            name='specialization',
            field=models.CharField(blank=True, max_length=200, verbose_name='Specialization/Branch'),
        ),
    ]
