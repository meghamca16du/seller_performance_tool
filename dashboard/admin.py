from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

@admin.register(ProductMain)
class ProductMainAdmin(ImportExportModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    pass

admin.site.register(BuyerDetails)
admin.site.register(OrderDetails)
admin.site.register(ProductDetails)
admin.site.register(SellerDetails)
admin.site.register(TraitValueDetails)

