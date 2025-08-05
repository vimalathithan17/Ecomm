from shop.models import Product
from django.core.files import File

# Example new products (update image paths as needed)
products = [
    {
        "name": "Classic White Shirt",
        "price": 29.99,
        "image_path": "media/products/shirt.jpg",  # Add this image to your media/products folder
        "description": "Premium cotton white shirt, perfect for formal and casual occasions."
    },
    {
        "name": "Running Sneakers",
        "price": 79.99,
        "image_path": "media/products/shoes.jpg",  # Add this image to your media/products folder
        "description": "Lightweight running sneakers with breathable mesh and cushioned sole."
    },
    {
        "name": "Leather Wallet",
        "price": 24.99,
        "image_path": "media/products/wallet.jpg",  # Add this image to your media/products folder
        "description": "Genuine leather wallet with multiple card slots and coin pocket."
    }
]

for prod in products:
    try:
        with open(prod["image_path"], "rb") as img_file:
            product = Product(
                name=prod["name"],
                price=prod["price"],
                description=prod["description"]
            )
            product.image.save(prod["image_path"].split("/")[-1], File(img_file), save=True)
        print(f"Added: {prod['name']}")
    except FileNotFoundError:
        print(f"Image not found for: {prod['name']} (expected at {prod['image_path']})")
