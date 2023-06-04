from django.db import models
from haystack import indexes


# class Case(models.Model):
    # class Meta:
    #     app_label = 'case'
#     id = models.AutoField(primary_key=True) 

#     qw_value = models.CharField(max_length=200) # 全文
#     ws_value = models.CharField(max_length=200) # 文首
#     jbfy_value = models.CharField(max_length=200) # 经办法院
#     xzqh_p_value = models.CharField(max_length=200) # 行政区划-省份
#     xzqh_c_value = models.CharField(max_length=200) # 行政区划-城市
#     land_value = models.CharField(max_length=200) # 年份


#     search_index = indexes.CharField(document=True, use_template=True)

class Law(models.Model):
    # class Meta:
    #     app_label = 'laws'
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Case(models.Model):
    # class Meta:
    #     app_label = 'cases'
    id = models.AutoField(primary_key=True) 
    qw_value = models.TextField(max_length=500) # 全文
    head = models.CharField(max_length=200) # 文首
    related_people = models.TextField() # 当事人
    judicial_record = models.TextField() # 诉讼记录
    basic_info = models.TextField() # 案件基本情况
    judgement_process = models.TextField() # 判决分析过程
    result = models.TextField() # 判决结果
    tail = models.TextField() # 文尾

    note_name = models.CharField(max_length=30) # 文书名称
    judge_prop = models.CharField(max_length=30) # 审判程序（一审/二审）
    
    court = models.CharField(max_length=30) # 经办法院
    case_reason = models.CharField(max_length=30) # 案由
    province = models.CharField(max_length=200) # 行政区划-省份
    year = models.IntegerField(default=2023) # 年份
    laws = models.ManyToManyField(to=Law, related_name="cases") # 法律条文

    # search_index = indexes.CharField(document=True, use_template=True)

    def __str__(self):
        return self.head
    


