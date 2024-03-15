# models.py
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    # Add other fields as needed

class Header(models.Model):
    store_name = models.BooleanField(default=False)
    asin = models.BooleanField(default=False)
    category = models.BooleanField(default=False)
    title = models.BooleanField(default=False)
    mrp = models.BooleanField(default=False)
    price = models.BooleanField(default=False)
    shipping_price = models.BooleanField(default=False)
    manufacturer = models.BooleanField(default=False)
    star_rating = models.BooleanField(default=False)
    is_prime = models.BooleanField(default=False)
    customer_review = models.BooleanField(default=False)
    weight = models.BooleanField(default=False)
    color = models.BooleanField(default=False)
    size = models.BooleanField(default=False)
    package_dimensions = models.BooleanField(default=False)
    item_model_number = models.BooleanField(default=False)
    department = models.BooleanField(default=False)
    date_first_available = models.BooleanField(default=False)
    best_sellers_rank = models.BooleanField(default=False)
    bullet_points = models.BooleanField(default=False)
    image_urls = models.BooleanField(default=False)
    product_url = models.BooleanField(default=False)
    vedio_links = models.BooleanField(default=False)
    delivery_time = models.BooleanField(default=False)
    description = models.BooleanField(default=False)

    def __str__(self):
        return "Header Status"

    class Meta:
        verbose_name_plural = "Header Status"


class ScrapedData(models.Model):
    url = models.URLField()
    status = models.CharField(max_length=100, blank=True, null=True)



class UploadedFile(models.Model):
    file = models.FileField(upload_to='upload/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    


class ScrapeDataCount(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Scrape Data Count: {self.count}"