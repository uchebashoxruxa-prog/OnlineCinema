from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import get_object_or_404

from online_cinema.models import *
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView


# Create your views here.
# @api_view(['GET'])
# def category_list_view(request):
#     categories = Category.objects.all()
#     serializer = CategoryListSerializer(categories, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def cinema_list_view(request):
#     cinemas = Cinema.objects.all()
#     serializer = CinemaListSerializer(cinemas, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def cinema_by_category_view(request, pk):
#     cinemas = Cinema.objects.filter(category=pk)
#     serializer = CinemaListSerializer(cinemas, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def cinema_detail_view(request, pk):
#     cinema = get_object_or_404(Cinema, pk=pk)
#     serializer = CinemaDetailSerializer(cinema)
#     return Response(serializer.data)
#
# @api_view(['POST'])
# def comment_create_view(request, pk):
#     cinema = get_object_or_404(Cinema, pk=pk)
#     if request.user.is_authenticated:
#         data = request.data
#         data['author_id'] = request.user.id
#         data['cinema_id'] = cinema.id
#         serializer = CommentCreateSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#
#
# @api_view(['PUT', 'DELETE'])
# def comment_update_delete_view(request, pk):
#     comment = get_object_or_404(Comment, pk=pk, author=request.user)
#     if request.method == 'PUT':
#         data = request.data
#         serializer = CommentCreateSerializer(comment, data=data)
#         serializer.is_valid()
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     elif request.method == 'DELETE':
#         comment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(['GET'])
# def profile_user_view(request, pk):
#     user = get_object_or_404(User, id=pk)
#     serializer = AuthUserSerializer(user)
#     return Response(serializer.data)
#  ----------  Вьюшки на классе APIView -------------------
# class CategoryListView(APIView):
#
#     def get(self, request):
#         categories = Category.objects.all()
#         serializer = CategoryListSerializer(categories, many=True)
#         return Response(serializer.data)
#
#
# class CinemaListView(APIView):
#
#     def get(self, request):
#         cinemas = Cinema.objects.all()
#         serializer = CinemaListSerializer(cinemas, many=True)
#         return Response(serializer.data)
#
#
# class CinemaListByCategoryView(APIView):
#
#     def get(self, request, pk):
#         cinemas = Cinema.objects.filter(category=pk)
#         serializer = CinemaListSerializer(cinemas, many=True)
#         return Response(serializer.data)
#
#
#
#
# class CinemaDetailView(APIView):
#
#     def get(self, request, pk):
#         cinemas = get_object_or_404(Cinema, pk=pk)
#         serializer = CinemaDetailSerializer(cinemas)
#         return Response(serializer.data)
#
#
#
# class CommentCreateApiView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         data = request.data  # {"text": "comment", "cinema": 5}
#         cinema = get_object_or_404(Cinema, pk=data["cinema"])
#         data["author"] = request.user.id
#         # data["cinema"] = cinema.id  # Но не обязательно
#         serializer = CommentCreateSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
from .services import IsOwner, CinemaPagination


class CategoryListApiView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CinemaListApiView(ListAPIView):
    queryset = Cinema.objects.all().order_by('-created_at')
    serializer_class = CinemaListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'actors']
    pagination_class = CinemaPagination
    permission_classes = [IsAuthenticated]


class CinemaCategoryListApiView(ListAPIView):
    serializer_class = CinemaListSerializer

    def get_queryset(self):
        cinemas = Cinema.objects.filter(category=self.kwargs['pk']).order_by('-created_at')
        return cinemas


class CinemaDetailApiView(RetrieveAPIView):
    queryset = Cinema
    serializer_class = CinemaDetailSerializer


class CommentCreateApiView(CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]


class CommentUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    queryset = Comment
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated, IsOwner]
