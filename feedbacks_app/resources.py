from import_export import resources
from .models import *

class FeedbacksResource(resources.ModelResource):
    class meta:
        model = Feedbacks_table

class FeedbackResource(resources.ModelResource):
    class meta:
        model = Feedbacks