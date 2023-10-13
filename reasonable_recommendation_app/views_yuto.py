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
DISCOUNTRANKMIN = 900
DISCOUNTRANKMAX = 1000

class DiscountApplier(ListView):
    # TODO: Change name
    model = Discounted_Items

    # TODO: Change name
    template_name = 'reasonable_recommendation_app/test_yuto.html'

    paginate_by = 10

    def get_context_data(self, **kwargs):
        self.context = super().get_context_data(**kwargs)
        try:
            user_id = self.request.user.id #self.request.POST.get('user_id', TESTUSER) # TODO
        except Exception:
            print("Need login")
            return "Need login."
        user_info = User.objects.get(id=user_id)

        for item in self.context['object_list']:
            if check_age(user_info):
                item = apply_discount(item)
                item.discount_rate = DISCOUNTRATE
            else:
                item.price = Decimal(item.product_price).quantize(Decimal('0'), rounding=ROUND_HALF_UP)

        self.sort_by_rank()
        return self.context
    
    def sort_by_rank(self):
        self.context['object_list'] = sorted(self.context['object_list'], key = lambda x: int(x.product_rank), reverse=True)
    
def apply_discount(item):
    # TODO: if table are defined, make code executable
    if DISCOUNTRANKMIN <= item.product_rank <= DISCOUNTRANKMAX:
        priceproportion = 1 - DISCOUNTRATE
    else:
        priceproportion = 1

    price = item.product_price * Decimal(priceproportion)
    item.price = Decimal(price).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
    return item

def check_age(user):
    age = (int(datetime.date.today().strftime("%Y%m%d")) - int(user.birthday.strftime("%Y%m%d"))) // 10000
    
    if AGEMIN <= int(age) < AGEMAX:
        return True
    else:
        return False
    
