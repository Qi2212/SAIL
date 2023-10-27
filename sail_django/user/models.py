from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username=models.CharField(max_length=30,verbose_name='用户名',unique=True,primary_key=True)
    password=models.CharField(max_length=32,verbose_name='密码')
#重置数据库表名
    class Meta:
        db_table = 'user_user_profile'
