from django.urls import reverse
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.conf import settings

from accounts.mixins import (
    LoginRequiredMixin
)

from .models import (
    Link,PageView
)

from .forms import (
    LinkCreationForm,LinkUpdateForm
)

User = get_user_model()

class MyPageView(View):
    def get(self,request,slug):
        user = get_object_or_404(User, slug=slug)
        self.create_page_view(request,user)
        links = Link.objects.filter(user=user, status=Link.LinkStatus.enable)
        context = {
            'links':links,
            'user':user
        }
        return render(request,'links/my_page.html',context=context)
    
    def create_page_view(self,request,user):
        path = reverse('links:my-page', args=[user.slug])
        ip, user_agent = self.get_client_data(request)

        PageView.objects.get_or_create(
            user=user,
            path=path,
            ip_address=ip,
            user_agent=user_agent
        )

    def get_client_data(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        return ip, user_agent

class DashboardView(LoginRequiredMixin,View):
    def get(self,request):
        user = get_object_or_404(User, username=request.user.username)
        active_links = Link.objects.filter(user=user, status="Enable").count()
        path,full_link = self.get_link_my_page(user.slug)
        total_views = PageView.objects.filter(path=path).count()
        context = {
            'active_links':active_links,
            'total_views':total_views,
            'my_link':full_link
        }
        return render(request,'links/dashboard.html',context=context)

    def get_link_my_page(self,slug):
        path = reverse('links:my-page', args=[slug])
        full_link = f"{settings.SITE_DOMAIN}{path}"
        return path,full_link

class LinkListView(LoginRequiredMixin,View):
    def get(self,request):
        links = Link.objects.filter(user=request.user)
        context = {
            'links':links
        }
        return render(request,'links/link_list.html',context=context)

class LinkDetailView(LoginRequiredMixin,View):
    def get(self,request,pk):
        link = get_object_or_404(Link, id=pk, user=request.user)
        context = {
            'link':link
        }
        return render(request,'links/link_detail.html',context=context)

class LinkCreateView(LoginRequiredMixin,View):
    def get(self,request):
        form = LinkCreationForm(user=request.user)
        context = {
            'form':form
        }
        return render(request,'links/link_create.html',context=context)
    
    def post(self,request):
        form = LinkCreationForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"This link successfully created.")
            return redirect('links:link-list')
        else:
            messages.error(request,"This data was invalid.")
            return render(request,'links/link_create.html',{'form':form})

class LinkUpdateView(LoginRequiredMixin,View):
    def get(self,request,pk):
        link = get_object_or_404(Link, id=pk, user=request.user)
        form = LinkUpdateForm(instance=link, user=request.user)
        context = {
            'form':form
        }
        return render(request,'links/link_update.html',context)
    
    def post(self,request,pk):
        link = get_object_or_404(Link, id=pk, user=request.user)
        form = LinkUpdateForm(request.POST, request.FILES, instance=link, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Link successfully updated.')
            return redirect('links:link-list')
        else:
            messages.error(request,'Link data was invalid.')
            return render(request,'links/link_update.html',{'form':form})
        
class LinkDeleteView(LoginRequiredMixin,View):
    def get(self,request,pk):
        link = get_object_or_404(Link, id=pk, user=request.user)
        link.delete()
        messages.success(request,"This link successfully deleted.")
        return redirect('links:link-list')