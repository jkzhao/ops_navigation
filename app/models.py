from django.db import models

# Create your models here.
class UrlGroup(models.Model):
    """
    定义导航项目的组
    """
    group_name = models.CharField('分类名称', max_length=100, unique=True)
    code = models.CharField('标签名称', max_length=100)
    createtime = models.DateTimeField(auto_now_add=True, null=True)
    updatetime = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = '导航分组'
        verbose_name_plural = '导航分组'

    def __str__(self):
        return self.group_name


class UrlInfor(models.Model):
    """
    定义导航项目的具体信息
    """
    url_name = models.CharField('链接名称', max_length=100)
    url_path = models.CharField('链接', max_length=200)
    url_desc = models.TextField('链接描述', max_length=200)
    url_group = models.ForeignKey(to=UrlGroup, verbose_name='分类名称', related_name='group_set', to_field="id")
    createtime = models.DateTimeField(auto_now_add=True, null=True)
    updatetime = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = '导航详情'
        verbose_name_plural = '导航详情'
        ordering = ['url_name']

    def __str__(self):
        return self.url_name
