from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

class Author(models.Model):
    user_author = models.OneToOneField(User, on_delete = models.CASCADE)
    user_rating = models.IntegerField(default = 0)

    def update_rating(self):
        ap_rating = self.post_set.all().aggregate(sum = Sum('post_rating'))['sum']
        aucom_rating = self.user_author.comment_set.all().aggregate(sum = Sum('comment_rating'))['sum']
        comm_rating = Comment.objects.filter(comment_post__post_author = self).aggregate(sum = Sum('comment_rating'))['sum']
        self.user_rating = ap_rating * 3 + aucom_rating + comm_rating
        self.save()

    def __str__(self):
        return self.user_author.username



class Category(models.Model):
    category_name = models.CharField(max_length = 255,
                                     unique = True)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    news = 'NW'
    article = 'AR'
    POST_TYPES = [
        (article, 'Статья'),
        (news, 'Новость')
        ]
    post_author = models.ForeignKey('Author', on_delete = models.CASCADE, verbose_name='Автор')
    post_type = models.CharField(max_length = 2,
                                 choices = POST_TYPES,
                                 default = news, verbose_name='Тип')
    post_time = models.DateTimeField(auto_now_add = True, verbose_name='Дата создания')
    post_category = models.ManyToManyField('Category', through = 'PostCategory', verbose_name='Категория')
    post_name = models.CharField(max_length = 255, verbose_name='Заголовок')
    post_text = models.TextField(verbose_name='Содержание публикации')
    post_rating = models.IntegerField(default = 0, verbose_name='Рейтинг статьи')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.post_text[:124]}...'

    def __str__(self):
        return f'{self.post_name}: {self.preview()}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[int(self.pk)])


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete = models.CASCADE)
    category = models.ForeignKey('Category', on_delete = models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey('Post', on_delete = models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add = True)
    comment_rating = models.IntegerField(default = 0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return self.comment_user.username