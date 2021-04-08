from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic import ListView, DetailView
from webapp.models import Category, Item
from accounts.models import Profile
from django.core.paginator import Paginator, PageNotAnInteger
from django.utils import timezone
from django.urls import reverse
import re
from django.db.models import Q
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
        context['new_items'] = Item.objects.all().order_by('-created')[:6]
        paginator = Paginator(items, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
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
    template_name = 'webapp/item_detail.html'

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


class Search(ListView):
    ''' Search items '''
    paginate_by = 9
    template_name = "webapp/search.html"

    def normalize_query(self, query_string,
                        findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                        normspace=re.compile(r'\s{2,}').sub):
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

    def get_query(self, query_string, search_fields):
        ''' Returns a query, that is a combination of Q objects. That combination
            aims to search keywords within a model by testing the given search fields.

        '''
        query = None  # Query to search for every search term
        terms = self.normalize_query(query_string)
        for term in terms:
            or_query = None  # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
        return query

    def get_queryset(self):
       if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']

            entry_query = self.get_query(
                query_string, ['name', 'description', ])

            found_entries = Item.objects.filter(
                entry_query).order_by('-created')

        return found_entries

    def get_context_data(self, *args, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        context['items'] = self.get_queryset()
        print(context)
        return context
