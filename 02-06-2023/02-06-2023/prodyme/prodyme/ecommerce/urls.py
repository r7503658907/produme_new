from django.urls import path
from . import views
urlpatterns = [
    #part3
    path('category/',views.categorylist.as_view()),
    path('itemcategory/',views.itemcategorylist.as_view()),
    path('itemtype/',views.itemtypelist.as_view())
]
