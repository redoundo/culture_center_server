# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.timezone import now


class Applied(models.Model):
    appliedid = models.AutoField(db_column='appliedId', primary_key=True)  # Field name made lowercase.
    appliedlectureid = models.IntegerField(db_column='appliedLectureId')  # Field name made lowercase.
    applieduserid = models.IntegerField(db_column='appliedUserId')  # Field name made lowercase.

    def dictionary(self):
        return {
            "appliedId": self.appliedid, "appliedLectureId": self.appliedlectureid, "appliedUserId": self.applieduserid
        }

    class Meta:
        managed = True
        db_table = 'applied'


class Branches(models.Model):
    branchid = models.AutoField(db_column='branchId', primary_key=True)  # Field name made lowercase.
    branchname = models.CharField(db_column='branchName', unique=True, max_length=255)  # Field name made lowercase.
    branchaddress = models.CharField(db_column='branchAddress', max_length=255)  # Field name made lowercase.
    centeridofbranch = models.IntegerField(db_column='centerIdOfBranch')  # Field name made lowercase.

    def dictionary(self):
        return {
            "branchId": self.branchid, "branchName": self.branchname, "branchAddress": self.branchaddress, "centerIdOfBranch": self.centeridofbranch
        }

    class Meta:
        managed = True
        db_table = 'branches'


class Categories(models.Model):
    categoryid = models.AutoField(db_column='categoryId', primary_key=True)  # Field name made lowercase.
    categoryname = models.CharField(db_column='categoryName', max_length=100)  # Field name made lowercase.
    targetid = models.IntegerField(db_column='targetId')  # Field name made lowercase.

    def dictionary(self):
        return {"categoryId": self.categoryid, "categoryName": self.categoryname, "targetId": self.targetid}

    class Meta:
        managed = True
        db_table = 'categories'


class Centers(models.Model):
    centerid = models.AutoField(db_column='centerId', primary_key=True)  # Field name made lowercase.
    centername = models.CharField(db_column='centerName', unique=True, max_length=90)  # Field name made lowercase.
    centertype = models.CharField(db_column='centerType', max_length=45)  # Field name made lowercase.
    centerurl = models.CharField(db_column='centerUrl', max_length=200)  # Field name made lowercase.
    
    def dictionary(self):
        return {"centerId": self.centerid, "centerName": self.centername, "centerType": self.centertype, "centerUrl": self.centerurl}

    class Meta:
        managed = True
        db_table = 'centers'


class Lectures(models.Model):
    lectureid = models.AutoField(db_column='lectureId', primary_key=True)  # Field name made lowercase.
    center = models.CharField(max_length=90)
    type = models.CharField(max_length=50)
    region = models.CharField(max_length=60)
    branch = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    target = models.CharField(max_length=90)
    category = models.CharField(max_length=90)
    title = models.CharField(max_length=300)
    url = models.CharField(unique=True, max_length=400)
    src = models.TextField()
    content = models.TextField()
    price = models.IntegerField()
    adult = models.CharField(max_length=50, blank=True, null=True)
    kid = models.CharField(max_length=45, blank=True, null=True)
    baby = models.CharField(max_length=45, blank=True, null=True)
    lecturestart = models.DateTimeField(db_column='lectureStart')  # Field name made lowercase.
    lectureend = models.DateTimeField(db_column='lectureEnd')  # Field name made lowercase.
    enrollstart = models.DateTimeField(db_column='enrollStart', blank=True, null=True)  # Field name made lowercase.
    enrollend = models.DateTimeField(db_column='enrollEnd', blank=True, null=True)  # Field name made lowercase.
    lecturesupplies = models.CharField(db_column='lectureSupplies', max_length=200, blank=True, null=True)
    curriculum = models.JSONField(blank=True, null=True)
    crawleddate = models.DateTimeField(db_column='crawledDate', default=now)  # Field name made lowercase.
    lecturehelddates = models.CharField(db_column='lectureHeldDates', max_length=500, blank=True, null=True)  # Field name made lowercase.

    def dictionary(self) -> dict:
        return {
            "lectureId": self.lectureid, "center": self.center, "type": self.type, "region": self.region, "branch": self.branch,
            "address": self.address, "target": self.target, "category": self.category, "title": self.title, "url": self.url,
            "src": self.src, "content": self.content, "price": self.price, "lectureStart": self.lecturestart,
            "lectureEnd": self.lectureend, "enrollStart": self.enrollstart, "enrollEnd": self.enrollend,
            "lectureSupplies": self.lecturesupplies, "curriculum": self.curriculum, "crawledDate": self.crawleddate,
            "lectureHeldDates": self.lecturehelddates
        }
    
    class Meta:
        managed = True
        db_table = 'lectures'


class Liked(models.Model):
    likedid = models.AutoField(db_column='likedId', primary_key=True)  # Field name made lowercase.
    likedlectureid = models.IntegerField(db_column='likedLectureId')  # Field name made lowercase.
    likeduserid = models.IntegerField(db_column='likedUserId')  # Field name made lowercase.

    def dictionary(self):
        return {
            "liekdId": self.likedid, "likedLectureId": self.likedlectureid, "likedUserId": self.likeduserid
        }


    class Meta:
        managed = True
        db_table = 'liked'


class Targets(models.Model):
    targetid = models.AutoField(db_column='targetId', primary_key=True)  # Field name made lowercase.
    targetname = models.CharField(db_column='targetName', max_length=45)  # Field name made lowercase.
    
    def dictionary(self):
        return {"targetId": self.targetid, "targetName": self.targetname}

    class Meta:
        managed = True
        db_table = 'targets'


class Users(models.Model):
    userid = models.AutoField(db_column='userId', primary_key=True)  # Field name made lowercase.
    email = models.CharField(unique=True, max_length=255)
    nickname = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    registerdate = models.DateTimeField(db_column='registerDate', default=now)  # Field name made lowercase.
    snsprovider = models.CharField(db_column='snsProvider', max_length=255)  # Field name made lowercase.
    snsproviderid = models.CharField(db_column='snsProviderId', unique=True, max_length=255) # Field name made lowercase.
    wantfcmmessage = models.IntegerField(db_column='wantFcmMessage', default=0)  # Field name made lowercase.
    fcmtoken = models.CharField(db_column='fcmToken', max_length=500, blank=True, null=True)  # Field name made lowercase.

    def dictionary(self) -> dict:
        return {
            "userId": self.userid, "email": self.email, "nickname": self.nickname, "password": self.password,
            "registerDate": self.registerdate, "snsProvider": self.snsprovider, "snsProviderId": self.snsproviderid,
            "wantFcmMessage": self.wantfcmmessage, "fcmToken": self.fcmtoken
        }

    class Meta:
        managed = True
        db_table = 'users'
