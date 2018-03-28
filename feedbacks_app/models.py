from django.db import models
from dashboard.models import * 


class FeedbackDetails(models.Model):
    bid = models.ForeignKey('dashboard.BuyerDetails', on_delete = models.CASCADE, db_column='bid')
    oid = models.ForeignKey('dashboard.OrderDetails', on_delete = models.CASCADE, db_column='oid')
    pid = models.ForeignKey('dashboard.ProductDetails', on_delete = models.CASCADE, db_column='pid')
    feedbackEntered = models.TextField(max_length = 300) 
    default = 0
    oneStar= 1   
    twoStar= 2
    threeStar= 3
    fourStar = 4
    fiveStar = 5
    Rating_types=(
        (default, 'default'),
        (oneStar,'oneStar'),
        (twoStar,'twoStar'),
        (threeStar,'threeStar'),
        (fourStar,'fourStar'),
        (fiveStar,'fiveStar'),
        )
    feedbackRating = models.IntegerField(
        choices = Rating_types,
        default = default,
        )
    dateFeedbackEntered = models.DateField()

    class Meta:
        managed = True
        db_table = 'feedback_details'