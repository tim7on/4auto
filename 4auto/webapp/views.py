import re
import mptt
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, FormView, UpdateView
from webapp.models import Category, Item
from webapp.forms import ItemForm
from accounts.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, PageNotAnInteger
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from django.http import JsonResponse


class IndexView(ListView):
    '''
    HomePage of website
    '''
    model = Item
    template_name = 'webapp/index.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = Item.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['new_items'] = Item.objects.all().order_by('-updated')[:8]
        context['paid_items'] = Item.objects.filter(
            owner__profile__expired__gte=timezone.now()).order_by('-updated')[:8]
        return context


class AllCategory(ListView):
    '''
    Catregory: 'All' of website
    '''

    model = Item
    template_name = 'webapp/category.html'
    paginate_by = 6
    context_object_name = 'items'

    def get_queryset(self):
        queryset = Item.objects.all().order_by('-updated')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllCategory, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
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
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['items'] = self.get_queryset().order_by('-updated')
        context['category'] = Category.objects.all()

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
            id=self.kwargs['pk']).order_by('-updated')[:3]
        return context

    def get_object(self, queryset=None):
        item = super().get_object(queryset)
        item.viewed = item.viewed + 1
        item.save()
        return item


class ProfileDetailView(ListView):
    model = Item
    template_name = "webapp/profile.html"
    paginate_by = 6

    def get_queryset(self):
        queryset = Item.objects.filter(owner__username=self.kwargs['username'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(
            user__username=self.kwargs.get("username"))
        context['items'] = self.get_queryset().order_by('-updated')
        return context


class ItemCreateView(LoginRequiredMixin, FormView):
    template_name = 'webapp/item_create.html'
    form_class = ItemForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.updated = timezone.now()
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user.username})


class ItemUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'webapp/item_create.html'
    model = Item
    form_class = ItemForm

    def test_func(self):
        return self.request.user == self.get_object().owner

    def post(self, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            self.object = self.get_object()
            form = self.get_form(self.request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return HttpResponseRedirect(self.get_success_url())

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user.username})

    def get_form(self, *args, **kwargs):
        form_kwargs = {'instance': self.object}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ItemForm(**form_kwargs)


class ItemUpUpdateView(UserPassesTestMixin, UpdateView):
    '''Update time of item to Up'''
    model = Item

    def test_func(self):
        return self.request.user == self.get_object().owner

    def post(self, *args, **kwargs):
        profile = Profile.objects.get(user__username=self.get_object().owner)
        if profile.up_counter < 5:
            self.object = self.get_object()
            self.object.updated = timezone.now()
            self.object.save()
            profile.up_counter = profile.up_counter + 1
            profile.save()
            print(profile.up_counter)
        data = {'success': 'OK'}
        return JsonResponse(data)


class ItemDeleteView(UserPassesTestMixin, DeleteView):
    model = Item

    def test_func(self):
        return self.request.user == self.get_object().owner

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        data = {'success': 'OK'}
        return JsonResponse(data)


class Search(ListView):
    ''' Search items '''
    paginate_by = 6
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
                entry_query).order_by('-updated')
        else:
            found_entries = Item.objects.none()
        return found_entries

    def get_context_data(self, *args, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['q'] = f'&q={self.request.GET.get("q")}'
        return context
