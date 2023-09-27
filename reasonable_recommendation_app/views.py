from django.shortcuts import render
from django.views.generic import TemplateView
import requests
import time

# Create your views here.

def home(request):
    return render(request, 'reasonable_recommendation_app/home.html', {})

class test_koya(TemplateView):
    template_name = "reasonable_recommendation_app/test_koya.html"
    
    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context_data = super().get_context_data(**kwargs)
        context_data["test"] = "This is test Message"
        data = requests.get("https://app.rakuten.co.jp/services/api/Product/Search/20170426?format=json&keyword=%E3%82%B7%E3%83%A3%E3%83%B3%E3%83%97%E3%83%BC&applicationId=1086392607264524220%20").json()
        product_list = []
        for product in data["Products"]:
            product_list.append(product["Product"]["productName"])
        context_data["product_list"] = product_list
        return context_data
    
    def fetch_all_page_items(self, request, num_page):
        all_res_data = []
        for i in range(1,num_page+1):
            params = {"applicationId" : "1086392607264524220",
                    "keyword" : request.POST["keyword"],
                    "format" : "json",
                    "page" :i}   
            res_data = requests.get("https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601", params).json()
            all_res_data.extend(res_data["Items"])
            time.sleep(0.2)
        result_item_list = []
        for item in  all_res_data:
            result_item = test_koya_ResultItem(item["Item"]["itemName"], item["Item"]["itemPrice"])
            result_item_list.append(result_item)
        return result_item_list
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return super().render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        """
        params = {"applicationId" : "1086392607264524220",
                  "keyword" : request.POST["keyword"],
                  "format" : "json"}   
        res_data = requests.get("https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601", params).json()
        result_item_list = []
        for item in res_data["Items"]:
            result_item = test_koya_ResultItem(item["Item"]["itemName"], item["Item"]["itemPrice"])
            result_item_list.append(result_item)
        """
        result_item_list = self.fetch_all_page_items(request, 10)
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

def test_akiba(request):
    return render(request, 'reasonable_recommendation_app/test_akiba.html', {})

