from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from .models import Item # TODO

class DiscountApplier(ListView):
    # TODO: Change name
    model = Item

    # TODO: Change name
    template_name = 'reasonable_recommendation_app/discounts_items.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
