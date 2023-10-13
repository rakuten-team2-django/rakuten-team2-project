from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from .models import User, Discounted_Items # TODO
import datetime
from decimal import Decimal, ROUND_HALF_UP
from . import views

DISCOUNTRATE = 0.10 # 0.05
TESTUSER = 1
AGEMIN = 20
AGEMAX = 30
TOP700FOR5PERCENT = 700
TOP900FOR10PERCENT = 900
DISCOUNT10PERCENTRATE = 0.1
DISCOUNT5PRTCENTRATE = 0.05
DISCOUNTRANGE = 10
DISCOUNTDIFF = 0.01
MAXDISCOUNT = 0.10

class DiscountApplier(ListView):
    # TODO: Change name
    model = Discounted_Items
    #model.objects.order_by("-product_rank")

    # TODO: Change name
    template_name = 'reasonable_recommendation_app/test_yuto.html'

    paginate_by = 10
    ordering = ["-product_rank"]

    def get_context_data(self, **kwargs):
        views.test_bibek(self.request)
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
            else:
                item.price = Decimal(item.product_price).quantize(Decimal('0'), rounding=ROUND_HALF_UP)

        return self.context
    
    def sort_by_rank(self):
        self.context['object_list'] = sorted(self.context['object_list'], key = lambda x: int(x.product_rank), reverse=True)
    
def apply_discount(item):
    # TODO: if table are defined, make code executable
    try:
        """
        if item.product_rank >= TOP900FOR10PERCENT:
            priceproportion = 1 - DISCOUNTRATE
            item.discount_rate = f"{int(DISCOUNT10PERCENTRATE * 100)}%"
        elif item.product_rank >= TOP700FOR5PERCENT:
            priceproportion = 1 - DISCOUNTRATE
            item.discount_rate = f"{int(DISCOUNT5PRTCENTRATE * 100)}%"
            """
        if item.product_rank > (1000 - (MAXDISCOUNT / DISCOUNTDIFF) * DISCOUNTRANGE):
            priceproportion = 1 - ( MAXDISCOUNT - (((1000 - item.product_rank) // DISCOUNTRANGE) * DISCOUNTDIFF )) 
            item.discount_rate = f"{int(( MAXDISCOUNT - (((1000 - item.product_rank) // DISCOUNTRANGE) * DISCOUNTDIFF )) * 100)}%"
        else:
            priceproportion = 1
    except Exception:
        print("error")
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
    
