import requests
import time
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
    def __init__(self):
        self.template_name = "reasonable_recommendation_app/test_koya.html"
        self.search_url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
        self.ranking_url = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20220601"
     
    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context_data = super().get_context_data(**kwargs)
        context_data["test"] = "This is test Message"
        data = requests.get("https://app.rakuten.co.jp/services/api/Product/Search/20170426?format=json&keyword=%E3%82%B7%E3%83%A3%E3%83%B3%E3%83%97%E3%83%BC&applicationId=1086392607264524220%20").json()
        product_list = []
        for product in data["Products"]:
            product_list.append(product["Product"]["productName"])
        context_data["product_list"] = product_list
        return context_data
    
    def fetch_all_page_items(self, rakutenAPI_url, num_page,request=None):
        all_res_data = []
        for i in range(1,num_page+1):
            if rakutenAPI_url == self.search_url:
                params = {"applicationId" : "1086392607264524220",
                        "keyword" : request.POST["keyword"],
                        "format" : "json",
                        "page" :i}   
            elif rakutenAPI_url == self.ranking_url:
                params = {"applicationId" : "1086392607264524220",
                        "format" : "json",
                        "page" :i}   
            res_data = requests.get(rakutenAPI_url, params).json()
            all_res_data.extend(res_data["Items"])
            time.sleep(0.2)
        result_item_list = []
        for item in  all_res_data:
            result_item = test_koya_ResultItem(item["Item"]["itemName"], item["Item"]["itemPrice"], item["Item"]["itemCode"])
            result_item_list.append(result_item)
        return result_item_list
   
    def add_ranking_to_result_item_list(self, result_item_list):
        ranking_list = self.fetch_all_page_items(self.ranking_url, 30)
        result_item_list_tmp = result_item_list.copy()
        #検索結果のアイテムリストにランキング情報を付与する。
        for result_item in result_item_list_tmp:
            for i in range(len(ranking_list)):
                if result_item.item_code == ranking_list[i].item_code:
                    result_item.ranking = i
        
        #ランキングがつかなかったアイテムを削除
        result_item_list_added_ranking = [item for item in result_item_list_tmp if item.ranking != None]
        return result_item_list_added_ranking
    
    def sort_result_item_list_ascending_price(result_item_list):
        return
    
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
        result_item_list = self.fetch_all_page_items(self.search_url, 30, request)
        result_item_list_added_ranking = self.add_ranking_to_result_item_list(result_item_list)
        context = {"result_item_list": result_item_list_added_ranking}
        return super().render_to_response(context)
    
class test_koya_ResultItem:
    def __init__(self, name, price, item_code):
        self.name = name
        self.price = price
        self.item_code = item_code
        self.ranking = None

def test_yuto(request):
    return render(request, 'test_yuto.html', {})

def test_bibek(request):
    return render(request, 'test_bibek.html', {})

def test_akiba(request):
    return render(request, 'reasonable_recommendation_app/test_akiba.html', {})


