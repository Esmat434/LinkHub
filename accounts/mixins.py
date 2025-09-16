from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages

class LogoutRequiredMixin(AccessMixin):
    def dispatch(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request,"You must be logout.")
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

class LoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"You must be login.")
            return redirect('accounts:login')
        return super().dispatch(request,*args,**kwargs)