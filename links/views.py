from user_agents import parse

from django.urls import reverse
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.cache import cache

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
        ip, device_type = self.get_client_data(request)

        PageView.objects.get_or_create(
            user=user,
            path=path,
            ip_address=ip,
            user_agent=device_type
        )

    def get_client_data(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_string)

        if user_agent.is_mobile:
            device_type = 'Mobile'
        elif user_agent.is_pc:
            device_type = 'PC'
        elif user_agent.is_tablet:
            device_type = 'Tablet'
        else:
            device_type = 'Other'

        return ip, device_type

class DashboardView(LoginRequiredMixin,View):
    def get(self,request):
        user = get_object_or_404(User, username=request.user.username)
        path,full_link = self.get_link_my_page(user.slug)
        context = {
            'active_links':self.get_active_link_and_cache(user)['active_links'],
            'total_views':self.get_views_and_cache(path)['total_views'],
            'my_link':full_link
        }
        return render(request,'links/dashboard.html',context=context)

    def get_link_my_page(self,slug):
        path = reverse('links:my-page', args=[slug])
        full_link = f"{settings.SITE_DOMAIN}{path}"
        return path,full_link

    def get_views_and_cache(self, path):
        cache_key = f'views:{path}'
        context = cache.get(cache_key)
        if not context:
            total_views = PageView.objects.filter(path=path).count()
            context = {'total_views': total_views}
            cache.set(cache_key, context, timeout=60)
        return context

    def get_active_link_and_cache(self,user):
        cache_key = f'active_links:{user.username}'

        context = cache.get(cache_key)
        if not context:
            active_links = Link.objects.filter(user=user, status=Link.LinkStatus.enable).count()
            context = {
                'active_links':active_links
            }
            cache.set(cache_key, context, timeout=60)
        return context

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
            self.delete_cache(request.user)
            messages.success(request,"This link successfully created.")
            return redirect('links:link-list')
        else:
            messages.error(request,"This data was invalid.")
            return render(request,'links/link_create.html',{'form':form})
    
    def delete_cache(self,user):
        cache_key = f'active_links:{user.username}'
        cache.delete(cache_key)

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
            self.delete_cache(request.user)
            messages.success(request,'Link successfully updated.')
            return redirect('links:link-detail', form.instance.pk)
        else:
            messages.error(request,'Link data was invalid.')
            return render(request,'links/link_update.html',{'form':form})
    
    def delete_cache(self,user):
        cache_key = f'active_links:{user.username}'
        cache.delete(cache_key)
        
class LinkDeleteView(LoginRequiredMixin,View):
    def post(self,request,pk):
        link = get_object_or_404(Link, id=pk, user=request.user)
        link.delete()
        self.delete_cache(request.user)
        messages.success(request,"This link successfully deleted.")
        return redirect('links:link-list')
    
    def delete_cache(self,user):
        cache_key = f'active_links:{user.username}'
        cache.delete(cache_key)