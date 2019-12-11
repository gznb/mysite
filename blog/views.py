from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail


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
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


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
