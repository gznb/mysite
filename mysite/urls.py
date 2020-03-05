"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

'''
2020-03-15  
1. url 使用正则表达式的方式进行接入。
2. 使用include 导入urls
'''

from django.contrib import admin
from django.conf.urls import include, url
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    # admin.site.urls 是一特殊的存在 不能用  include
    url(r'^admin/', admin.site.urls),
    # url(r'^blog/', include('blog.urls', namespace='blog')),
    # 这里做了新的改动，把App name 放在元组里面
    url(r'^blog/', include(('blog.urls', 'blog'), namespace='blog')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

