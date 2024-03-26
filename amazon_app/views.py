from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
import os
from django.conf import settings
from .scrape import main
from .forms import UploadFileForm
import pandas as pd
import json
from concurrent.futures import ThreadPoolExecutor
from .models import Header
from .models import PaginationSettings
# Create your views here.
from .categories import CATEGORIES
from .get_sku_by_cat import link_scrape
from .models import ScrapedData
from .models import ScrapeDataCount
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.core.paginator import Paginator
categ={'mainCategory':'','subcategory1':'','subcategory2':'','subcategory3':''}
# main_categories = ['Fashion', 'Electronics']  # Your list of main categories
# main_categories2 = []  # Initialize an empty list for subcategories
# main_categories3 = []
# main_categories4 = []
# Define a global variable to store the URL

@login_required(login_url='login')
def HomePage(request):
    global scraped_url
    status=None
    latest_status_entry = ScrapedData.objects.last()
    count_obj, created = ScrapeDataCount.objects.get_or_create()
    scrape_data_count = count_obj.count

    if latest_status_entry:
        status = latest_status_entry.status

    main_categories = ['FASHION', 'ELECTRONICS']  # Your list of main categories
    main_categories2 = []  # Initialize an empty list for subcategories
    main_categories3 = []  # Initialize an empty list for sub-subcategories
    main_categories4 = []  # Initialize an empty list for sub-sub-subcategories
    scraped_url = None
    
    if request.method == 'GET':
        main_category = request.GET.get('mainCategory')
        subcategory1 = request.GET.get('subcategory1')
        subcategory2 = request.GET.get('subcategory2')
        subcategory3 = request.GET.get('subcategory3')
    elif request.method == 'POST':
        
        main_category = request.POST.get('mainCategory')
        subcategory1 = request.POST.get('subcategory1')
        subcategory2 = request.POST.get('subcategory2')
        subcategory3 = request.POST.get('subcategory3')
    else:
        main_category = categ['mainCategory']
        subcategory1 = categ['subcategory1']
        subcategory2 = categ['subcategory2']
        subcategory3 = categ['subcategory3']

    if main_category:
       
        categ.clear()

      
        categ['mainCategory'] = main_category.upper()
        main_categories2 = list(CATEGORIES[main_category.upper()])
    
    if subcategory1:
        
        # print(categ)
        categ['subcategory1'] = subcategory1
        # Check if there is a third level
        try:
            if isinstance(CATEGORIES[categ['mainCategory']][subcategory1], dict):
                main_categories3 = list(CATEGORIES[categ['mainCategory']][subcategory1].keys())
            else:
                url = CATEGORIES[categ['mainCategory']][subcategory1]
        except:
            categ.clear()

            subcategory1 = ''
            subcategory2 = ''
            subcategory3 = ''
        categ.pop('subcategory2', None)  # Clear subcategory 2 selection
        categ.pop('subcategory3', None)  # Clear subcategory 3 selection

    if subcategory2:
        categ['subcategory2'] = subcategory2
        
        if isinstance(CATEGORIES[categ['mainCategory']][categ['subcategory1']][subcategory2], dict):
            main_categories4 = list(CATEGORIES[categ['mainCategory']][categ['subcategory1']][subcategory2].keys())
        else:
            url = CATEGORIES[categ['mainCategory']][categ['subcategory1']][subcategory2.title()]
            scraped_url = url

    
    if subcategory3:
        categ['subcategory3'] = subcategory3.title()
        url = CATEGORIES[categ['mainCategory']][categ['subcategory1']][categ['subcategory2']][subcategory3.title()]
        scraped_url = url  # Store the URL in the global variable
        print(url)

    return render(request, 'home.html', {'main_categories': main_categories, 'main_categories2': main_categories2,
                                        'main_categories3': main_categories3, 'main_categories4': main_categories4,
                                        'selected_main_category': main_category, 'selected_subcategory1': subcategory1,
                                        'selected_subcategory2': subcategory2, 'selected_subcategory3': subcategory3,
                                        'scraped_url': scraped_url,'status': status,'scrape_data_count':scrape_data_count})  # Pass the URL to the template
    

def scrape_by_cat(request):
    
    if request.method == 'POST':
        scraped_url = request.POST.get('scrapedUrl')
        if scraped_url is not None:# Get the scraped URL
            print('scraped_url',scraped_url)
            # Your scraping logic using the URL
            
            file_path=link_scrape(scraped_url)   #scrape asins ans save to SKI_files
            data = ScrapedData.objects.get_or_create(url=file_path)[0]
            data.status = "Category scraper Processing"
            data.save()
            with ThreadPoolExecutor() as executor:
                executor.submit(main, file_path, 15)
                data = ScrapedData.objects.get_or_create(url=file_path)[0]
                data.status = "Category scraper Complete"
                data.save()
            return JsonResponse({'success': True})
            # Redirect to the home page
            # return redirect('home')
    
    # If the request is GET or any other method, render the home page
    return HomePage(request)
@csrf_exempt  # Use this decorator to exempt CSRF verification for this view (for demonstration purposes)
def scrape_by_url(request):
    if request.method == 'POST':
        scraped_url = request.POST.get('urlInput')
        if scraped_url is not None:
            print('scraped_url:', scraped_url)
            # Your scraping logic using the URL
            data = ScrapedData.objects.get_or_create(url='')[0]
            data.status = "Url scraper Processing"
            data.save()
            file_path = link_scrape(scraped_url)  # Scrape asins and save to SKI_files
            data = ScrapedData.objects.get_or_create(url=file_path)[0]
            data.status = "Url scraper Processing"
            data.save()
            with ThreadPoolExecutor() as executor:
                executor.submit(main, file_path, 15)
                data = ScrapedData.objects.get_or_create(url=file_path)[0]
                data.status = "Url scraper Complete"
                data.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
    
def header_form(request):
    headers = [
        'store_name', 'Asin', 'Category', 'Title', 'MRP', 'Price', 'ShippingPrice',
        'Manufacturer', 'StarRating', 'IsPrime', 'CustomerReview', 'Weight', 'Color',
        'Size', 'PackageDimensions', 'ItemModelNumber', 'Department', 'DateFirstAvailable',
        'BestSellersRank', 'BulletPoints', 'ImageURLs', 'ProductUrl', 'VedioLinks', 'DeliveryTime', 'Description'
    ]
    pagination_counts = range(1, 401)  # Generates numbers from 1 to 400
    print(request.POST)
    if request.method == 'POST':
        form_type = request.POST.get('form_type', '')
        print(form_type)
        # Check if the header form is submitted
        if form_type == 'header_form':
            header_instance = Header.objects.first()  # Assuming there's only one instance
            if not header_instance:
                header_instance = Header.objects.create()  # Create an instance if it doesn't exist

            for header in headers:
                enabled = request.POST.get(header, False) == 'on'
                setattr(header_instance, f"{header.lower()}", enabled)
            
            header_instance.save()
            header_status = {header: getattr(header_instance, header.lower(), False) for header in headers}
            update_success = True  # or False based on the result of status update
            pagination_instance = PaginationSettings.objects.first()
            return render(request, 'settings.html', {
                'headers': headers, 
                'header_status': header_status,
                'pagination_counts': pagination_counts,
                'pagination_instance': pagination_instance,
                'update_success': update_success
            })
        # Check if the pagination form is submitted
        if form_type == 'pagination_form':
            pagination_instance = PaginationSettings.objects.first()  # Assuming there's only one instance
            if not pagination_instance:
                pagination_instance = PaginationSettings.objects.create(pagination_count=400)  # Create an instance if it doesn't exist with a default value
            pagination_count = int(request.POST.get('pagination_count', 400))  # Default to 400 if not provided
            print(pagination_count)
            pagination_instance.pagination_count = pagination_count  # Assign the pagination count to the pagination_count attribute
            pagination_instance.save()
            
            return render(request, 'settings.html', {
                'headers': headers, 
                'pagination_instance': pagination_instance,
                'pagination_counts': pagination_counts,
            })

    # If the request method is not POST or if no form is submitted, render the settings page with initial data
    header_instance = Header.objects.first()  # Assuming there's only one instance
    pagination_instance = PaginationSettings.objects.first()  # Assuming there's only one instance
    return render(request, 'settings.html', {
        'headers': headers, 
        'header_instance': header_instance,
        'pagination_instance': pagination_instance,
        'pagination_counts': pagination_counts
    })
def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

# def buttonPage(request):
#     return render (request,'buttons.html')
def settingsPage(request):
    # Get the header instance
    header_instance = Header.objects.first()  # Assuming there's only one instance
    page_instance=PaginationSettings.objects.first()
    # print(page_instance)
    # print(header_instance)
    pagination_counts = range(1, 401)  # Generates numbers from 1 to 400
    # Define all headers
    headers = [
        'store_name', 'Asin', 'Category', 'Title', 'MRP', 'Price', 'ShippingPrice',
        'Manufacturer', 'StarRating', 'IsPrime', 'CustomerReview', 'Weight', 'Color',
        'Size', 'PackageDimensions', 'ItemModelNumber', 'Department', 'DateFirstAvailable',
        'BestSellersRank', 'BulletPoints', 'ImageURLs', 'ProductUrl', 'VedioLinks', 'DeliveryTime', 'Description'
    ]

    # Create a dictionary to store the enabled status of each header
    header_status = {header: getattr(header_instance, header.lower(), False) for header in headers}

    # print(header_status)
    context = {
        'headers': headers,
        'header_status': header_status,
        'page_status': page_instance,
        'pagination_counts': pagination_counts
    }

    return render(request, 'settings.html', context)




@csrf_exempt  # Only if CSRF protection is enabled
def upload_asin(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded file
            uploaded_file = request.FILES['file']
            filename = uploaded_file.name
            print("Uploaded filename:", filename)
            
            # Save the uploaded file to a specific folder
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'upload')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            file_path = os.path.join(upload_dir, filename)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            print("File saved at:", file_path)
            # Return a JSON response indicating successful upload
            return JsonResponse({'success': True, 'file_path': file_path})
    else:
        form = UploadFileForm()
    return render(request, 'home.html', {'form': form})


def scrape_asin(request):
    
    file_path = request.GET.get('file_path')
    data = ScrapedData.objects.get_or_create(url=file_path)[0]
    data.status = "Asin scraper Processing"
    data.save()
    # Execute scraping function in background
    with ThreadPoolExecutor() as executor:
        executor.submit(main, file_path, 15)
        
    return JsonResponse({'success': True})






def list_excel_files(request):
    # Path to the folder containing Excel files
    folder_path = os.path.join(settings.MEDIA_ROOT, 'download')

    # Get a list of Excel files in the folder
    excel_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    print(excel_files)
    # Pass the list of files to the template
    return render(request, 'download.html', {'excel_files': excel_files})


def download_excel_file(request, file_name):
    # Path to the folder containing Excel files
    folder_path = os.path.join(settings.MEDIA_ROOT, 'download')

    # Full path to the Excel file
    file_path = os.path.join(folder_path, file_name)

    # Open the file for reading as binary
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        # Set the Content-Disposition header to force download
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response