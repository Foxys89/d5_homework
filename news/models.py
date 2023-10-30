from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    user_author = models.OneToOneField(User, on_delete = models.CASCADE)
    user_rating = models.IntegerField(default = 0)

    def update_rating(self):
        ap_rating = self.post_set.all().aggregate(sum = Sum('post_rating'))['sum']
        aucom_rating = self.user_author.comment_set.all().aggregate(sum = Sum('comment_rating'))['sum']
        comm_rating = Comment.objects.filter(comment_post__post_author = self).aggregate(sum = Sum('comment_rating'))['sum']
        self.user_rating = ap_rating * 3 + aucom_rating + comm_rating
        self.save()



class Category(models.Model):
    category_name = models.CharField(max_length = 255,
                                     unique = True)


class Post(models.Model):
    news = 'NW'
    article = 'AR'
    POST_TYPES = [
        (article, 'Статья'),
        (news, 'Новость')
        ]
    post_author = models.ForeignKey('Author', on_delete = models.CASCADE)
    post_type = models.CharField(max_length = 2,
                                 choices = POST_TYPES,
                                 default = news)
    post_time = models.DateTimeField(auto_now_add = True)
    post_category = models.ManyToManyField('Category', through = 'PostCategory')
    post_name = models.CharField(max_length = 255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default = 0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.post_text[:124]}...'


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