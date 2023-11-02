from celery import shared_task

from django.db.models.functions import datetime
import datetime

from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post, Category, PostCategory


@shared_task  # функция отправки письма
def send_notify_subscribers(preview, pk, title, subscribers):
    html_content = render_to_string(
        'email_template.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task  # отправка писем всем подписчикам в категории
def notify_subscribers(instance_id):
    instance = PostCategory.objects.get(pk=instance_id)
    categories = instance.category.all()
    subscribers_email = []

    for category in categories:
        subscribers = category.subscribers.all()
        subscribers_email += [user.email for user in subscribers]

    send_notify_subscribers(instance.preview(), instance.pk, instance.title, subscribers_email)


@shared_task  # еженедельная рассылка в 8 утра понедельника
def new_posts_week():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(created_at__gt=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject="Статьи за неделю",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

