from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Category, Cinema, Comment, ProfileUser, IpVisitor
from .forms import LoginForm, RegisterForm, CommentForm, EditAccountForm, EditProfileUserForm
from django.views.generic import ListView, DetailView, UpdateView
from .tests import get_client_ip

# Create your views here.
# def main_page(request):
#     cinemas = Cinema.objects.all().order_by('-created_at')
#     context = {
#         'title': 'OnlineCinema смотреть в качестве',
#         'cinemas': cinemas
#     }
#
#     return render(request, 'online_cinema/index.html', context)

class CinemaList(ListView):
    model = Cinema
    context_object_name = 'cinemas'
    template_name = 'online_cinema/index.html'
    ordering = '-created_at'
    extra_context = {
        'title': 'OnlineCinema смотреть в качестве'
    }


# ===============================================================================
# Функция для получения кинофильмов по категории
# def cinema_by_category(request, pk):
#     cinemas = Cinema.objects.filter(category=pk).order_by('-created_at')  # SELECT * FROM cinemas WHERE category_id =
#     cat = Category.objects.get(pk=pk)
#
#     context = {
#         'cinemas': cinemas,
#         'title': f'OnlineCinema {cat.title}'
#     }
#
#     return render(request, 'online_cinema/index.html', context)

class CinemaByCategory(CinemaList):

    def get_queryset(self):  # Метод что бы переназначить вывод
        cinemas = Cinema.objects.filter(category=self.kwargs['pk']).order_by('-created_at')
        return cinemas

    def get_context_data(self, *, object_list=None, **kwargs):  # Метод что бы доп что то передать
        context = super(CinemaByCategory, self).get_context_data()
        cat = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'OnlineCinema {cat.title}'
        return context

# ===============================================================================
# def cinema_detail(request, pk):
#     cinema = Cinema.objects.get(pk=pk)  # SELECT * FROM cinema WHERE id = ?
#
#     context = {
#         'title': f'OnlineCinema {cinema.title}',
#         'cinema': cinema
#     }
#
#     return render(request, 'online_cinema/cinema_detail.html', context)

class CinemaDetail(DetailView):
    model = Cinema
    context_object_name = 'cinema'

    def get_context_data(self, **kwargs):
        context = super(CinemaDetail, self).get_context_data()
        cinema = context['cinema']
        context['title'] = f'OnlineCinema {cinema.title}'
        same_cinemas = Cinema.objects.filter(category__in=cinema.category.all()).exclude(pk=cinema.pk)
        context['same_cinemas'] = same_cinemas.distinct().order_by('-created_at')[:4]
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()

        # Логика сохранения ip для просмотров
        ip = get_client_ip(self.request)
        if IpVisitor.objects.filter(ip=ip).exists():  # Проверяем есть ли ip в базе
            cinema.views.add(IpVisitor.objects.get(ip=ip))
        else:
            IpVisitor.objects.create(ip=ip)  # Если нет в базе до создаём
            cinema.views.add(IpVisitor.objects.get(ip=ip))  # В кинофильм в просмотры добавляем ip

        context['comments'] = Comment.objects.filter(cinema=cinema).order_by('-created_at')  # Получим комментарии кинофильма
        return context

# ===============================================================================
# Вьюшка для Авторизации
def login_user_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)

        return redirect('main')


# Вьюшка для выхода из аккаунта
def logout_user_view(request):
    logout(request)
    return redirect('main')


def register_user_view(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            profile = ProfileUser.objects.create(user=user)
            profile.save()
            login(request, user)


        return redirect('main')



# Вьюшка для поиска кинофильмов
class SearchCinema(CinemaList):

    def get_queryset(self):  # Метод что бы переназначить вывод
        word = self.request.GET.get('q')
        cinemas = Cinema.objects.filter(title__iregex=word).order_by('-created_at')
        return cinemas


def save_comment_cinema(request, pk):
    if request.user.is_authenticated and request.method == 'POST':
        try:
            cinema = Cinema.objects.get(pk=pk)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.cinema = cinema
                comment.save()

            return redirect('cinema', cinema.pk)
        except:
            return redirect('main')
    else:
        return redirect('login')


class CommentUpdate(UpdateView):
    form_class = CommentForm
    model = Comment

    def get_success_url(self):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        return reverse('cinema', kwargs={'pk': comment.cinema.pk})

    def form_valid(self, form):
        try:
            comment = Comment.objects.get(pk=self.kwargs['pk'], author=self.request.user)
            if comment and self.request.user.is_authenticated:
                return super(CommentUpdate, self).form_valid(form)
            else:
                return redirect('main')
        except:
            return redirect('main')




def comment_delete(request, pk):
    if request.user.is_authenticated and request.method == 'POST':
        try:
            comment = Comment.objects.get(pk=pk)
            if comment.author == request.user:
                comment.delete()

            return redirect('cinema', comment.cinema.pk)
        except:
            return redirect('main')
    else:
        return redirect('main')



def profile_user(request):
    if request.user.is_authenticated:
        profile = ProfileUser.objects.get(user=request.user)
        context = {
            'title': f'Профиль {profile.user.username}',
            'profile': profile,
            'account_form': EditAccountForm(instance=request.user),
            'profile_form': EditProfileUserForm(instance=request.user.profileuser)
        }

        return render(request, 'online_cinema/profile.html', context)

    else:
        return redirect('login')




def edit_account_profile(request):
    if request.user.is_authenticated and request.method == 'POST':
        account_form = EditAccountForm(request.POST, instance=request.user)
        profile_form = EditProfileUserForm(request.POST, request.FILES, instance=request.user.profileuser)
        if account_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            account_form.save()

            # Логика изменения пароля
            data = account_form.cleaned_data  # Функция которая позволит получить данные из формы в виде словаря
            user = User.objects.get(id=request.user.id)
            if user.check_password(data['old_password']):
                if data['old_password'] != data['new_password'] and data['new_password'] == data['confirm_password']:
                    user.set_password(data['new_password'])
                    user.save()
                    update_session_auth_hash(request, user)

            return redirect('profile')

    else:
        return redirect('main')

