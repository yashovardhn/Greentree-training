from django.db import migrations


def add_sample_data(apps, schema_editor):
    # Get models
    Category = apps.get_model('store', 'Category')
    Product = apps.get_model('store', 'Product')
    
    # Create categories
    electronics = Category.objects.create(
        name='Electronics',
        description='Electronic devices and gadgets'
    )
    
    clothing = Category.objects.create(
        name='Clothing',
        description='Apparel and fashion items'
    )
    
    # Create products
    Product.objects.create(
        name='Smartphone',
        description='Latest model smartphone',
        price=699.99,
        category=electronics
    )
    
    Product.objects.create(
        name='Laptop',
        description='High-performance laptop',
        price=1299.99,
        category=electronics
    )
    
    Product.objects.create(
        name='T-Shirt',
        description='Cotton t-shirt',
        price=29.99,
        category=clothing
    )
    
    Product.objects.create(
        name='Headphones',
        description='Wireless noise-cancelling headphones',
        price=199.99,
        category=electronics
    )


def remove_sample_data(apps, schema_editor):
    # Get models
    Category = apps.get_model('store', 'Category')
    Product = apps.get_model('store', 'Product')
    
    # Delete all data
    Product.objects.all().delete()
    Category.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_category_alter_product_options_and_more'),
    ]

    operations = [
        migrations.RunPython(add_sample_data, remove_sample_data),
    ]
