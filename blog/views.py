from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# def post_list(request):
#     # 使用的是我们定义的查询管理器
#     # 第一版，没有进行分页的的
#     posts = Post.published.all()
#     return render(request, 'blog/post/list.html',
#                   {'posts': posts})

def post_list(request):
    object_list = Post.published.all()
    # 相当于有一个默认的 一页 3 个
    paginator = Paginator(object_list, 3)
    # 这里有有一个 get 明确指定的
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger as err:
        # 参数错误就显示第一页就好
        posts = paginator.page(1)
    except EmptyPage as err:
        # 如果超过了最大的页数，那就是最后一页
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day = day)
    return render(request,
                  'blog/post/detail.html',
                  {'post':post})
