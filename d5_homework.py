from django.contrib.auth.models import User

#Создать двух пользователей (с помощью метода User.objects.create_user('username')).
user1 = User.objects.create_user('username1', 'myemail@email.com', 'Mypassword')
user2 = User.objects.create_user('username2', 'myemail@email2.com', 'Mypassword')

#Создать два объекта модели Author, связанные с пользователями.
from news.models import *
author1 = Author.objects.create(user_author = user1)
author2 = Author.objects.create(user_author = user2)

#Добавить 4 категории в модель Category.
category1 = Category.objects.create(category_name = 'Category1')
category2 = Category.objects.create(category_name = 'Category2')
category3 = Category.objects.create(category_name = 'Category3')
category4 = Category.objects.create(category_name = 'Category4')

#Добавить 2 статьи и 1 новость.
post1 = Post.objects.create(post_author = author1, post_type = 'AR', post_name = 'article1', post_text = 'some text')
post2 = Post.objects.create(post_author = author2, post_type = 'AR', post_name = 'article2', post_text = 'some text')
post3 = Post.objects.create(post_author = author1, post_type = 'AR', post_name = 'news1', post_text = 'some text')

#Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
post1.post_category.add(category1)
post1.post_category.add(category2)
post2.post_category.add(category2)
post2.post_category.add(category3)
post3.post_category.add(category3)
post3.post_category.add(category4)

#Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
comment1 = Comment.objects.create(comment_post = post1, comment_user = user1, comment_text = 'some text')
comment2 = Comment.objects.create(comment_post = post2, comment_user = user2, comment_text = 'some text')
comment3 = Comment.objects.create(comment_post = post3, comment_user = user2, comment_text = 'some text')
comment4 = Comment.objects.create(comment_post = post3, comment_user = user1, comment_text = 'some text')

#Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
post1.like()
post1.like()
post1.like()
post2.like()
post2.like()
post3.dislike()
post3.dislike()
post4.dislike()
comment4.dislike()
comment3.like()
comment2.like()
comment2.like()
comment2.like()
comment1.dislike()
comment1.dislike()

#Обновить рейтинги пользователей.
from django.db.models import Sum
author1.update_rating()
author2.update_rating()

#Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
best_user = Author.objects.order_by('-user_rating').values('user_author__username', 'user_rating').first()
print(f"Лучший пользователь: {best_user['user_author__username']} с рейтингом {best_user['user_rating']}")

#Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
best_article = Post.objects.filter(post_type='AR').order_by('-post_rating').first()
print('Лучшая статья:', best_article.post_time.strftime('%d.%m.%y %H:%M:%S'), best_article.post_author.user_author.username,
      best_article.post_name, best_article.preview(), sep='\n')

#Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
comments = Comment.objects.filter(comment_post=best_article)
for c in comments:
      print(f"дата: {c.comment_time.strftime('%d.%m.%y %H:%M:%S')}, пользователь: {c.comment_user.username}, "
            f"рейтинг {c.comment_rating}, текст комментария: {c.comment_text}")