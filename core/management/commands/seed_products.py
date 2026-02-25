from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Product
import requests


CAT_IMAGES = {
    'cupcakes': 'https://images.unsplash.com/photo-1551024506-0bcc5e0577f6?q=80&w=1200&auto=format&fit=crop',
    'cookies': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?q=80&w=1200&auto=format&fit=crop',
    'wedding': 'https://images.unsplash.com/photo-1526318472351-c75fcf070305?q=80&w=1200&auto=format&fit=crop',
    'birthday': 'https://images.unsplash.com/photo-1601655781325-c6efc7ee82d7?q=80&w=1200&auto=format&fit=crop',
    'delivery': 'https://images.unsplash.com/photo-1609401521835-8e9fd2dc69a1?q=80&w=1200&auto=format&fit=crop',
    'decorating': 'https://images.unsplash.com/photo-1589367920969-ab8e050bbb04?q=80&w=1200&auto=format&fit=crop',
}

SAMPLES = [
    ("Sweet Crumbs Vanilla Cupcake", 'cupcakes', 3.50, "Classic vanilla bean with buttercream frosting"),
    ("Chocolate Fudge Dream", 'cupcakes', 3.75, "Rich chocolate fudge with cocoa dusting"),
    ("Red Velvet Bliss", 'cupcakes', 3.75, "Signature red velvet with cream cheese frosting"),
    ("Artisanal Chocolate Chip", 'cookies', 2.50, "Chewy dough with premium dark chocolate chips"),
    ("Honey Oatmeal Raisin", 'cookies', 2.50, "Warm spices, honey, and plump raisins"),
    ("Elegant Wedding Tier", 'wedding', 180.00, "3-tier masterpiece with custom floral design"),
    ("Celebration Birthday Cake", 'birthday', 45.00, "8-inch cake with personalized message"),
    ("Sweet Crumbs Delivery", 'delivery', 10.00, "Premium delivery service inside city limits"),
    ("Professional Decorating Kit", 'decorating', 25.00, "Complete kit with piping bags, tips, and sprinkles"),
]


class Command(BaseCommand):
    help = 'Seed initial Product entries with images'

    def handle(self, *args, **options):
        created = 0
        for name, category, price, description in SAMPLES:
            product, was_created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'price': price,
                    'description': description,
                }
            )
            if was_created:
                created += 1
                # Fetch and attach image
                url = CAT_IMAGES.get(category)
                if url:
                    try:
                        import urllib.request
                        urllib.request.urlretrieve(url, f"temp_{category}.jpg")
                        with open(f"temp_{category}.jpg", 'rb') as f:
                            product.image.save(
                                f"{category}-{product.id}.jpg",
                                ContentFile(f.read()),
                                save=True
                            )
                        # Clean up temp file
                        import os
                        os.remove(f"temp_{category}.jpg")
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Could not download image for {product.name}: {e}"))
                        pass
        self.stdout.write(self.style.SUCCESS(f"Seed complete. Created {created} products."))


