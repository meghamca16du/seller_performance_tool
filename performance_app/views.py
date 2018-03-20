from django.shortcuts import render
from dashboard.models import *
from django.db.models import Count,F
from abc import ABC, abstractmethod
#from django.http import HttpResponse

"""def performance(request):
    cancelled=OrderDetails.objects.filter(status='C').count()
    total=OrderDetails.objects.filter(sid='ank202').count()
    perc=(cancelled/total)*100
    return render(request,'performance.html',{'perc':perc})
    #return HttpResponse(perc)
"""

class Trait(ABC):
    #trait_value_dict={}

    #def __init__(self,trait_components):
     #   parameters=trait_components
    
    def template_method(self):
        #self.get_parameters()
        self.store_sid()
        value = self.calc_value()
        self.store_value(value)

    #def get_parameters(self,trait_components):
       # parameters=trait_components

    def store_sid(self):    #not working
        check = TraitValueDetails.objects.filter(sid='ank202').exists()
        if check == False:
            #s = SellerDetails.objects.filter(sid='adi201')
            save_sid = TraitValueDetails(tid='1',sid='ank202',late_shipment_rate=0,on_time_delivery=0,hit_to_success_ratio=0,return_rate=0)
            save_sid.save()
        else:
            pass

    @abstractmethod
    def calc_value(self):
        pass
    
    @abstractmethod
    def store_value(value):
        pass

class LateShipmentRate(Trait):

    def calc_value(self):
        LateOrders=OrderDetails.objects.all().filter(actual_shipment__isnull=False).filter(actual_shipment__gt=F('exp_shipment')).count()
        Total=OrderDetails.objects.filter(sid='ank202').count()
        late_perc=(LateOrders/Total)*100
        return late_perc

    def store_value(self,value):
        trait_obj=TraitValueDetails(late_shipment_rate=value)
        trait_obj.save()
        return value

   
    
def main(request):
    trait_value_dict={}
    l=LateShipmentRate()
    late_perc=l.template_method()
    trait_value_dict['late_perc']=late_perc
    return render(request,'performance.html',trait_value_dict)

if __name__ == '__main__':
    main(request)