from django.db import models
from dashboard.models import * 
from dashboard.models import ProductMain
from dashboard.models import Products
from .search import Feedbacks_Index

'''class FeedbackDetails(models.Model):
    fid = models.AutoField(primary_key = True, null = False)
    bid = models.ForeignKey('dashboard.BuyerDetails', on_delete = models.CASCADE, db_column='bid')
    oid = models.ForeignKey('dashboard.OrderDetails', on_delete = models.CASCADE, db_column='oid')
    pid = models.ForeignKey('dashboard.ProductDetails', on_delete = models.CASCADE, db_column='pid')
    feedbackEntered = models.TextField(max_length = 300) 
    default = '0'
    oneStar= '1'   
    twoStar= '2'
    threeStar= '3'
    fourStar = '4'
    fiveStar = '5'
    Rating_types=(
        (default, 'default'),
        (oneStar,'oneStar'),
        (twoStar,'twoStar'),
        (threeStar,'threeStar'),
        (fourStar,'fourStar'),
        (fiveStar,'fiveStar'),
        )
    feedbackRating = models.CharField(
        max_length = 1,
        choices = Rating_types,
        default = default,
        )
    dateFeedbackEntered = models.DateField()

    class Meta:
        managed = True
        db_table = 'feedback_details'

class Feedbacks_table(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    pid_seller = models.ForeignKey('dashboard.ProductMain', on_delete = models.CASCADE)
    feedbackdate = models.DateField()
    rating_points = models.IntegerField()
    feedback_entered = models.TextField(max_length=500)

    def indexing(self):
        obj = Feedbacks_Index(
                meta={'id' : self.id},
                id = self.id,
                pid_seller = self.pid_seller.id,
                feedbackdate=self.feedbackdate,
                rating_points = self.rating_points,
                feedback_entered= self.feedback_entered
                )
        obj.save()
        return obj.to_dict(include_meta=True)'''

class Feedbacks(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    product_id = models.ForeignKey('dashboard.Products', on_delete = models.CASCADE)
    feedback_date = models.DateField()
    rating = models.IntegerField()
    feedback = models.TextField(max_length=500)

    def indexing(self):
        obj = Feedbacks_Index(
                meta={'id' : self.id},
                id = self.id,
                product_id = self.product_id.id,
                feedback_date=self.feedback_date,
                rating = self.rating,
                feedback= self.feedback
                )
        obj.save()
        return obj.to_dict(include_meta=True)
