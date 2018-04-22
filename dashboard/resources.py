from import_export import resources
from .models import *

class ProductMainResource(resources.ModelResource):
    class meta:
        model = ProductMain
        exclude = ('id',)
        import_id_fields = ['pid',]

class CategoryResource(resources.ModelResource):
    class meta:
        model = Category

class SellerResource(resources.ModelResource):
    class meta:
        model = Seller

class BuyerResource(resources.ModelResource):
    class meta:
        model = Buyer

class CategoriesResource(resources.ModelResource):
    class meta:
        model = Categories

class SubcategoriesResource(resources.ModelResource):
    class meta:
        model = Subcategories

class ProductsResource(resources.ModelResource):
    class meta:
        model = Products

class OrdersResource(resources.ModelResource):
    class meta:
        model = Orders

