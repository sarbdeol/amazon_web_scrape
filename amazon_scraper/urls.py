"""registration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from amazon_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('home/',views.HomePage,name='home'),
    path('',views.HomePage,name='home'),
    path('scrape_by_cat/',views.scrape_by_cat,name='scrape_by_cat'),
    path('scrape_by_url/', views.scrape_by_url, name='scrape_by_url'),
    path('logout/',views.LogoutPage,name='logout'),
    path('settings/',views.settingsPage,name='settings'),
    path('header-form/', views.header_form, name='header_form'),    
    path('upload/', views.upload_asin, name='upload_asin'),
    path('scrape_asin/', views.scrape_asin, name='scrape_asin'),  # Define URL pattern for scrape_asin view
    path('download/', views.list_excel_files, name='list_excel_files'),
    path('excel-files/<str:file_name>/', views.download_excel_file, name='download_excel_file'),



    
]