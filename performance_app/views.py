from django.shortcuts import render
from dashboard.models import *
from django.db.models import Count, F, Sum
from abc import ABC, abstractmethod
import re
from datetime import datetime
from django.utils import formats
from .feedbacks import polarity
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from feedbacks_app.models import *
from django.contrib.auth.models import User
import json
import pickle

class Trait(ABC):
    '''
        Objective: An abstract class which calculates the value of the trait and stores it in the database.
    ''' 
    def __init__(self, trait_cmp,from_date,to_date,current_sellerid):
        '''
        Objective: A constructor which initializes the trait component variable.
        Input Parameter: trait_cmp - Trait Component
        Return Value: Returns an object of the called class
        '''
        self.trait_component = trait_cmp
        self.from_date = from_date
        self.to_date = to_date
        self.current_sellerid = current_sellerid

    def template_method(self, trait_name, trait_value, recommendation_list,traitWeightageList, IsDateEnteredByUser):
        '''
        Objective: Template method defines an algorithm's skeleton in the Trait base class 
                    and let subclasses redefine certain steps of the algorithm.
        Input Parameter: trait_list - A list of Traits
                         value_list - A list of Values of the corresponding traits defined in the trait_list
        '''
        table_name = self.find_table()
        self.store_sid(table_name)
        value = self.calc_value()
        traitWeightage = self.returnTraitWeightage()
        traitWeightageList.append(traitWeightage)
        self.saveRecommendation(value, recommendation_list,IsDateEnteredByUser)
        self.store_value(value, table_name, trait_name, trait_value,IsDateEnteredByUser)

    def find_table(self):
        '''
        Objective: To find the database table which contains the trait_component field .
        Return Value: Returns the database table name
        '''
        for cls in Base_TraitValueDetails.__subclasses__():
            field=cls._meta.get_field(self.trait_component)
            if field:
                return cls

    def store_sid(self,table_name):
        '''
        Objective: To check and then store the sid of seller in the table_name which contains trait_component.
        Input Parameter: table_name - Table which contains trait_component
        ''' 
        check=table_name.objects.filter(sid=self.current_sellerid).exists()
        if check==False:
            s=Seller.objects.get(id=self.current_sellerid)
            save_sid=table_name(sid=s)
            save_sid.save()

    @abstractmethod
    def calc_value(self):
        '''
        Objective: An abstract method which calculates the value of trait_component.
        Return Value: Calculated Value of the trait.
        '''
        pass

    def store_value(self,value,table_name,trait_name, trait_value,IsDateEnteredByUser):
        '''
        Objective: To store or update the value of the trait component in the database table.
        Input Parameter: value - Calculated value of the trait component
                         table_name - Database table in which the value is to be inserted/updated
                         trait_list - A list of Traits
                         value_list - A list of Values of the corresponding traits defined in the trait_list
        '''
        if (IsDateEnteredByUser == False):
            trait_obj = table_name.objects.filter(sid=self.current_sellerid).update(**{self.trait_component:value})
        trait_name.append(self.trait_component)
        trait_value.append(value)
        return value

    def calc_overall_performance(self,trait_value, traitWeightageList,IsDateEnteredByUser):
        '''
        Objective: To calculate the overall performance of the seller.
        Input Parameter: value_list - A list of Values of the corresponding traits defined in the trait_list
        Return Value: overall_perf_val - Overall performance value of the seller
        '''
        if (IsDateEnteredByUser == False):
            numerator = [trait_value[i]*traitWeightageList[i] for i in range(len(trait_value))]
            overall_perf_value = sum(numerator) / sum(traitWeightageList)
            self.store_overall_value(TraitValueDetails,overall_perf_value)

    def store_overall_value(self,TraitValueDetails ,overall_perf_value):
        '''
        Objective: To store or update the overall performance of the seller.
        Input Paramter: tabel_name - Database table in which the value is to be inserted/updated
                        overall_performance - Overall performance value of the seller
        '''
        TraitValueDetails.objects.filter(
                    sid=self.current_sellerid
                    ).update(
                    overall_perf_val = overall_perf_value
                    )
            

class LateShipmentRate(Trait):
    '''
    Objective: A derived class of Trait which calculates the value of 'late shipment rate' trait
    '''
    def calc_value(self):
        '''
        Objective: Calculates the values of late_shipment_rate.
        Return Value: late_perc - Percentage of the late shipment done by the seller.
        '''
        LateOrders = Orders.objects.all().filter(
                         seller_id=self.current_sellerid
                         ).filter(
                         actual_shipment__isnull=False
                         ).filter(
                         actual_shipment__gt = F('exp_shipment')
                         ).filter(
                         order_date__gte = self.from_date
                         ).filter(
                         order_date__lte = self.to_date
                         ).count()
        Total = Orders.objects.filter(
                    seller_id=self.current_sellerid
                    ).filter(
                    order_date__gte=self.from_date
                    ).filter(
                    order_date__lte=self.to_date
                    ).filter(
                    actual_shipment__isnull=False).count()
        late_perc = round((LateOrders/Total)*100, 2)
        return late_perc
    
    def returnTraitWeightage(self):
        return -1

    def saveRecommendation(self, value, recommendation_list, IsDateEnteredByUser):
        if value <= 30:
            recommendation_list.append("Use company’s shipping services for shipment of products on time for better customer experience.")
            if (IsDateEnteredByUser == False):
                TraitValueDetails.objects.filter(
                    sid=self.current_sellerid
                    ).update(
                    recommendations_lateShipmentRate = "Use company’s shipping services for shipment of products on time for better customer experience "
                    )            
        elif value > 30 and value <= 70:
            if (IsDateEnteredByUser == False):
                TraitValueDetails.objects.filter(
                    sid = self.current_sellerid
                    ).update(
                    recommendations_lateShipmentRate = "Review your order fulfillment processes to identify and resolve any deficiencies that can result in late shipments."   
                    )
            recommendation_list.append("Review your order fulfillment processes to identify and resolve any deficiencies that can result in late shipments.")
            
        else:
            if (IsDateEnteredByUser == False):
                TraitValueDetails.objects.filter(
                    sid = self.current_sellerid
                    ).update(
                    recommendations_lateShipmentRate = "recommendation 3"   
                    )
            recommendation_list.append("recommendation 3")
            

class OnTimeDelivery(Trait):
    '''
    Objective: A derived class of Trait which calculates the value of 'On time Delivery' trait
    '''
    def calc_value(self):
        '''
        Objective: Calculates the values of on_time_delivery.
        Return Value: late_perc - Percentage of the on time delivery done by the seller.
        '''
        onTimeDeliver = Orders.objects.all().filter(
                            seller_id=self.current_sellerid
                            ).filter(
                            actual_delivery__isnull=False
                            ).filter(
                            exp_delivery__gte = F('actual_delivery')
                            ).filter(
                            order_date__gte=self.from_date
                            ).filter(
                            order_date__lte=self.to_date
                            ).count(
                            )
        totalDeliver = Orders.objects.filter(
                            seller_id=self.current_sellerid
                            ).filter(
                            actual_delivery__isnull=False
                            ).filter(
                            order_date__gte=self.from_date
                            ).filter(
                            order_date__lte=self.to_date
                            ).count()
        Percentage =round((onTimeDeliver/totalDeliver)*100, 2)
        return Percentage

    def returnTraitWeightage(self):
        return 2

    def saveRecommendation(self, value,recommendation_list, IsDateEnteredByUser ):
        if value <= 30:
            if (IsDateEnteredByUser == False):
                TraitValueDetails.objects.filter(
                    sid=self.current_sellerid
                    ).update(
                    recommendations_onTimeDeliery = "Use company’s delivery services for shipment of products on time for better customer experience."
                    )
            recommendation_list.append("Use company’s delivery services for shipment of products on time for better customer experience.")
            
        elif value > 30 and value <= 70:
            if (IsDateEnteredByUser == False):
                TraitValueDetails.objects.filter(
                    sid = self.current_sellerid
                    ).update(
                    recommendations_onTimeDeliery = "Be proactive in resolving any delivery problems related to the delivery method you use."   
                    )
            recommendation_list.append("Be proactive in resolving any delivery problems related to the delivery method you use.")
        else:
            if (IsDateEnteredByUser == False):
                TraitValueDetails.objects.filter(
                    sid = self.current_sellerid
                    ).update(
                    recommendations_onTimeDeliery = "You may also send order tracking information for better customer experience."   
                    )
            recommendation_list.append("You may also send order tracking information for better customer experience.")

class HitToSuccessRatio(Trait): 
    '''
    Objective: A derived class of Trait which calculates the value of 'Hit to Success Ratio' trait
    '''
    def calc_value(self):
        '''
        Objective: Calculates the values of hit_to_success_ratio.
        Return Value: late_perc - Percentage of the successes.
        '''
        success=Orders.objects.filter(
                    seller_id=self.current_sellerid
                    ).filter(
                    order_date__gte=self.from_date
                    ).filter(
                    order_date__lte=self.to_date
                    ).count()
        hits = Hits.objects.all().filter(
                pid__sid=self.current_sellerid
                ).filter(
                hit_date__gte=self.from_date
                ).filter(
                hit_date__lte=self.to_date
                ).aggregate(Sum('hits'))['hits__sum']
        success_perc = round((success/hits)*100, 2)
        return success_perc

    def returnTraitWeightage(self):
        return 1.5

    def saveRecommendation(self, value, recommendation_list, IsDateEnteredByUser):
        if value <= 30:
            if (IsDateEnteredByUser == False):
                TraitValueDetails.objects.filter(
                    sid=self.current_sellerid
                    ).update(
                    recommendations_HitToSucessRatio = "Provide accurate product descriptions and include images with your listings."
                    )
            recommendation_list.append("Provide accurate product descriptions and include images with your listings.")
        elif value > 30 and value <= 70:
            if (IsDateEnteredByUser == False):
                TraitValueDetails.objects.filter(
                    sid = self.current_sellerid
                    ).update(
                    recommendations_HitToSucessRatio = "recommendation 2"   
                    )
            recommendation_list.append("recommendation 2")
        else:
            if (IsDateEnteredByUser == False):
                TraitValueDetails.objects.filter(
                    sid = self.current_sellerid
                    ).update(
                    recommendations_HitToSucessRatio = "recommendation 3"   
                    )
            recommendation_list.append("recommendation 3")

class ReturnRate(Trait):
    '''
    Objective: A derived class of Trait which calculates the value of 'ReturnRate' trait
    '''
    def calc_value(self):
        '''
        Objective: Calculates the values of return rate ratio.
        '''
        returnCount = Orders.objects.filter(
                            seller_id=self.current_sellerid
                            ).filter(
                            status = 'R'
                            ).filter(
                            order_date__gte=self.from_date
                            ).filter(
                            order_date__lte=self.to_date
                            ).count(       
                            )
        totalOrders = Orders.objects.filter(
                            seller_id=self.current_sellerid
                            ).filter(
                            order_date__gte=self.from_date
                            ).filter(
                            order_date__lte=self.to_date
                            ).count(       
                            )
        return_rate = round((returnCount/totalOrders)*100, 2)
        return return_rate

    def returnTraitWeightage(self):
        return -1.25

    def saveRecommendation(self, value, recommendation_list, IsDateEnteredByUser):
        if value <= 30:
            if (IsDateEnteredByUser == False):
                TraitValueDetails.objects.filter(
                    sid=self.current_sellerid
                    ).update(
                    recommendations_returnRate = "Package all items carefully. Use a trustworthy courier to make sure that they arrive at their destination safely and in a timely manner."
                    )
            recommendation_list.append("Package all items carefully. Use a trustworthy courier to make sure that they arrive at their destination safely and in a timely manner.")
        elif value > 30 and value <= 70:
            if (IsDateEnteredByUser == False):
                TraitValueDetails.objects.filter(
                    sid = self.current_sellerid
                    ).update(
                    recommendations_returnRate = "Make sure that all listings and images are completely accurate."   
                    )
            recommendation_list.append("Make sure that all listings and images are completely accurate.")
        else:
            if (IsDateEnteredByUser == False):
                TraitValueDetails.objects.filter(
                    sid = self.current_sellerid
                    ).update(
                    recommendations_returnRate = "recommendation 3"   
                    )
            recommendation_list.append("recommendation 3")

class PositiveFeedbacks(Trait):

    def calc_value(self):
        polar=polarity()
        positive_score=polar.calc_positive_feedbacks(self.from_date,self.to_date,self.current_sellerid)
        return positive_score

    def returnTraitWeightage(self):
        return 2

    def saveRecommendation(self,value,recommendation_list,IsDateEnteredByUser):
        if value <= 30:
            if IsDateEnteredByUser == False:
                TraitValueDetails.objects.filter(
                    sid=self.current_sellerid
                    ).update(
                    recommendations_positive_feedbacks = "recommendation 1"
                    )
            recommendation_list.append("recommendation 1")
        elif value > 30 and value <= 70:
            if IsDateEnteredByUser == False:
                TraitValueDetails.objects.filter(
                    sid =self.current_sellerid
                    ).update(
                    recommendations_positive_feedbacks = "recommendation 2"   
                    )
            recommendation_list.append("recommendation 2")
        else:
            if IsDateEnteredByUser == False:
                TraitValueDetails.objects.filter(
                    sid = self.current_sellerid
                    ).update(
                    recommendations_positive_feedbacks = "recommendation 3"   
                    )
            recommendation_list.append("recommendation 3")

class NegativeFeedbacks(Trait):

    def calc_value(self):
        polar=polarity()
        negative_score=polar.calc_negative_feedbacks(self.from_date,self.to_date,self.current_sellerid)
        return negative_score

    def returnTraitWeightage(self):
        return -1

    def saveRecommendation(self,value,recommendation_list,IsDateEnteredByUser):
        if value <= 30:
            if IsDateEnteredByUser == False:
                TraitValueDetails.objects.filter(
                    sid=self.current_sellerid
                    ).update(
                    recommendations_negative_feedbacks = "recommendation 1"
                    )
            recommendation_list.append("recommendation 1")
        elif value > 30 and value <= 70:
            if IsDateEnteredByUser == False:
                TraitValueDetails.objects.filter(
                    sid =self.current_sellerid
                    ).update(
                    recommendations_negative_feedbacks ="Provide accurate product descriptions and include images with your listings."   
                    )
            recommendation_list.append("Provide accurate product descriptions and include images with your listings.")
        else:
            if IsDateEnteredByUser == False:
                TraitValueDetails.objects.filter(
                    sid = self.current_sellerid
                    ).update(
                    recommendations_negative_feedbacks = "recommendation 3"   
                    )
            recommendation_list.append("recommendation 3")


#for runtime
'''class CancellationRate(Trait):
    def calc_value(self):
        cancelCount = Orders.objects.filter(
                            seller_id=self.current_sellerid
                            ).filter(
                            status = 'C'
                            ).filter(
                            order_date__gte=self.from_date
                            ).filter(
                            order_date__lte=self.to_date
                            ).count(       
                            )
        totalOrders = Orders.objects.filter(
                            seller_id=self.current_sellerid
                            ).filter(
                            order_date__gte=self.from_date
                            ).filter(
                            order_date__lte=self.to_date
                            ).count(       
                            )
        cancellation_rate = round((cancelCount/totalOrders)*100, 2)
        return cancellation_rate

    def returnTraitWeightage(self):
        return 1

    def saveRecommendation(self, value, recommendation_list, IsDateEnteredByUser):
        if value <= 30:
            if (IsDateEnteredByUser == False):
                TraitValueDetails.objects.filter(
                    sid=self.current_sellerid
                    ).update(
                    recommendations_CancellationRate = "recommendation 1"
                    )
            recommendation_list.append("recommendation 1")
        elif value > 30 and value <= 70:
            if (IsDateEnteredByUser == False):
                TraitValueDetails.objects.filter(
                    sid = self.current_sellerid
                    ).update(
                    recommendations_CancellationRate = "recommendation 2"   
                    )
            recommendation_list.append("recommendation 2")
        else:
            if (IsDateEnteredByUser == False):
                TraitValueDetails.objects.filter(
                    sid = self.current_sellerid
                    ).update(
                    recommendations_CancellationRate = "recommendation 3"   
                    )
            recommendation_list.append("recommendation 3")'''

def main(request):
    current_sellerid = request.user.username
    if request.method == "GET":
        if 'from_date' in request.GET and 'to_date' in request.GET:
            from_date = request.GET['from_date']
            to_date = request.GET['to_date']
        elif 'from_date' not in request.GET and 'to_date' not in request.GET:
            to_date = datetime.now()
            from_date='1980-01-01'
    else:
        to_date = datetime.now()
        from_date='1980-01-01'

    if to_date == datetime.now() and from_date=='1980-01-01' :
        IsDateEnteredByUser = False
    else:
        IsDateEnteredByUser = True

    trait_name = []
    trait_value = []
    recommendation_list = []
    traitWeightageList = []
    for cls in Trait.__subclasses__():

        class_name = cls.__name__
        trait_component = re.sub( '(?<!^)(?=[A-Z])', '_', class_name ).lower()
        obj = cls(trait_component,from_date,to_date,current_sellerid)
        obj.template_method(trait_name, trait_value, recommendation_list,traitWeightageList,IsDateEnteredByUser)

    obj.calc_overall_performance(trait_value,traitWeightageList,IsDateEnteredByUser)

    trait_percentage_dictionary = {}
    trait_recommendation_dictionary = {}
    for name,percentage,recommendation in zip(trait_name,trait_value,recommendation_list):
        trait_percentage_dictionary[name]=percentage
        trait_recommendation_dictionary[name]=recommendation
    return render(request,'try.html',{'trait_percentage_dictionary':trait_percentage_dictionary,'trait_recommendation_dictionary':trait_recommendation_dictionary})

def ReturnValueForDashboard(request):
    current_sellerid = request.user.username
    to_date = datetime.now()
    from_date='1980-01-01'
    IsDateEnteredByUser = False
    trait_name = []
    trait_value = []
    recommendation_list = []
    traitWeightageList = []
    for cls in Trait.__subclasses__():

        class_name = cls.__name__
        trait_component = re.sub( '(?<!^)(?=[A-Z])', '_', class_name ).lower()
        obj = cls(trait_component,from_date,to_date,current_sellerid)
        obj.template_method(trait_name, trait_value, recommendation_list,traitWeightageList, IsDateEnteredByUser)

    obj.calc_overall_performance(trait_value,traitWeightageList,IsDateEnteredByUser)
    
    overall_value = TraitValueDetails.objects.all().filter(
                    sid=current_sellerid
                    ).values(
                    'overall_perf_val'
                    )
    for value in overall_value:
        for key,val in value.items():
            performance_percentage = val

    return performance_percentage

if __name__ == '__main__':
    main(request)