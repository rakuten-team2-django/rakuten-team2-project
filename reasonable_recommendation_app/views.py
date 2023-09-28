from django.shortcuts import render
from django.views.generic import TemplateView
import json
import requests
from reasonable_recommendation_app.models import Discounted_Items
from django.core.management.base import BaseCommand
from django.http import JsonResponse

def home(request):
    return render(request, 'reasonable_recommendation_app/home.html', {})
def test_koya(request):
    return render(request, 'test_koya.html', {})
def test_yuto(request):
    return render(request, 'test_yuto.html', {})

def test_bibek(request):
    params = {
        "format": "json",
        "applicationId": 1007895533761095400,
    }
    app_id = "1007895533761095400"
    api_url = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20220601"
    try:
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if "Items" in data.keys():
                  item_list=[]
                  for item in data['Items']:
                        item_list.append(item['Item'])
                  sorted_items = sorted(item_list, key=lambda x: int(x["rank"]))
                  top_10_least_sold = sorted_items[:10]
                  print(top_10_least_sold)
                  for item in top_10_least_sold:
                    Discounted_Items.objects.create(
                        product_id=item.get('itemCode'),
                        product_name=item.get('itemName'),
                        product_price=item.get('itemPrice'),
                        productimg_url=item.get('itemUrl'),  
                  )
                  return render(request, 'reasonable_recommendation_app/disc_items.html', {'top_10_least_sold_items': top_10_least_sold})
            else:
                  return render(request, 'reasonable_recommendation_app/error.html', {'message': 'No ranking information found in the response.'})
                  
        else:
              return render(request, 'reasonable_recommendation_app/error.html', {'message': f'Failed to fetch data. Status code: {response.status_code}'})
    except Exception as e:
           return render(request, 'reasonable_recommendation_app/error.html', {'message': f'An error occurred: {str(e)}'})
    
def rep_data(request):
    item=Discounted_Items.objects.all()
    context={'items': item}
    return render(request,'database_data.html',context)

def test_akiba(request):
    return render(request, 'reasonable_recommendation_app/test_akiba.html', {})
