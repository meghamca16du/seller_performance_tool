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