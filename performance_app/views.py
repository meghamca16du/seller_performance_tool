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
            #s = SellerDetails.objects.filter(sid='ank202').only('sid').all()
            s = SellerDetails.objects.get(sid='ank202')
            save_sid = TraitValueDetails(sid=s)
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
        LateOrders = OrderDetails.objects.all().filter(
                         actual_shipment__isnull=False
                         ).filter(
                         actual_shipment__gt=F('exp_shipment')
                         ).count()
        Total=OrderDetails.objects.filter(sid='ank202').count()
        late_perc=(LateOrders/Total)*100
        return late_perc

    def store_value(self,value):
        s = SellerDetails.objects.get(sid='ank202')
        trait_obj=TraitValueDetails(sid=s,late_shipment_rate=value)
        trait_obj.save()
        return value

'''
class HitToSuccessRatio(Trait):

    def calc_value(self):
        sid_pid_tuple = ProductDetails.objects.filter(
                                sid='ank202'
                                ).values_list(
                                'sid','pid',flat=True
                                )
        

        success_num = OrderDetails.objects.filter(
                                sid__in=s,pid__in=p
                                ).count()
        
        hit_num = ProductDetails.objects.all().filter(
                       sid=ank202
                        ).annotate(
                        hit_num=Sum('no_of_hits')
                        )
        hit_to_success_ratio = (success_num/hit_num)*100
        return hit_to_success_ratio

    def store_value(self,value):
        s = SellerDetails.objects.get(sid='ank202')
        trait_obj=TraitValueDetails(sid=s,hit_to_success_ratio=value)
        trait_obj.save()
        return value
'''

def main(request):
    trait_value_dict={}
    l=LateShipmentRate()
    late_perc=l.template_method()
    trait_value_dict['late_perc']=late_perc
    return render(request,'performance.html',trait_value_dict)

    #h = HitToSuccessRatio()
    #hit_to_success_ratio = h.template_method()
    #trait_value_dict['hit_to_success_ratio'] = hit_to_success_ratio
    #return render(request,'performance.html',trait_value_dict)

if __name__ == '__main__':
    main(request)