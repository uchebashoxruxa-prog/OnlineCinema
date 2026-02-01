from django.urls import path
from .views import *

urlpatterns = [
    # path('api/v1/categories/', category_list_view),
    # path('api/v1/cinemas/', cinema_list_view),
    # path('api/v1/cinemas/<int:pk>/', cinema_by_category_view),
    # path('api/v1/cinema/<int:pk>/', cinema_detail_view),
    # path('api/v1/comment_create/<int:pk>/', comment_create_view),
    # path('api/v1/comment_update_delete/<int:pk>/', comment_update_delete_view),
    # path('api/v1/profile/<int:pk>/', profile_user_view),

    # Пусти для вьюшек на классе APIView ---
    # path('api/v1/categories/', CategoryListView.as_view()),
    # path('api/v1/cinemas/', CinemaListView.as_view()),
    # path('api/v1/cinemas/<int:pk>/', CinemaListByCategoryView.as_view()),
    # path('api/v1/cinema/<int:pk>/', CinemaDetailView.as_view()),
    # path('api/v1/comment/create/', CommentCreateApiView.as_view()),

            # Пусти для вьюшек на классах generics
    path('api/v1/categories/', CategoryListApiView.as_view()),
    path('api/v1/cinemas/', CinemaListApiView.as_view()),
    path('api/v1/cinemas/<int:pk>/', CinemaCategoryListApiView.as_view()),
    path('api/v1/cinema/<int:pk>/', CinemaDetailApiView.as_view()),
    path('api/v1/comment/create/', CommentCreateApiView.as_view()),
    path('api/v1/comment/action/<int:pk>/', CommentUpdateDeleteApiView.as_view()),
]





