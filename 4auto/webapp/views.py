from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic import ListView, DetailView
from webapp.models import Category, Item
from accounts.models import Profile
from django.core.paginator import Paginator, PageNotAnInteger
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
import mptt


class IndexView(ListView):
    '''
    HomePage of website
    '''

    model = Item
    template_name = 'webapp/index.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = Item.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        items = self.get_queryset()
        paginator = Paginator(items, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context = {'items': items,
                   'category': Category.objects.all()
                   }
        return context


class AllCategory(ListView):
    '''
    Catregory: 'All' of website
    '''

    model = Item
    template_name = 'webapp/category.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = Item.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllCategory, self).get_context_data(**kwargs)
        items = self.get_queryset().order_by('-created')
        paginator = Paginator(items, self.paginate_by)

        page = self.request.GET.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context = {'items': items,
                   'category': Category.objects.all()
                   }
        return context


class CategoryListView(ListView):
    '''
    Category views, with request filtration
    '''
    model = Item
    template_name = 'webapp/category.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = Item.objects.filter(Q(category__slug=self.kwargs.get(
            'subcategory')) | Q(category__parent__slug=self.kwargs.get('subcategory')))
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        items = self.get_queryset().order_by('-created')
        paginator = Paginator(items, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context = {'items': items,
                   'category': Category.objects.all()
                   }
        return context


class ItemDetailView(DetailView):
    ''' DetailView of Item '''
    model = Item
    template_name = "webapp/item_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(
            user__username=self.kwargs['owner'])
        context['new_items'] = Item.objects.exclude(
            id=self.kwargs['pk']).order_by('-created')[:3]
        return context


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "webapp/profile.html"

    def get_object(self, queryset=None):
        return Profile.objects.get(user__username=self.kwargs.get("username"))

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['items'] = Item.objects.filter(
            owner__username=self.kwargs['username'])
        return context
