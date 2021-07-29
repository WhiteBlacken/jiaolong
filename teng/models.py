from django.db import models

# Create your models here.
# models.py
from django.db import models
import django.utils.timezone as timezone
import base64


# Country
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Country(models.Model):
    name_cn = models.CharField(max_length=90, default=None)
    language_cn = models.CharField(max_length=90, default=None)
    name_en = models.CharField(max_length=90, default=None)
    language_en = models.CharField(max_length=90, default=None)
    comment = models.CharField(max_length=600, null=True)

    _flag = models.TextField(
        db_column='flag',
        blank=True)

    def set_flag(self, flag):
        self._flag = base64.encodestring(flag)

    def get_flag(self):
        return base64.decodestring(self._flag)

    flag = property(get_flag, set_flag)

    def __str__(self):
        return self.name_cn


class Product(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Business(models.Model):
    name_cn = models.CharField(max_length=90)
    name_en = models.CharField(max_length=90, default=None)
    show_order = models.IntegerField(default=0)
    comment = models.CharField(max_length=600, null=True)
    icon = models.CharField(max_length=32, default='lightbulb')

    def __str__(self):
        return self.name_cn


class Subbusiness(models.Model):
    name_cn = models.CharField(max_length=90)
    name_en = models.CharField(max_length=90)
    show_order = models.IntegerField(default=0)
    parent = models.ForeignKey(Business, on_delete=models.CASCADE)
    comment = models.CharField(max_length=600, null=True)

    def __str__(self):
        return self.name_cn


class Keyword(models.Model):
    chinese_keyword = models.CharField(max_length=90, unique=True)
    english_keyword = models.CharField(max_length=90, unique=True)
    status = models.SmallIntegerField(default=0)
    similar_set = models.IntegerField(default=0)
    comment = models.CharField(max_length=600, null=True)
    # 新增：qxy
    subbusiness = models.ForeignKey(Subbusiness, on_delete=models.CASCADE, default=2)
    # create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    # update_time = models.DateTimeField(auto_now=True)  # 最后更新时间

    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    review_time = models.DateTimeField(auto_now=True)  # 最后更新时间
    searched_times = models.IntegerField(default=0)


    def __str__(self):
        return self.chinese_keyword

@receiver(pre_save, sender=Keyword)
def pre_save_handler(sender, **kwargs):
    # 我们可以在Keyword这个Model保存之前尽情调戏了：）
    print("nihaoa")



## 中文关键词附表
class Keyword_cn(models.Model):
    chinese_keyword = models.CharField(max_length=90, unique=True)
    subbusiness = models.ForeignKey(Subbusiness, on_delete=models.CASCADE, default=0)
    # subbusiness_id = models.IntegerField(default=0)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, default=2)
    # keyword_id = models.IntegerField(default=0)
    comment = models.CharField(max_length=600, null=True)


## 英文关键词附表
class Keyword_en(models.Model):
    english_keyword = models.CharField(max_length=90, unique=True)
    subbusiness = models.ForeignKey(Subbusiness, on_delete=models.CASCADE, default=0)
    # subbusiness_id = models.IntegerField(default=0)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, default=2)
    # keyword_id = models.IntegerField(default=0)
    comment = models.CharField(max_length=600, null=True)


## 爬虫多对多映射表
class Keyword_website_turkey(models.Model):
    keyword_id = models.IntegerField(default=0, null=True)
    chinese_keyword = models.CharField(max_length=90, null=True,unique=True)
    english_keyword = models.CharField(max_length=90, null=True)
    turkish_keyword = models.CharField(max_length=150)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=2)

    # url暂时这么写
    url_id = models.IntegerField(default=100, null=True)
    """状态信息类型"""
    # status = (
    #     (0, "还没被搜索"),
    #     (1, "搜索未完成，但正常搜索结束"),
    #     (2, "搜索未完成并非正常搜索结束"),
    #     (3, "正常搜索完成")
    # )
    status = models.SmallIntegerField(default=0, null=True)
    comment = models.CharField(max_length=600, null=True)

    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    review_time = models.DateTimeField(auto_now=True)  # 最后更新时间




# Chinese models here.
class Supplier(models.Model):
    name_cn = models.CharField(max_length=300, unique=True)
    name_en = models.CharField(max_length=300, unique=True, default=None, blank=True)
    name_tr = models.CharField(max_length=300, unique=True, default=None, blank=True)
    credit = models.DecimalField(max_digits=3, decimal_places=2, default=7.00)
    status = models.SmallIntegerField(default=0)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=2)
    website = models.CharField(max_length=2048, default="http://www.baidu.com", blank=True)
    scale = models.CharField(max_length=30, default=None)
    built_year = models.SmallIntegerField(default=1970)
    address_cn = models.CharField(max_length=300, blank=True, default="广南路")
    address_en = models.CharField(max_length=300, blank=True, default="广南路")
    email = models.EmailField(null=True, blank=True)
    office_phone = models.CharField(max_length=24, blank=True, default="16621360442")
    cell_phone = models.CharField(max_length=24, blank=True, default="16621360442")
    description_cn = models.CharField(max_length=1500, blank=True, default="很不错的公司")
    description_en = models.CharField(max_length=1500, blank=True, default="nice company")
    created_date = models.DateTimeField(default=timezone.now)
    review_date = models.DateTimeField(default=timezone.now)
    products = models.ManyToManyField("Product")
    categories = models.ManyToManyField("Subbusiness")
    comment = models.CharField(max_length=600, null=True, default="test data")
    visited_times = models.IntegerField(default=0)
    keywords_collected = models.CharField(max_length=3000)

    # test = models.CharField(max_length=90)

    def __str__(self):
        return self.name_cn


class Keyword_supplier(models.Model):
    chinese_keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    rank = models.SmallIntegerField(default=100)
