from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.SET_NULL,
        null=True
    )
    slug = models.SlugField(max_length=200, unique=True)
    published_at = models.DateTimeField(
        "Дата и время публикации",
        auto_now_add=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['published_at']
        verbose_name = 'пост'
        verbose_name_plural = 'посты'


class Comment(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.SET_NULL,
        null=True
    )
    post = models.ForeignKey(
        Post,
        verbose_name='Пост',
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        'self',
        verbose_name='Родительский коментарий',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    published_at = models.DateTimeField(
        "Дата и время публикации",
        auto_now_add=True,
    )
    depth = models.PositiveIntegerField('Глубина вложенности', blank=True)

    def __str__(self):
        return f'{self.author} - {self.post} - {self.published_at}'

    def save(self, *args, **kwargs):
        self.depth = 1 if not self.parent_id else self.parent.depth + 1
        super(Comment, self).save(*args, **kwargs)

    class Meta:
        ordering = ['post', 'published_at']
        verbose_name = 'коментарий'
        verbose_name_plural = 'коментарии'
