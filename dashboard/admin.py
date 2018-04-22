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
#admin.site.register(TraitValueDetails)

#new code
@admin.register(Seller)
class SellerAdmin(ImportExportModelAdmin):
    pass

@admin.register(Buyer)
class BuyerAdmin(ImportExportModelAdmin):
    pass

@admin.register(Categories)
class CategoriesAdmin(ImportExportModelAdmin):
    pass

@admin.register(Subcategories)
class SubcategoriesAdmin(ImportExportModelAdmin):
    pass

@admin.register(Products)
class ProductsAdmin(ImportExportModelAdmin):
    pass

@admin.register(Orders)
class OrdersAdmin(ImportExportModelAdmin):
    pass

@admin.register(Hits)
class HitsAdmin(ImportExportModelAdmin):
    pass
