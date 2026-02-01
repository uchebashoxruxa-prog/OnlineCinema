from online_cinema.models import Category
from django import template
from online_cinema.forms import LoginForm, RegisterForm

register = template.Library()

@register.simple_tag()
def get_categories():
    categories = Category.objects.all()
    return categories


@register.simple_tag()
def auth_forms():
    return {
        'login_form': LoginForm(),
        'register_form': RegisterForm()
    }

