from django.urls import path
from .views import * # or HomeView,AboutView,ContactView,HistoryView,BloglistView  pani lekhna sakxau
from django.contrib.sitemaps.views import sitemap
from . import views

app_name = 'sellapp'
urlpatterns =[
	path('',AllprView.as_view(),name='home'),
	# path('blog/create/',post_create,name='blogcreate'),
	path('blog/create',BlogCreateForm.as_view(),name='blogcreate'),
	path('bloglist/',BloglistView.as_view(),name='bloglist'),
	
    path("register/",
         CustomerRegistrationView.as_view(), name="customerregistration"),

    path("logout/", CustomerLogoutView.as_view(), name="customerlogout"),
    path("login/", CustomerLoginView.as_view(), name="customerlogin"),
	path('mobile/',MobileViewed.as_view(),name="mobile"),
	path('bike/',BikeViewed.as_view(),name="bike"),
	path('fridge/',FridgeViewed.as_view(),name="fridge"),
	path('cycle/',CycleViewed.as_view(),name="cycle"),
	path('blog/<int:pk>/detail/',BlogDetailView.as_view(),name='blogdetail'),
	path("search/", SearchView.as_view(), name="search"),
	path('pricerange/', views.MinmaxPrice, name='pricerange'),
	path("profile/", ProfileView.as_view(), name="profile"),
	path("mypost/", MypostView.as_view(), name="mypost"),
	path('changepass/', views.changepPass, name='changepass'),
	path("forgot-password/", PasswordForgotView.as_view(), name="passworforgot"),
	path("password-reset/<email>/<token>/",
         PasswordResetView.as_view(), name="passwordreset"),
	path('blog/<int:pk>/update/',BlogUpdateView.as_view(),name='blogupdate'),
	path('blog/<int:pk>/delete/',BlogDeleteView.as_view(),name='blogdelete'),
	path('lowtohigh/', LowToHigh.as_view(), name='lowtohigh'),
    path('hightolow/', HighToLow.as_view(), name='hightolow'),
]