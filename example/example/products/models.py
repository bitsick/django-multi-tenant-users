from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    categories = models.ManyToManyField(
        'products.Category',
        verbose_name=_('categories'),
        related_name=_('products'),
    )

    def __str__(self):
        return '[{}] {} (${})'.format(
            ', '.join(c.name for c in self.categories.all()),
            self.name,
            self.price,
        )
