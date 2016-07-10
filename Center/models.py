# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Course(models.Model):
    cid = models.IntegerField(db_column='cID', primary_key=True)  # Field name made lowercase.
    cname = models.CharField(db_column='cName', max_length=45)  # Field name made lowercase.
    descripition = models.CharField(db_column='Descripition', max_length=200, blank=True,
                                    null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    startday = models.DateField(db_column='StartDay')  # Field name made lowercase.
    endday = models.DateField(db_column='EndDay')  # Field name made lowercase.
    teacherid = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='teacherID')  # Field name made lowercase.
    isteam = models.CharField(db_column='IsTeam', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'course'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Resource(models.Model):
    cid = models.ForeignKey(Course, models.DO_NOTHING, db_column='cID')  # Field name made lowercase.
    index = models.IntegerField(db_column='Index')  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=1024)  # Field name made lowercase.
    filepath = models.CharField(db_column='FilePath', max_length=2048)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'resource'
        unique_together = (('cid', 'index'),)


class Student(models.Model):
    sid = models.IntegerField(db_column='sID', primary_key=True)  # Field name made lowercase.
    sname = models.CharField(db_column='sName', max_length=45)  # Field name made lowercase.
    ssex = models.CharField(db_column='sSex', max_length=1)  # Field name made lowercase.
    spassword = models.CharField(db_column='sPassword', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'student'


class Studentcourse(models.Model):
    sid = models.ForeignKey(Student, models.DO_NOTHING, db_column='sID')  # Field name made lowercase.
    cid = models.ForeignKey(Course, models.DO_NOTHING, db_column='cID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'studentcourse'
        unique_together = (('sid', 'cid'),)


class Task(models.Model):
    cid = models.ForeignKey(Course, models.DO_NOTHING, db_column='cID', primary_key=True)  # Field name made lowercase.
    index = models.IntegerField(db_column='Index')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    request = models.CharField(db_column='Request', max_length=2048, blank=True,
                               null=True)  # Field name made lowercase.
    release = models.DateTimeField(db_column='Release')  # Field name made lowercase.
    deadline = models.DateTimeField(db_column='Deadline')  # Field name made lowercase.
    attachment = models.CharField(db_column='Attachment', max_length=2048, blank=True,
                                  null=True)  # Field name made lowercase.
    maxgrade = models.FloatField(db_column='MaxGrade')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'task'
        unique_together = (('cid', 'index'),)


class Teacher(models.Model):
    tid = models.IntegerField(db_column='tID', primary_key=True)  # Field name made lowercase.
    tname = models.CharField(db_column='tName', max_length=45)  # Field name made lowercase.
    tsex = models.CharField(db_column='tSex', max_length=1)  # Field name made lowercase.
    tpassword = models.CharField(db_column='tPassword', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'teacher'


class Team(models.Model):
    teamid = models.IntegerField(db_column='teamID', primary_key=True)  # Field name made lowercase.
    teamname = models.CharField(db_column='teamName', max_length=45)  # Field name made lowercase.
    descripition = models.CharField(db_column='Descripition', max_length=200, blank=True,
                                    null=True)  # Field name made lowercase.
    leaderid = models.ForeignKey(Student, models.DO_NOTHING, db_column='LeaderID')  # Field name made lowercase.
    maxnumber = models.IntegerField(db_column='maxNumber')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'team'


class Teamapply(models.Model):
    teamid = models.ForeignKey(Team, models.DO_NOTHING, db_column='teamID')  # Field name made lowercase.
    cid = models.ForeignKey(Course, models.DO_NOTHING, db_column='cID')  # Field name made lowercase.
    accept = models.CharField(db_column='Accept', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'teamapply'
        unique_together = (('teamid', 'cid'),)


class Teamcourse(models.Model):
    teamid = models.ForeignKey(Team, models.DO_NOTHING, db_column='teamID')  # Field name made lowercase.
    cid = models.ForeignKey(Course, models.DO_NOTHING, db_column='cID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'teamcourse'
        unique_together = (('teamid', 'cid'),)


class Teamjoin(models.Model):
    teamid = models.ForeignKey(Team, models.DO_NOTHING, db_column='teamID')  # Field name made lowercase.
    sid = models.ForeignKey(Student, models.DO_NOTHING, db_column='sID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'teamjoin'
        unique_together = (('teamid', 'sid'),)


class Teamsubmit(models.Model):
    teamid = models.ForeignKey(Teamcourse, models.DO_NOTHING, db_column='teamID')  # Field name made lowercase.
    cid = models.ForeignKey(Teamcourse, models.DO_NOTHING, db_column='cID',
                            related_name="t_cid")  # Field name made lowercase.
    taskindex = models.ForeignKey(Task, models.DO_NOTHING, db_column='TaskIndex')  # Field name made lowercase.
    submittime = models.DateTimeField(db_column='SubmitTime')  # Field name made lowercase.
    filepath = models.CharField(db_column='FilePath', max_length=2048)  # Field name made lowercase.
    grade = models.FloatField(db_column='Grade', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=2048, blank=True,
                               null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'teamsubmit'
        unique_together = (('teamid', 'cid', 'taskindex'),)


class Worksubmit(models.Model):
    sid = models.ForeignKey(Studentcourse, models.DO_NOTHING, db_column='sID',primary_key=True)  # Field name made lowercase.
    cid = models.ForeignKey(Studentcourse, models.DO_NOTHING, db_column='cID',
                            related_name="w_cid")  # Field name made lowercase.
    taskindex = models.ForeignKey(Task, models.DO_NOTHING, db_column='TaskIndex')  # Field name made lowercase.
    text = models.CharField(db_column='Text', max_length=4096, blank=True, null=True)  # Field name made lowercase.
    filepath = models.CharField(db_column='FilePath', max_length=2048)  # Field name made lowercase.
    submittime = models.DateTimeField(db_column='SubmitTime')  # Field name made lowercase.
    grade = models.FloatField(db_column='Grade', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=2048, blank=True,
                               null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'worksubmit'
        unique_together = (('sid', 'cid', 'taskindex'),)
