import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView



def home(request):
    print(request.user)
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    context = {'user': user}
    return render(request, 'reasonable_recommendation_app/home.html', context)

class test_koya(TemplateView):
    template_name = "reasonable_recommendation_app/test_koya.html"
    
    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context_data = super().get_context_data(**kwargs)
        context_data["test"] = "This is test Message"
        data = requests.get("https://app.rakuten.co.jp/services/api/Product/Search/20170426?format=json&keyword=%E3%82%B7%E3%83%A3%E3%83%B3%E3%83%97%E3%83%BC&applicationId=1086392607264524220%20").json()
        product_list = []
        for product in data["Products"]:
            product_list.append(product["Product"]["productName"])
        print(product_list)
        context_data["product_list"] = product_list
        return context_data
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return super().render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        params = {"applicationId" : "1086392607264524220",
                  "keyword" : request.POST["keyword"],
                  "format" : "json"}   
        res_data = requests.get("https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601", params).json()
        result_item_list = []
        for item in res_data["Items"]:
            result_item = test_koya_ResultItem(item["Item"]["itemName"], item["Item"]["itemPrice"])
            result_item_list.append(result_item)
        context = {"result_item_list": result_item_list}
        return super().render_to_response(context)
    
class test_koya_ResultItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

def test_yuto(request):
    return render(request, 'test_yuto.html', {})

def test_bibek(request):
    return render(request, 'test_bibek.html', {})

# def test_akiba(request):
#     return render(request, 'reasonable_recommendation_app/test_akiba.html', {})

class test_akiba(TemplateView):
    template_name = 'reasonable_recommendation_app/test_akiba.html'


