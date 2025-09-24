from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import get_user_model

from accounts.mixins import (
    LoginRequiredMixin
)

from .models import (
    Link
)

from .forms import (
    LinkFormCreation,LinkFormUpdate
)

User = get_user_model()

class MyPageView(LoginRequiredMixin,View):
    def get(self,request,slug):
        user = get_object_or_404(User, slug=slug)
        links = Link.objects.filter(user=user)
        context = {
            'links':links,
            'user':user
        }
        return render(request,'links/my_page.html',context=context)

class DashboardView(TemplateView):
    template_name = 'links/dashboard.html'

class LinkListView(LoginRequiredMixin,View):
    def get(self,request):
        links = Link.objects.filter(user=request.user)
        context = {
            'links':links
        }
        return render(request,'links/link_list.html',context=context)

class LinkCreateView(LoginRequiredMixin,View):
    def get(self,request):
        form = LinkFormCreation(user=request.user)
        context = {
            'form':form
        }
        return render(request,'links/link_create.html',context=context)
    
    def post(self,request):
        form = LinkFormCreation(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"This link successfully created.")
            return redirect('links:link_list')
        else:
            messages.error(request,"This data was invalid.")
            return render(request,'links/link_create.html',{'form':form})

class LinkUpdateView(LoginRequiredMixin,View):
    def get(self,request,pk):
        link = get_object_or_404(Link, id=pk, user=request.user)
        form = LinkFormUpdate(instance=link, user=request.user)
        context = {
            'form':form
        }
        return render(request,'links/link_update.html',context)
    
    def post(self,request,pk):
        link = get_object_or_404(Link, id=pk, user=request.user)
        form = LinkFormUpdate(request.POST, request.FILES, instance=link, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Link successfully updated.')
            return redirect('links:link_list')
        else:
            messages.error(request,'Link data was invalid.')
            return render(request,'links/link_update.html',{'form':form})
        