from django.db import models


class Chart(models.Model):
    creater_id = models.IntegerField()
    hash_id = models.CharField(max_length=255)
    options = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'chart'


class Datasource(models.Model):
    user_id = models.IntegerField()
    type = models.CharField(max_length=255)
    options = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    tips = models.CharField(max_length=255, blank=True, null=True)
    hash_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'datasource'


class Message(models.Model):
    content = models.TextField(blank=True, null=True)
    from_id = models.IntegerField()
    from_name = models.CharField(max_length=255)
    to_id = models.IntegerField()
    to_name = models.CharField(max_length=255)
    readed = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'message'


class Project(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=255)
    tips = models.CharField(max_length=255, blank=True, null=True)
    hash_id = models.CharField(max_length=255)
    options = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    chart_mode = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'project'


class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    userpicture = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    user_admin = models.IntegerField(default=0)
    manage = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'user'