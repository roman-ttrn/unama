from rest_framework import serializers

class UserProductInlineSerializer(serializers.Serializer): 
    title = serializers.CharField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product-detail')

class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    other_products = serializers.SerializerMethodField(read_only=True)

    def get_other_products(self, obj):
        user = obj
        qs = user.products_set.all()[:3]
        return UserProductInlineSerializer(qs, many=True, context=self.context).data