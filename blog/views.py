from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from taggit.models import Tag
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count


def post_list(request, tag_slug=None):
    # 先是得到所有的帖子
    object_list = Post.published.all()
    tag = None
    # 如果标签被使用
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        # 根据标签进行过滤
        object_list = object_list.filter(tags__in=[tag])

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

    # 将页面，以及页面数据丢过去，使用的是模板语言， 传递了相应的变量
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # 帖子的评论列表
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # 得到表单的评论
        comment_form = CommentForm(data=request.POST)
        # 验证通过
        if comment_form.is_valid():
            # 创建对象，但是还没有保存
            new_comment = comment_form.save(commit=False)
            # 将当前帖子分配给评论
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


# 分页的视图类
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = '{} ({}) reconmends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{} comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'gznbgznb@163.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
