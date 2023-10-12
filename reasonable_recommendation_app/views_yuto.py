from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from .models import User, Discounted_Items # TODO
import datetime
from decimal import Decimal, ROUND_HALF_UP

DISCOUNTRATE = 0.10 # 0.05
TESTUSER = 1
AGEMIN = 20
AGEMAX = 30

class DiscountApplier(ListView):
    # TODO: Change name
    model = Discounted_Items

    # TODO: Change name
    template_name = 'reasonable_recommendation_app/test_yuto.html'

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.POST.get('user_id', TESTUSER) # TODO
        user_info = User.objects.get(id=user_id)
        
        if check_age(user_info):
            for item in context['object_list']:
                item = apply_discount(item)
                item.discount_rate = DISCOUNTRATE

        return context
    
def apply_discount(item):
    item.price = item.price * (1 - DISCOUNTRATE)
    item.price = Decimal(item.price).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
    return item

def check_age(user):
    age = (int(datetime.date.today().strftime("%Y%m%d")) - int(user.birthday.strftime("%Y%m%d"))) // 10000
    
    if AGEMIN <= int(age) < AGEMAX:
        return True
    else:
        return False
