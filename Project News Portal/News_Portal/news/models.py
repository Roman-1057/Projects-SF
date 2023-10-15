from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')
    rating = models.FloatField(default=0.0)

    def update_rating(self):  # Метод обновления рейтинга
        # Рейтинг постов
        article_rating = Post.objects.filter(author=self).aggregate(models.Sum('rating'))['rating__sum'] or 0
        # Рейтинг комментов авторов
        comment_rating = Comment.objects.filter(post__author=self).aggregate(models.Sum('rating'))['rating__sum'] or 0
        # Рейтинг комментов к постам
        comment_rating_to_articles = Comment.objects.filter(post__author=self).aggregate(models.Sum('rating'))['rating__sum'] or 0

        self.rating = article_rating * 3 + comment_rating + comment_rating_to_articles
        self.save()

    def set_default_rating(self):
        self.rating = self._meta.get_field('rating').get_default()
        self.save()

    def __str__(self):
        return self.user.username.title()


class Category(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    ARTICLE = 'article'
    NEWS = 'news'

    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=10, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField(default="Нет содержания")
    rating = models.FloatField(default=0.0)

    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):  # Метод лайка
        self.rating += 1
        self.save()

    def dislike(self):  # Метод дизлайка
        self.rating -= 1
        self.save()

    def preview(self):  # Метод показа начала поста
        if len(self.text) <= 124:
            return self.text
        else:
            return self.text[:124] + '...'

    def __str__(self):
        if self.post_type == 'article':
            return f'{self.title.title()}: {self.text[:20]}'
        else:
            return self.title.title()

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):  #  Модель связей многие ко многим
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField(default="Нет содержания")
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
