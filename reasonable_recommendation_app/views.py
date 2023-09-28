import requests
import time
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .koya_models import ResultItemsModel

def home(request):
    print(request.user)
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    context = {'user': user}
    return render(request, 'reasonable_recommendation_app/home.html', context)

class test_koya_Search(TemplateView):
    def __init__(self):
        self.template_name = "reasonable_recommendation_app/test_koya.html"
        self.search_url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
        self.ranking_url = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20220601"
    
    def post(self, request, *args, **kwargs):
        result_item_list = test_koya_APIListOperations().fetch_all_page_items(self.search_url, 20, request)
        result_item_list_sorted = test_koya_APIListOperations.bubble_sort_result_item_list_ascending_price(result_item_list)
        ResultItemsModel.objects.all().delete()
        for result_item in result_item_list_sorted:
            ResultItemsModel.objects.create(item_name=result_item.item_name, item_price=result_item.item_price, item_code=result_item.item_code, image_urls=result_item.image_urls, ranking=result_item.ranking)
        context = {"result_item_list": result_item_list_sorted}
        return super().render_to_response(context)
    
class test_koya_RankingSearch(TemplateView):
    def __init__(self):
        self.template_name = "reasonable_recommendation_app/test_koya.html"
        self.search_url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
        self.ranking_url = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20220601"
    
    def add_ranking_to_result_item_list(self, result_item_list):
        ranking_list = test_koya_APIListOperations.fetch_all_page_items(self.ranking_url, 10)
        result_item_list_tmp = result_item_list.copy()
        #検索結果のアイテムリストにランキング情報を付与する。
        for result_item in result_item_list_tmp:
            for i in range(len(ranking_list)):
                if result_item.item_code == ranking_list[i].item_code:
                    result_item.ranking = i
        
        #ランキングがつかなかったアイテムを削除
        result_item_list_added_ranking = [item for item in result_item_list_tmp if item.ranking != None]
        return result_item_list_added_ranking
    
    def get(self, request, *args, **kwargs):
        result_item_list = list(ResultItemsModel.objects.all())
        print(result_item_list[0].item_name)
        result_item_list_added_ranking = self.add_ranking_to_result_item_list(result_item_list)
        context = {"result_item_list": result_item_list_added_ranking}
        return super().render_to_response(context)
    
class test_koya_APIListOperations:
    
    @staticmethod
    def fetch_all_page_items(rakutenAPI_url, num_page,request=None):
        search_url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
        ranking_url = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20220601"
        all_res_data = []
        for i in range(1,num_page+1):
            if rakutenAPI_url == search_url:
                params = {"applicationId" : "1086392607264524220",
                            "keyword" : request.POST["keyword"],
                            "format" : "json",
                            "page" :i}   
            elif rakutenAPI_url == ranking_url:
                params = {"applicationId" : "1086392607264524220",
                            "age": 20,
                            "format" : "json",
                            "page" :i}   
            res_data = requests.get(rakutenAPI_url, params).json()
            all_res_data.extend(res_data["Items"])
            time.sleep(0.2)
        result_item_list = []
        for item in  all_res_data:
            result_item = test_koya_ResultItem(item["Item"]["itemName"], item["Item"]["itemPrice"], item["Item"]["itemCode"], item["Item"]["mediumImageUrls"])
            result_item_list.append(result_item)
        return result_item_list
    
    @staticmethod
    def bubble_sort_result_item_list_ascending_price(result_item_list_tmp):
        result_item_list_tmp = result_item_list_tmp.copy()
        for i in range(len(result_item_list_tmp)):
            for j in range(len(result_item_list_tmp) - i -1):
                if result_item_list_tmp[j].item_price > result_item_list_tmp[j+1].item_price: #左の方が大きい場合
                    result_item_list_tmp[j], result_item_list_tmp[j+1] = result_item_list_tmp[j+1], result_item_list_tmp[j] #前後入れ替え
        return result_item_list_tmp
    
class test_koya_ResultItem:
    def __init__(self, name, price, item_code, image_urls):
        self.item_name = name
        self.item_price = price
        self.item_code = item_code
        self.image_urls = []
        for image_url in image_urls:
            self.image_urls.append(image_url["imageUrl"])
        self.image_url = self.image_urls[0]
        self.images = []
        self.ranking = None

def test_yuto(request):
    return render(request, 'test_yuto.html', {})

def test_bibek(request):
    return render(request, 'test_bibek.html', {})

def test_akiba(request):
    return render(request, 'reasonable_recommendation_app/test_akiba.html', {})


