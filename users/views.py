from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import User
from .forms import UserRegistrationForm, UserProfileForm


class RegisterView(CreateView):
    """
    User registration view
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        if user:
            login(self.request, user)
            messages.success(self.request, 'Registration successful! Welcome to Telegram Market Bot.')
        return response
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)


class LoginView(BaseLoginView):
    """
    User login view
    """
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)


class LogoutView(BaseLogoutView):
    """
    User logout view
    """
    next_page = reverse_lazy('core:home')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, UpdateView):
    """
    User profile edit view
    """
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    User dashboard with orders and downloads
    """
    template_name = 'users/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get user's orders
        context['orders'] = user.orders.select_related('template').order_by('-created_at')[:10]
        context['completed_orders'] = user.orders.filter(status='completed').count()
        context['total_spent'] = sum(
            order.amount for order in user.orders.filter(status='completed')
        )
        
        return context
