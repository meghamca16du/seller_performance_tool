# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class BuyerDetails(models.Model):
    bid = models.TextField(primary_key=True)  # This field type is a guess.
    bname = models.TextField()

    class Meta:
        db_table = 'buyer_details'

class SellerDetails(models.Model):
    sid = models.TextField(primary_key=True)  # This field type is a guess.
    sname = models.TextField()

    class Meta:
        managed = True
        db_table = 'seller_details'

class ProductDetails(models.Model):
    pid = models.TextField(primary_key=True)  # This field type is a guess.
    pname = models.TextField()
    sid = models.TextField()  # This field type is a guess.

    class Meta:
        managed = True
        db_table = 'product_details'

class OrderDetails(models.Model):
    ontime_delivery='OD'   #creating data type enumeration for status
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
    oid = models.TextField(primary_key=True)  # This field type is a guess.
    pid = models.ForeignKey('ProductDetails', models.DO_NOTHING, db_column='pid')
    sid = models.ForeignKey('SellerDetails', models.DO_NOTHING, db_column='sid')
    bid = models.ForeignKey(BuyerDetails, models.DO_NOTHING, db_column='bid')
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

