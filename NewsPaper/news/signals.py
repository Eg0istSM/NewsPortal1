from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory, Post
from django.conf import settings
import datetime

def send_notifications(preview, pk, title, subscribers):
    for subscriber in subscribers:
        html_content = render_to_string(
            'post_created_email.html',
            {
                'username': subscriber.username,
                'text': preview,
                'link': f'{settings.SITE_URL}/post/{pk}',
            }
        )

        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email],

        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_users = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_users += [s for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_users)

#перенес в формс с нормальным выводом в пользователю
# @receiver(pre_save, sender=Post)
# def post_limit(sender, instance, **kwargs):
#     today = datetime.date.today()
#     post_limit = Post.objects.filter(author=instance.aythor, time_post__date=today).count()
#     if post_limit >= 3:
#         raise ValidationError('Нельзя публиковать более трех постов в сутки!')


