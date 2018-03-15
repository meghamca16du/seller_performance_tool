from django.contrib import admin
from .models import BuyerDetails, OrderDetails, ProductDetails, SellerDetails
# Register your models here.

admin.site.register(BuyerDetails)
admin.site.register(OrderDetails)
admin.site.register(ProductDetails)
admin.site.register(SellerDetails)

