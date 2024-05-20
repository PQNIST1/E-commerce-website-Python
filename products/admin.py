from django.contrib import admin
from .models import Product
from .models import Category
from .models import ProductImage
from .models import ProductComment
from .models import BlogProduct
from .models import CartItem

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(ProductComment)
admin.site.register(BlogProduct)
admin.site.register(CartItem)

# Register your models here.
