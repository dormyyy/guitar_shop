from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .forms import *
from .models import *
from cart.cart import Cart

menu = [
    {'title': 'Про сайт', 'url_name': 'about'},
    {'title': 'Додати товар', 'url_name': 'add_product'},
    {'title': 'Корзина', 'url_name': 'cart_detail'},
]
about_txt = 'Ласкаво просимо до інтернет магазину гітар!\n' \
        'У нашому магазині ви зможете підібрати інструмент для себе, а також переглянути їх велику кількість!'


class GuitarsHome(ListView):
    paginate_by = 3
    model = Guitars
    template_name = 'guitars/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Головна сторінка'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Guitars.objects.filter(is_published=True)


class ShowPost(DetailView):
    model = Guitars
    template_name = 'guitars/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = context['post']
        context['menu'] = menu
        return context


class AddPage(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    form_class = AddPostForm
    template_name = 'guitars/addproduct.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Додання товару'
        context['menu'] = menu
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect('home')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'guitars/registration.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Реєстрація'
        context['menu'] = menu
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'guitars/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вхід'
        context['menu'] = menu
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def about(request):
    context = {
        'menu': menu,
        'title': 'Про сайт',
        'about': about_txt
    }
    return render(request, 'guitars/about.html', context=context)


def show_category(request, cat_id):
    posts = Guitars.objects.filter(category=cat_id)
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'posts': posts,
        'menu': menu,
        'title': 'Відображення по категоріям',
        'cat_selected': cat_id
    }
    return render(request, 'guitars/index.html', context=context)


def show_user_posts(request, user_name):
    posts = Guitars.objects.filter(author__username=user_name)
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'posts': posts,
        'menu': menu,
        'title': 'Відображення по категоріям'
    }
    return render(request, 'guitars/index.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url=reverse_lazy('login'))
def cart_add(request, id):
    cart = Cart(request)
    product = Guitars.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url=reverse_lazy('login'))
def item_clear(request, id):
    cart = Cart(request)
    product = Guitars.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url=reverse_lazy('login'))
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url=reverse_lazy('login'))
def cart_detail(request):
    context = {
        'menu': menu,
        'title': 'Корзина'
    }
    return render(request, 'guitars/cart_detail.html', context=context)


def successfully_purchased(request):
    context = {
        'menu': menu,
        'title': 'Покупка успішна!'
    }
    cart_clear(request)
    return render(request, 'guitars/purchase.html', context=context)
