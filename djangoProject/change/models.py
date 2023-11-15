from django.db import models

# Create your models here.

class Channel_info(models.Model):
    channel_no=models.IntegerField(verbose_name='通道序号',unique=True,primary_key=True)#
    channel_status=models.CharField(max_length=30,verbose_name='通道状态',default='未配置')
    address=models.CharField(max_length=100,verbose_name='RTSP地址',default='rtsp://xxxxx')
    channel_name=models.CharField(max_length=30,verbose_name='通道名称',default='ID_xx')
    #算法配置-人数统计
    person_status=models.CharField(max_length=30,verbose_name='算法-人数统计开关状态',default='开')
    person_sensitive=models.IntegerField(verbose_name='算法-人数统计灵敏度')
    person_frequency=models.IntegerField(verbose_name='算法-人数统计频率')
    #算法配置-车辆统计
    car_status=models.CharField(max_length=30,verbose_name='算法-车辆统计开关状态',default='开')
    car_sensitive=models.IntegerField(verbose_name='算法-车辆统计灵敏度')
    car_frequency=models.IntegerField(verbose_name='算法-车辆统计频率')
    #周界
    week=models.CharField(max_length=30,verbose_name='周界',default='')
    #最后一次修改时间
    change_time=models.DateTimeField(verbose_name='修改时间',auto_now=True)
    class Meta:
        db_table = 'channel_info'