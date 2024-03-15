# templatetags/categories_tags.py

from django import template

register = template.Library()
CATEGORIES = {
    'FASHION': ['clothing', 'shoes', 'watches', 'Jewellery', 'Wallets', 'Eyewear'],
    'ELECTRONICS': ['Laptops', 'Smartphones', 'Tablets', 'Cameras', 'Headphones'],
    'BOOKS': ['Fiction', 'Non-Fiction', 'Mystery', 'Science Fiction', 'Romance'],
    'Toys & Games': ['Board Games', 'Video Games', 'Outdoor Toys', 'Puzzles'],
    'Health & Personal Care': ['Vitamins & Supplements', 'Personal Care', 'Fitness Equipment'],
    'Home & Kitchen': ['Kitchen Appliances', 'Home Decor', 'Furniture', 'Bedding']
}
@register.simple_tag
def render_dropdown(category_name):
    if category_name in CATEGORIES:
        subcategories = CATEGORIES[category_name]
        dropdown_html = f'<select name="{category_name}_subcategory">'
        for subcategory in subcategories:
            dropdown_html += f'<option value="{subcategory}">{subcategory}</option>'
        dropdown_html += '</select>'
        return dropdown_html
    else:
        return ''
