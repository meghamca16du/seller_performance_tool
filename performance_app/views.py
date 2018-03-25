from django.shortcuts import render
from dashboard.models import *
from django.db.models import Count, F, Sum
from abc import ABC, abstractmethod
#import numpy as np
import re

class Trait(ABC):
    '''
        Objective: An abstract class which calculates the value of the trait and stores it in the database.
    ''' 
    traitWeightageList = []
    def __init__(self, trait_cmp):
        '''
        Objective: A constructor which initializes the trait component variable.
        Input Parameter: trait_cmp - Trait Component
        Return Value: Returns an object of the called class
        '''
        self.trait_component = trait_cmp

    def template_method(self, trait_name, trait_value):
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
        Trait.traitWeightageList.append(traitWeightage)
        #self.appendTraitWeightageList(traitWeightageList)
        #traitWeightageList.append( traitWeightage )
        self.store_value(value, table_name, trait_name, trait_value)
        overall_perf_value = self.calc_overall_performance(trait_value, Trait.traitWeightageList)
        self.store_overall_value(TraitValueDetails,overall_perf_value)

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
        check=table_name.objects.filter(sid='ank202').exists()
        if check==False:
            s=SellerDetails.objects.get(sid='ank202')
            save_sid=table_name(sid=s)
            save_sid.save()

    @abstractmethod
    def calc_value(self):
        '''
        Objective: An abstract method which calculates the value of trait_component.
        Return Value: Calculated Value of the trait.
        '''
        pass

    def store_value(self,value,table_name,trait_name, trait_value):
        '''
        Objective: To store or update the value of the trait component in the database table.
        Input Parameter: value - Calculated value of the trait component
                         table_name - Database table in which the value is to be inserted/updated
                         trait_list - A list of Traits
                         value_list - A list of Values of the corresponding traits defined in the trait_list
        '''
        trait_obj=table_name.objects.filter(sid='ank202').update(**{self.trait_component:value})
        trait_name.append(self.trait_component)
        trait_value.append(value)
        return value

    def calc_overall_performance(self,trait_value,traitWeightageList):
        '''
        Objective: To calculate the overall performance of the seller.
        Input Parameter: value_list - A list of Values of the corresponding traits defined in the trait_list
        Return Value: overall_perf_val - Overall performance value of the seller
        '''
        #numerator = (np.array(trait_value)) * (np.array(traitWeightageList))
        #decimal_trait_value = [decimal.Decimal(val) for val in trait_value]
        #lists = zip(decimal_trait_value, traitWeightageList)
        #for val,weightage in lists:
        #   overall_perf_val = overall_perf_val + (val*weightage)
        numerator = [trait_value[i]*traitWeightageList[i] for i in range(len(trait_value))]
        #print(numerator)
        overall_perf_val = sum(numerator) / sum(traitWeightageList)
        #print(overall_perf_val)
        return overall_perf_val

    def store_overall_value(self,TraitValueDetails ,overall_perf_value):
        '''
        Objective: To store or update the overall performance of the seller.
        Input Paramter: tabel_name - Database table in which the value is to be inserted/updated
                        overall_performance - Overall performance value of the seller
        '''
        TraitValueDetails.objects.filter(
                    sid='ank202'
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
        LateOrders = OrderDetails.objects.all().filter(
                         sid='ank202'
                         ).filter(
                         actual_shipment__isnull=False
                         ).filter(
                         actual_shipment__gte=F('exp_shipment')
                         ).count()
        Total = OrderDetails.objects.filter(sid='ank202').count()
        late_perc = (LateOrders/Total)*100
        return late_perc

    def returnTraitWeightage(self):
        return 2

class OnTimeDelivery(Trait):
    '''
    Objective: A derived class of Trait which calculates the value of 'On time Delivery' trait
    '''
    def calc_value(self):
        '''
        Objective: Calculates the values of on_time_delivery.
        Return Value: late_perc - Percentage of the on time delivery done by the seller.
        '''
        onTimeDeliver = OrderDetails.objects.all().filter(
                            sid='ank202'
                            ).filter(
                            actual_delivery__isnull=False
                            ).filter(
                            exp_delivery__gte = F('actual_delivery')
                            ).count()
        totalDeliver = OrderDetails.objects.filter(
                            sid='ank202'
                            ).filter(
                            actual_delivery__isnull=False
                            ).count()
        Percentage = (onTimeDeliver/totalDeliver)*100
        return Percentage

    def returnTraitWeightage(self):
        return 2

class HitToSuccessRatio(Trait):
    '''
    Objective: A derived class of Trait which calculates the value of 'Hit to Success Ratio' trait
    '''
    def calc_value(self):
        '''
        Objective: Calculates the values of hit_to_success_ratio.
        Return Value: late_perc - Percentage of the successes.
        '''
        success = OrderDetails.objects.filter(
                            sid='ank202'
                            ).count(       
                            )
        hits = ProductDetails.objects.filter(sid='ank202').aggregate(Sum('no_of_hits'))['no_of_hits__sum']
        success_perc=(success/hits)*100
        return success_perc

    def returnTraitWeightage(self):
        return 1

def main(request):
    trait_name = []
    trait_value = []
    for cls in Trait.__subclasses__():

        class_name = cls.__name__
        trait_component = re.sub( '(?<!^)(?=[A-Z])', '_', class_name ).lower()
        obj = cls(trait_component)
        obj.template_method(trait_name, trait_value)
    
    trait_list = zip(trait_name, trait_value)
    return render(request,'performance.html',{'trait_list':trait_list})

if __name__ == '__main__':
    main(request)