from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse


class Category(MPTTModel):
    name = models.CharField(verbose_name=_("Название"),
                            max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey('self', verbose_name=_("Родитель"), on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    def get_absolute_url(self):
        if self.parent_id:
            return reverse(
                'subcategory',
                kwargs={'category': self.parent.slug,
                        'subcategory': self.slug}
            )
        else:
            return reverse('category', kwargs={'subcategory': self.slug})

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Item(models.Model):
    owner = models.ForeignKey(get_user_model(), verbose_name=_(
        "Владелец"), on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_("Название"), max_length=50)
    category = models.ForeignKey(
        "webapp.Category", verbose_name=_("Категории"), on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name=_(
        "Фото"), upload_to="items_photo", null=True, blank=True)

    description = models.TextField(verbose_name=_("Описание"))
    price = models.DecimalField(verbose_name=_(
        'Цена'), max_digits=9, decimal_places=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товар'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item_view', kwargs={'owner': self.owner, 'pk': self.pk})
