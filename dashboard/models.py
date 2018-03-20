# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class BuyerDetails(models.Model):
    bid = models.TextField(primary_key=True)  
    bname = models.TextField()

    class Meta:
        db_table = 'buyer_details'

class SellerDetails(models.Model):
    sid = models.TextField(primary_key=True) 
    sname = models.TextField()

    class Meta:
        managed = True
        db_table = 'seller_details'

class ProductDetails(models.Model):
    pid = models.TextField(primary_key=True)  
    pname = models.TextField()
    sid = models.ForeignKey('SellerDetails', on_delete = models.CASCADE, db_column='sid')

    class Meta:
        managed = True
        db_table = 'product_details'

class OrderDetails(models.Model):
    ontime_delivery='OD'   
    late_delivery='LD'
    returned='R'
    cancelled='C'
    in_process='IP'
    dispatched='D'
    status_types=(
        (ontime_delivery,'ontime_delivery'),
        (late_delivery,'late_delivery'),
        (cancelled,'cancelled'),
        (returned,'returned'),
        (in_process,'in_process'),
        (dispatched,'dispatched'),
     )
    tid = models.AutoField(
        primary_key=True,
        null = False,
    )
    oid = models.TextField() 
    pid = models.ForeignKey('ProductDetails', on_delete = models.CASCADE, db_column='pid')
    sid = models.ForeignKey('SellerDetails', on_delete = models.CASCADE, db_column='sid')
    bid = models.ForeignKey('BuyerDetails', on_delete = models.CASCADE, db_column='bid')
    exp_shipment = models.DateField()
    exp_delivery = models.DateField()
    actual_shipment = models.DateField(blank=True,null=True)
    actual_delivery = models.DateField(blank=True,null=True)
    status = models.CharField(
        max_length = 2,
        choices = status_types,
        default = in_process,
    )  # This field type is enumeration.

    class Meta:
        managed = True
        db_table = 'order_details'
        unique_together = (('oid', 'pid', 'sid', 'bid'),)

class TraitValueDetails(models.Model):
   # ttid = models.AutoField(primary_key=True,null = False)
    sid = models.OneToOneField('SellerDetails',primary_key=True, on_delete = models.CASCADE, db_column='sid')
   # sid = models.ForeignKey('SellerDetails', on_delete = models.CASCADE, db_column='sid',unique = True)
    late_shipment_rate = models.DecimalField(max_digits=4,decimal_places=2,default=0)
    on_time_delivery = models.DecimalField(max_digits=4,decimal_places=2,default=0)
    hit_to_success_ratio = models.DecimalField(max_digits=4,decimal_places=2,default=0)
    return_rate = models.DecimalField(max_digits=4,decimal_places=2,default=0)
    
    class Meta:
        managed = True
        db_table = 'traits_value_details'