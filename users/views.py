from itertools import product
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, resolve
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .forms import UserRegisterForm, UserLoginForm, ProductForm


class HomePage(ListView):
    template_name = 'users/index.html'
    model = Products
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prods = Products.objects.all().select_related('username').select_related('sub_category').select_related(
            'main_category')
        context['categories'] = prods.order_by('sub_category').values('sub_category__sub_category', 'sub_category').distinct()
        context['cities'] = prods.order_by('city').values('city', 'city').distinct()

        return context
    
    def get_queryset(self):
        products = Products.objects.all().order_by('created_at').select_related('username').select_related(
            'sub_category').select_related('main_category')[::-1][:200]
        return products


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # auto login after registration
            login(request, user)  # auto login after registration
            # form.save()
            messages.success(request, 'Account is created')
            return redirect('home')
        else:
            messages.error(request, 'Sorry, Please try again!')
    else:
        form = UserRegisterForm()
    return render(request, 'users/registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back! {request.user}')
            return redirect('home')
    else:
        form = UserLoginForm
    return render(request, 'users/login.html', {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You are Logged Out!')
    return redirect('home')


class PostProduct(CreateView):
    form_class = ProductForm
    template_name = 'users/post_product.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        product = self.object.product
        return reverse_lazy('home')


class ViewProduct(DetailView):
    model = Products
    template_name = 'users/view_product.html'
    context_object_name = 'item'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # saved all existed data
        return context

    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj


class PostDeleteView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Products
    template_name = 'users/delete_confirm.html'
    success_message = "Post is deleted"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.username:
            return True
        return False

    def get_success_url(self):
        user = self.object.username
        return reverse_lazy('home')