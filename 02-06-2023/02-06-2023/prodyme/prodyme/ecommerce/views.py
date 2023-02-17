from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from . models import *
from .serializers import *


class categorylist(APIView):
    def get(self,request):
        try:
            category = Category.objects.all()  #ORM -> select * from Category
            serializer = categorySerializer(category,many=True)
            return JsonResponse({
            'status': 200,
            'message': 'Prodyme Category List',
            'category Name': serializer.data,
            })
        except Exception as e:
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'Error ': str(e),
            })


class itemcategorylist(APIView):
    def get(self, request):
        try:
            serializer = categorySerializer(data=request.data)
            if serializer.is_valid():
                category_name = serializer.data['category_name']
                itemcategory = Item_Category.objects.filter(category_name=category_name).values() # ORM -> select * from Itemcategory where category =
                print(itemcategory)
                return JsonResponse({
                'status': 200,
                'message': 'Prodyme Item Category List',
                'category Name': list(itemcategory,)
                })
        except Exception as e:
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'Error ': str(e),
            })

class itemtypelist(APIView):
    def get(self, request):
        try:
            serializer = subcategorySerializer(data=request.data)
            if serializer.is_valid():
                item_category_name = serializer.data['item_category_name']
                itemtype = Item_Type.objects.filter(
                    item_category_name=item_category_name).values()
                print(itemtype)
                return JsonResponse({
                    'status': 200,
                    'message': 'Prodyme Item Category List',
                    'category Name': list(itemtype, )
                })
        except Exception as e:
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'Error ': str(e),
            })
