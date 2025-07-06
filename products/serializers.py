from rest_framework import serializers
from rest_framework.reverse import reverse
from django.forms.models import model_to_dict

from .models import Products
from . import validators
from api.serializers import UserPublicSerializer

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True) 
    my_discount = serializers.SerializerMethodField(read_only=True) 
    edit_url = serializers.SerializerMethodField(read_only=True) 
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk' 
    ) 
    # user_id_2 = serializers.SerializerMethodField(read_only=True)
    url_delete = serializers.HyperlinkedIdentityField(
        view_name='product-delete',
        lookup_field='pk'
    ) 
    # url_products = serializers.SerializerMethodField(read_only=True) 
    #email = serializers.EmailField(write_only=True)
    title = serializers.CharField(validators=[validators.validate_title])
    NAME = serializers.CharField(source='title', read_only=True)
    price = serializers.FloatField(validators=[validators.validate_price])
    # user_name = serializers.SerializerMethodField(read_only=True)
    class Meta: 
        model = Products
        fields = [
                #   'user_name',
                #   'user_id_2',
                  'owner',
                  #'email',
                  'NAME',
                  'url_delete',
                  'url',
                  'edit_url', 
                  'pk',
                  'title',
                  'content',
                  'price',
                  'sale_price',
                  'my_discount',
                  'public'
                  ]
        # read_only_fields = ['content', 'title']

    # def validate_title(self, value):
    #     query = Products.objects.filter(title__exact=value) # Here we just Form the query 
    #                                                         # to make this query to the database
    #     print(value, "IT IS VALUE")
    #     if query.exists(): # and here we exactly do the query and fin out if it exists
    #         raise serializers.ValidationError("'{value}' already exists.")
    #     return value

    def validate_content(self, value):
        if 'roman' in value:
            raise serializers.ValidationError("There is only 1 Roman!")
        req = self.context.get('request')
        return value
    
    # def get_user_name(self, obj):
    #     req = self.context.get('request') # u can also add request body checking 
    #     print(obj)
    #     name = req.user.username
    #     return name

    def create(self, validated_data):
        # email = validated_data.pop('email')
        obj = super().create(validated_data)
        #print(email, obj)
        return obj

    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('product-edit', kwargs={'pk': obj.pk}, request=request)
    
    # def get_user_id_2(self, obj):
    #     request = self.context.get('request')
    #     if request is None:
    #         return None
    #     return request.user.id*2  # it is the stupiest example but it showed u how method field works
                                # and why we define terms to check if request is None
    
    # def get_url_products(self, obj):
    #     request = self.context.get('request')
    #     print('REQUEST:', request)
    #     print('context:', self.context)
    #     if request is None:
    #         return None 
    #     return reverse('admin-panel')

    def get_my_discount(self, obj):
        if isinstance(obj, Products): #we may not call model instance when we call serializer method in views
            # just writing: serializer = ProductSerializer(data=req.data) and working with it 
            # this func requires instance of model and if we do not have it we write this.
            # but if we want to access this return we have to specify:
            #instance = serializer.save() in views after serializer = ProductSerializer(data=req.data) that call serializer instance
            return obj.get_discount()
        return None