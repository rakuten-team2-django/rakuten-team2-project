from django.shortcuts import render
from django.views.generic import TemplateView
import requests

# Create your views here.

def home(request):
    return render(request, 'reasonable_recommendation_app/home.html', {})

class test_koya(TemplateView):
    template_name = "reasonable_recommendation_app/test_koya.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data["test"] = "This is test Message"
        data = requests.get("https://app.rakuten.co.jp/services/api/Product/Search/20170426?format=json&keyword=%E3%82%B7%E3%83%A3%E3%83%B3%E3%83%97%E3%83%BC&applicationId=1086392607264524220%20").json()
        product_list = []
        for product in data["Products"]:
            product_list.append(product["Product"]["productName"])
        print(product_list)
        context_data["product_list"] = product_list
        return context_data
    
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.kwargs)

def test_yuto(request):
    return render(request, 'test_yuto.html', {})

def test_bibek(request):
    return render(request, 'test_bibek.html', {})

def test_akiba(request):
    return render(request, 'reasonable_recommendation_app/test_akiba.html', {})

