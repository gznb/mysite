from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    # 定义了一个选择的元组
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250, verbose_name='标题')

    slug = models.SlugField(max_length=250, unique_for_date='publish')

    # 使用的是 级联删除，，如果作者没有了，文章就都没有了
    # 这里关联的作者是 django  权限控制表里面的默认的 User
    author = models.ForeignKey(User, related_name='blog_posts',verbose_name='作者', on_delete=models.CASCADE)

    body = models.TextField(verbose_name='消息主体内容')

    publish = models.DateTimeField(default=timezone.now, verbose_name='发表时间')

    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='状态')

    class Meta:
        # 默认使用  发布时间降序排列
        ordering = ('-publish', )

    def __str__(self):
        # 为调试做准备
        return self.title





