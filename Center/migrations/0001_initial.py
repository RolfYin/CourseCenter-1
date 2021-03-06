# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 06:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'managed': False,
                'db_table': 'auth_group',
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
                'db_table': 'auth_group_permissions',
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'managed': False,
                'db_table': 'auth_permission',
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=30, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'managed': False,
                'db_table': 'auth_user',
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
                'db_table': 'auth_user_groups',
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
                'db_table': 'auth_user_user_permissions',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('cid', models.IntegerField(db_column='cID', primary_key=True, serialize=False)),
                ('cname', models.CharField(db_column='cName', max_length=45)),
                ('descripition', models.CharField(blank=True, db_column='Descripition', max_length=200, null=True)),
                ('location', models.CharField(blank=True, db_column='Location', max_length=45, null=True)),
                ('startday', models.DateField(db_column='StartDay')),
                ('endday', models.DateField(db_column='EndDay')),
                ('isteam', models.CharField(db_column='IsTeam', max_length=1)),
            ],
            options={
                'managed': False,
                'db_table': 'course',
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'managed': False,
                'db_table': 'django_admin_log',
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'managed': False,
                'db_table': 'django_content_type',
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'managed': False,
                'db_table': 'django_migrations',
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'managed': False,
                'db_table': 'django_session',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(db_column='Index')),
                ('filename', models.CharField(db_column='FileName', max_length=45)),
                ('filepath', models.CharField(db_column='FilePath', max_length=200)),
                ('category', models.CharField(db_column='Category', max_length=45)),
            ],
            options={
                'managed': False,
                'db_table': 'resource',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('sid', models.IntegerField(db_column='sID', primary_key=True, serialize=False)),
                ('sname', models.CharField(db_column='sName', max_length=45)),
                ('ssex', models.CharField(db_column='sSex', max_length=1)),
                ('spassword', models.CharField(db_column='sPassword', max_length=45)),
            ],
            options={
                'managed': False,
                'db_table': 'student',
            },
        ),
        migrations.CreateModel(
            name='Studentcourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
                'db_table': 'studentcourse',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(db_column='Index')),
                ('request', models.CharField(blank=True, db_column='Request', max_length=300, null=True)),
                ('release', models.DateTimeField(db_column='Release')),
                ('deadline', models.DateTimeField(db_column='Deadline')),
                ('attachment', models.CharField(blank=True, db_column='Attachment', max_length=200, null=True)),
                ('maxgrade', models.FloatField(db_column='MaxGrade')),
            ],
            options={
                'managed': False,
                'db_table': 'task',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('tid', models.IntegerField(db_column='tID', primary_key=True, serialize=False)),
                ('tname', models.CharField(db_column='tName', max_length=45)),
                ('tsex', models.CharField(db_column='tSex', max_length=1)),
                ('tpassword', models.CharField(db_column='tPassword', max_length=45)),
            ],
            options={
                'managed': False,
                'db_table': 'teacher',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('teamid', models.IntegerField(db_column='teamID', primary_key=True, serialize=False)),
                ('teamname', models.CharField(db_column='teamName', max_length=45)),
                ('descripition', models.CharField(blank=True, db_column='Descripition', max_length=200, null=True)),
                ('maxnumber', models.IntegerField(db_column='maxNumber')),
            ],
            options={
                'managed': False,
                'db_table': 'team',
            },
        ),
        migrations.CreateModel(
            name='Teamapply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accept', models.CharField(db_column='Accept', max_length=1)),
            ],
            options={
                'managed': False,
                'db_table': 'teamapply',
            },
        ),
        migrations.CreateModel(
            name='Teamcourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
                'db_table': 'teamcourse',
            },
        ),
        migrations.CreateModel(
            name='Teamjoin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
                'db_table': 'teamjoin',
            },
        ),
        migrations.CreateModel(
            name='Teamsubmit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submittime', models.DateTimeField(db_column='SubmitTime')),
                ('filepath', models.CharField(db_column='FilePath', max_length=200)),
                ('grade', models.FloatField(blank=True, db_column='Grade', null=True)),
                ('comment', models.CharField(blank=True, db_column='Comment', max_length=200, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'teamsubmit',
            },
        ),
        migrations.CreateModel(
            name='Worksubmit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filepath', models.CharField(db_column='FilePath', max_length=200)),
                ('submittime', models.DateTimeField(db_column='SubmitTime')),
                ('grade', models.FloatField(blank=True, db_column='Grade', null=True)),
                ('comment', models.CharField(blank=True, db_column='Comment', max_length=200, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'worksubmit',
            },
        ),
    ]
