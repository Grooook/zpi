# Generated by Django 4.1.1 on 2022-12-18 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.PositiveIntegerField(blank=True, null=True, unique=True)),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30)),
                ('birth_date', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('is_student', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('is_vice_dean', models.BooleanField(default=False)),
                ('is_dean', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expired', models.DateField(blank=True, null=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('accepted_by', models.CharField(choices=[('s', 'Staff'), ('t', 'Teacher'), ('vd', 'Vice-dean'), ('d', 'Dean')], default='d', max_length=2)),
                ('file', models.FileField(upload_to='documents/')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=127)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('property_type', models.CharField(max_length=127)),
                ('max_length', models.PositiveSmallIntegerField()),
                ('required', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('c', 'Created'), ('p', 'Pending'), ('a', 'Accepted'), ('r', 'Rejected'), ('d', 'Deleted')], default='c', max_length=10)),
                ('file', models.FileField(null=True, upload_to='documents/processed/')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.application')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserApplicationProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveSmallIntegerField()),
                ('value', models.TextField(blank=True, max_length=1024, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('editable', models.BooleanField(default=False)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.property')),
                ('user_application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userapplication')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.application')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.property')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=32)),
                ('new_status', models.CharField(max_length=32)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userapplication')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.application')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.department')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.department'),
        ),
    ]
