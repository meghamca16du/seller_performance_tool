from django.shortcuts import render
from dashboard.models import *
from django.db.models import Count,F
from abc import ABC, abstractmethod
import re

class Trait(ABC):

    def __init__(self,trait_cmp):
        self.trait_component=trait_cmp

    def template_method(self,l1,l2):
        table_name = self.find_table()
        self.store_sid(table_name)
        value=self.calc_value()
        self.store_value(value,table_name,l1,l2)
        overall_perf_value = self.calc_overall_performance(l2)
        self.store_overall_value(self,overall_perf_value)

    def find_table(self):
        for cls in Base_TraitValueDetails.__subclasses__():
            field=cls._meta.get_field(self.trait_component)
            if field:
                return cls

    def store_sid(self,table_name):
        check=table_name.objects.filter(sid='ank202').exists()
        if check==False:
            s=SellerDetails.objects.get(sid='ank202')
            save_sid=table_name(sid=s)
            save_sid.save()

    @abstractmethod
    def calc_value(self):
        pass

    def store_value(self,value,table_name,l1,l2):
        trait_obj=table_name.objects.filter(sid='ank202').update(**{self.trait_component:value})
        l1.append(self.trait_component)
        l2.append(value)
        return value

    def calc_overall_performance(self,l2):
        overall_perf_val = sum(l2) / len(l2)
        return overall_perf_val

    def store_overall_value(self,overall_perf_value):
        obj = TraitValueDetails.objects.filter(
                    sid='ank202'
                    ).update(
                    overall_perf_val = overall_perf_value
                    )

class LateShipmentRate(Trait):
    def calc_value(self):
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

class OnTimeDelivery(Trait):
    def calc_value(self):
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

def main(request):
    l1 = []
    l2 = []
    for cls in Trait.__subclasses__():

        class_name = cls.__name__
        trait_component = re.sub( '(?<!^)(?=[A-Z])', '_', class_name ).lower()
        obj = cls(trait_component)
        obj.template_method(l1, l2)
    
    mylist = zip(l1,l2)
    return render(request,'performance.html',{'mylist':mylist})

if __name__ == '__main__':
    main(request)