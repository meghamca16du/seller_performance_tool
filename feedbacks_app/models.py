from django.db import models
from dashboard.models import * 


class FeedbackDetails(models.Model):
    bid = models.ForeignKey('dashboard.BuyerDetails', on_delete = models.CASCADE, db_column='bid')
    oid = models.ForeignKey('dashboard.OrderDetails', on_delete = models.CASCADE, db_column='oid')
    pid = models.ForeignKey('dashboard.ProductDetails', on_delete = models.CASCADE, db_column='pid')
    feedbackEntered = models.TextField(max_length = 300)  
    dateFeedbackEntered = models.DateField()

    class Meta:
        managed = True
        db_table = 'feedback_details'