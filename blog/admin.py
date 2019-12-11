from django.contrib import admin
from .models import Post, Comment

'''
默认的方式
# 将  Post 注册在一个管理员页面里面
admin.site.register(Post)
'''

'''
# 定制管理站点

class PostAdmin(admin.ModelAdmin):
    # 将自己想要显示的表现出来,其他的暂时就先不要考虑
    # 这里的python 原理是, 子类使用变量的时候,会优先查找自己的命名空间
    list_display = ('title', 'slug', 'author', 'publish', 'status')


# 对比于第一种方式, Post  不变, 然后多了一个 PostAdmin, 表示是使用自己的
admin.site.register(Post, PostAdmin)
'''


# 更加详细的定制,也就是说,更多的时候django 内置的一些功能
class PostAdmin(admin.ModelAdmin):
    # 显示那些字段
    list_display = ('title', 'slug', 'author', 'publish', 'status')

    # 开启过滤功能
    list_filter = ('status', 'created', 'publish', 'author')

    # 开启搜索功能
    search_fields = ('title', 'body')

    # 根据别名 生成 slug
    # 这个地方的时候,title 不能使用中文
    prepopulated_fields = {'slug': ('title', )}

    # 设置外键的详细信息
    raw_id_fields = ('author', )

    # 按照日期进行筛选
    date_hierarchy = 'publish'

    # 修改排序的规则
    ordering = ['status', 'publish']


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(Comment, CommentAdmin)
