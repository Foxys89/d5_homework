from django.urls import path
from .views import PostsList, PostDetail, PostSearch, NewsCreate,\
   PostEdit, PostDelete, ArticleCreate

urlpatterns = [
   path('', PostsList.as_view(), name = 'post_list'),
   path('<int:pk>', PostDetail.as_view(), name = 'post_detail'),
   path('search/', PostSearch.as_view(), name = 'post_search'),
   path('newscreate/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/newsedit/',PostEdit.as_view(), name='news_edit'),
   path('<int:pk>/newsdelete/', PostDelete.as_view(), name='news_delete'),
   path('articlecreate/', ArticleCreate.as_view(), name='article_create'),
   path('<int:pk>/articleedit/',PostEdit.as_view(), name='article_edit'),
   path('<int:pk>/articledelete/', PostDelete.as_view(), name='article_delete')
]