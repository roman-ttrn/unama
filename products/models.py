from django.db import models
from django.conf import settings
from django.db.models import Q

User = settings.AUTH_USER_MODEL # auth.User



class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)
    
    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query) # i. e. in their fields they have or title=query or content=query
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs = qs.filter(user=user)
        return qs

class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().is_public().search(query, user=user)
    


class Products(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL) # blank=false
                                                                                # without addditional logic it just add first user (default=1)
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15,
                                decimal_places=2, default=99.99)
    public = models.BooleanField(default=True)

    objects = ProductManager() 
    @property
    def sale_price(self):
        return "%.2f%%" %(float(self.price) * 0.8)
    
    # we can just define method that returns required value 
    def get_discount(self):
        return '122'