from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,authenticate,logout
from django.core.cache import cache
from django.contrib import messages
from django.views import View

from .forms import (
    RegisterForm,LoginForm,ProfileForm,PasswordResetRequestForm,PasswordResetConfirmForm
)
from .models import (
    CustomUser,ForgotPassword
)
from .mixins import (
    LoginRequiredMixin,LogoutRequiredMixin
)

class RegisterView(LogoutRequiredMixin,View):
    def get(self,request):
        form=RegisterForm()
        return render(request,'accounts/register.html',{'form':form})
    
    def post(self,request):
        form=RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Your registeration was successfully.')
            return redirect('accounts:login')
        else:
            messages.error(request,'Your registeration was faild.')
            return render(request,'accounts/register.html',{'form':form})

class LoginView(LogoutRequiredMixin,View):
    def get(self,request):
        form=LoginForm()
        return render(request,'accounts/login.html',{'form':form})

    def post(self,request):
        form=LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, 
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password']
            )

            if user:
                login(request,user)
                messages.success(request,'You successfully loged in')
                return redirect('/')
        else:
            messages.error(request,'Your password is incorrect')
            return render(request,'accounts/login.html',{'form':form})

class LogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,'Your successfully logout.')
        return render(request,'accounts/logout.html')

class PasswordResetRequestView(LogoutRequiredMixin,View):
    def get(self,request):
        form=PasswordResetRequestForm()
        return render(request,'accounts/password_reset_request.html',{'form':form})
    
    def post(self,request):
        form=PasswordResetRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Please check your email.')
            return render(request,'accounts/password_reset_message.html')
        else:
            messages.error(request,'your data was incorrect.')
            return render(request,'accounts/password_reset_request.html',{'form':form})

class PasswordResetConfirmView(LogoutRequiredMixin,View):
    def get(self,request,uuid):
        get_object_or_404(ForgotPassword,token=uuid)
        form=PasswordResetConfirmForm()
        return render(request,'accounts/password_reset_confirm.html',{'form':form,'uuid':uuid})
    
    def post(self,request,uuid):
        token=get_object_or_404(ForgotPassword,token=uuid)
        form=PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            form.save(token.user)
            messages.success(request,'Your password successfully changed.')
            return redirect('accounts:login')
        else:
            messages.error(request,'Your password was incorrect.')
            return render(request,'accounts/password_reset_confirm.html',{'form':form})

class ProfileView(LoginRequiredMixin,View):
    def get(self,request):
        cache_key = f"user_profile:{request.user.id}"

        user_data = cache.get(cache_key)
        if not user_data:
            user = request.user
            user_data = {
                'username': user.username,
                'email': user.email,
                'avatar': user.avatar.url if user.avatar else None
            }
            cache.set(cache_key, user_data, timeout=300)

        return render(request,'accounts/profile.html',{'user':user_data})
    
class ProfileUpdateView(LoginRequiredMixin,View):
    def get(self,request):
        user=get_object_or_404(CustomUser,username=request.user.username)
        form=ProfileForm(instance=user)
        return render(request,'accounts/profile_update.html',{'form':form})
    
    def post(self,request):
        user=get_object_or_404(CustomUser,username=request.user.username)
        form=ProfileForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            self.delete_cache_data(request.user.id)
            messages.success(request,"Your profile successfully updated.")
            return redirect('accounts:profile')
        else:
            messages.error(request,'Your data was incorrect.')
            return render(request,'accounts/profile_update.html',{'form':form})
    
    def delete_cache_data(self,user_id):
        cache_key = f"user_profile:{user_id}"
        cache.delete(cache_key)