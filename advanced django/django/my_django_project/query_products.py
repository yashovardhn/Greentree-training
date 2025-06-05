#!/usr/bin/env python3
"""
Script to query products with price > 50 in Electronics category.
Run with: python3 query_products.py
"""
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_django_project.settings')
django.setup()

def main():
    from store.models import Product
    from django.db.models import Q
    
    print("\nProducts where price > $50 and category contains 'Electronics':")
    print("-" * 60)
    
    # Query for products
    products = Product.objects.filter(
        price__gt=50,
        category__name__icontains='electronics'
    ).select_related('category')  # Optimize by joining with category in a single query
    
    if not products:
        print("No products found matching the criteria.")
        return
    
    # Print header
    print(f"{'ID':<5} | {'Product Name':<20} | {'Price':<10} | {'Category':<15}")
    print("-" * 60)
    
    # Print each product
    for product in products:
        print(f"{product.id:<5} | {product.name:<20} | ${product.price:<9.2f} | {product.category.name:<15}")
    
    print("\nTotal products found:", products.count())

if __name__ == "__main__":
    main()
