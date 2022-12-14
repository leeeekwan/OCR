from django.db import models

# Create your models here.

class Body(models.Model):
    emp = models.ForeignKey('Employees', models.DO_NOTHING, blank=True, null=True)
    height = models.CharField(max_length=20, blank=True, null=True)
    weight = models.CharField(max_length=20, blank=True, null=True)
    eye_l = models.CharField(db_column='eye_L', max_length=20, blank=True, null=True)  # Field name made lowercase.
    eye_r = models.CharField(db_column='eye_R', max_length=20, blank=True, null=True)  # Field name made lowercase.
    disease = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'body'


class Employees(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    birth = models.CharField(max_length=10, blank=True, null=True)
    gender = models.IntegerField()
    depart = models.CharField(max_length=20, blank=True, null=True)
    class_field = models.CharField(db_column='class', max_length=20, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    phone = models.CharField(max_length=20, blank=True, null=True)
    addr = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=20, blank=True, null=True)
    resi_num = models.CharField(max_length=20, blank=True, null=True)
    hire_date = models.CharField(max_length=20, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employees'


class Info(models.Model):
    emp = models.ForeignKey(Employees, models.DO_NOTHING, blank=True, null=True)
    salary = models.CharField(max_length=20, blank=True, null=True)
    task = models.CharField(max_length=200, blank=True, null=True)
    graduation = models.CharField(max_length=200, blank=True, null=True)
    license = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'info'


class Soldier(models.Model):
    emp = models.ForeignKey(Employees, models.DO_NOTHING)
    kind = models.CharField(max_length=20, blank=True, null=True)
    s_rank = models.CharField(max_length=20, blank=True, null=True)
    number = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    depart = models.CharField(max_length=20, blank=True, null=True)
    on_date = models.CharField(max_length=20, blank=True, null=True)
    out_date = models.CharField(max_length=20, blank=True, null=True)
    discharge = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'soldier'
