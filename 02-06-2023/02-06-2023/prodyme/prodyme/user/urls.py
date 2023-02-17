from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    #E-commerce API

    path('api/getCategory/', views.getCategorys.as_view()),
    path('api/getproduct/<category_name>/', views.getproductall.as_view()),
    path('api/getCategoryProductDetail/<product_id>/', views.getProductDetail.as_view()),
    path('api/searchFilter/<productName>/<categorName>/', views.searchFilter.as_view()),


    path('signup/',views.userSignup.as_view()),
    path('login2/',obtain_auth_token,name='login'),
    path('login/',views.userLogin.as_view(),name='login'),
    path('getprofile/',views.getProfile.as_view()),
    path('updateprofile/',views.updateProfile.as_view()),

    # Cart
    path('savecart/', views.savecartUserCreate.as_view()),
    path('statuschangesavecart/', views.StatusChangeSaveCart.as_view()),
    path('getsavecart/', views.getSaveCart.as_view()),
    path('boqCart/', views.getSaveCartPanda.as_view()),



    #path('accounts/', include('allauth.urls')),
    path('locationdetector/',views.locationdetector.as_view()),

    #part2
    path('api/postaddress/', views.postAddress.as_view()),
    path('api/getaddress/', views.getAddress.as_view()),
    path('api/DetailAddress/<address_id>/', views.getDetailAddres.as_view()),
    path('api/UpdateAddress/', views.UpdateAddres.as_view()),
    path('api/DeleteAddress/', views.DeleteAddress.as_view()),

    #part3
    path('api/UpdatePassword/', views.UpdatePassword.as_view()),
    path('api/postCommunicationPreference/',views.PostcommunicationPreference.as_view()),
    path('api/getCommunicationPreference/',views.getCommunicationPreference.as_view()),

    #part4
    path('api/getintouch/',views.getInTouch.as_view()),
    path('api/getloggedTickets/', views.getLoggedTickets.as_view()),
    path('api/getspecificloggedTickets/<id>/', views.getspecificloggedTickets.as_view()),
    path('api/getintouchChangeStatus/',views.getInTouchChangeStatus.as_view()),


    path('emailverify/',views.emailVerify.as_view()),
    path('emailverifyvalidate/',views.emailVerifyValidate.as_view()),
    path('forgotpassword/',views.userForgotPassword.as_view()),
    path('verifyresetpassword/',views.verifyResetPassword.as_view()),
    path('smartbuilder/',views.smartBuilder.as_view()),
    path('partitionmodification/',views.partitionModification.as_view()),
    path('cabinetstructure1/',views.cabinetstructure1.as_view()),
    path('checkparitions/',views.checkPartions.as_view()),
    path('column_modification/',views.columnModification.as_view()),
    path('column_deletion/',views.columnDeletion.as_view()),
    path('row_addition/',views.rowAddition.as_view()),
    path('change_basket/',views.changeBasket.as_view()),

    path('assignloyalty/',views.assignloyaltyUser.as_view()),
    path('getloyaltyPoints/',views.getLoyaltyPoints.as_view()),
    path('calculateQuantification/',views.calculateQuantification.as_view()),
    path('professionalSignup/',views.professionalSignup.as_view()),
    path('bookAService/',views.bookAServiceRequest.as_view()),
    path('optAService/',views.optAServiceRequest.as_view()),

    ###part4

    path('api/getCategory/<category_name>/', views.getsubCategory.as_view()),
    path('api/getCategory/<category_name>/<subCategory_name>/', views.getSubSubCategory.as_view()),
    path('api/getCategoryProduct/<category_name>/<subCategory_name>/<item_type>/', views.getProduct.as_view()),


    #upload data
    path("uploadItemData/<fileName>/", views.uploadItemData.as_view()),


    path('wishlist/',views.WishlistUserCreate.as_view()),
    path('statuschangewishlist/',views.StatusChangeWishlist.as_view()),
    path('getwishlist/',views.getWishlist.as_view()),
    path('boqCartWishlist/', views.getSaveCartWishlist.as_view()),

    #product filter

    # path('api/getProductRaleted/<productName>/', views.getProductRaleted.as_view()),
    path('api/getProductSimilar/<product_id>/', views.getProductsimilar.as_view()),
    path('api/getProductRecommended/<product_id>/', views.getProductRecommended.as_view()),
    path('api/getProductRating/<productRating>/', views.getProductRating.as_view()),
    path('api/getProductSeller/<productSaleCount>/', views.getProductSeller.as_view()),
    #search filter
]
