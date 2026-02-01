from django.urls import path
from .views import *

# В списке будим подключать пусти на страницы сайта
urlpatterns = [
    # path('', main_page, name='main'),
    # path('category/<int:pk>/', cinema_by_category, name='category'),
    # path('cinema/<int:pk>/', cinema_detail, name='cinema'),

    path('', CinemaList.as_view(), name='main'),
    path('category/<int:pk>/', CinemaByCategory.as_view(), name='category'),
    path('cinema/<int:pk>/', CinemaDetail.as_view(), name='cinema'),
    path('login/', login_user_view, name='login'),
    path('logout/', logout_user_view, name='logout'),
    path('register/', register_user_view, name='register'),
    path('search/', SearchCinema.as_view(), name='search'),
    path('save_comment/<int:pk>/', save_comment_cinema, name='save_comment'),
    path('comment_update/<int:pk>/', CommentUpdate.as_view(), name='comment_update'),
    path('comment_delete/<int:pk>/', comment_delete, name='comment_delete'),
    path('profile', profile_user, name='profile'),
    path('edit_account_profile/', edit_account_profile, name='edit'),

]







