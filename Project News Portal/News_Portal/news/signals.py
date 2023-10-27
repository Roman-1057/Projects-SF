from django.core.exceptions import ValidationError
from django.utils import timezone

from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings

from .models import *


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


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_email = []

        for category in categories:
            subscribers = category.subscribers.all()
            subscribers_email += [user.email for user in subscribers]

        send_notify_subscribers(instance.preview(), instance.pk, instance.title, subscribers_email)


@receiver(pre_save, sender=Post)
def validate_post_count(sender, instance, **kwargs):
    """
    Сигнальная функция для контроля количества публикаций новостей пользователем.
    """
    # Определяем текущую дату и время
    current_date = timezone.now().date()

    # Определяем автора новости
    author = instance.author

    # Выполняем запрос, чтобы получить количество новостей автора за сегодняшний день
    post_count = Post.objects.filter(author=author, created_at__date=current_date).count()

    # Если количество новостей автора превышает 3, возвращаем ошибку валидации
    if post_count >= 3:
        raise ValidationError("Вы не можете публиковать более трех новостей в сутки.")
