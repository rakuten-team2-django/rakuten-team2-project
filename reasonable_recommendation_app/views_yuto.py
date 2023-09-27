from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from .models import User, Item # TODO
import datetime

class DiscountApplier(ListView):
    # TODO: Change name
    model = Item

    # TODO: Change name
    template_name = 'reasonable_recommendation_app/discounts_items.html'

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
        raise NotImplementedError
        # fetch user information from database
        user_id = self.request.POST.get('user_id', '') # TODO
        user_info = User.objects.get(id=user_id)
        for item in DiscountApplier.model:
            
        return context
    
def apply_discount(item):
    DISCOUNTRATE = 0.10 # 0.05
    price = item.price * DISCOUNTRATE
    return price

def check_age(user):
    AGEMIN = 20
    AGEMAX = 30
    age = (int(datetime.date.today().strftime("%Y%m%d")) - int(user.birthday.strftime("%Y%m%d"))) // 10000
    if AGEMIN <= int(age) < AGEMAX:
        return True
    else:
        return False

