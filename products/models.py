from django.db import models
from django.utils import timezone
from django.conf import settings

from user.models import UserAccount
# Create your models here.
class Category(models.Model):
    # Sử dụng AutoField để tạo ra một trường int tự tăng
    # primary_key=True để chỉ định khóa chính cho bảng
    id = models.AutoField(primary_key=True)
    # Sử dụng CharField để tạo ra một trường kiểu varchar, max_length là attribute bắt buộc
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    # Cho phép một trường varchar có thể nhận giá trị null
    icon_url = models.CharField(max_length=128, null=True)
    # Sử dụng DateTimeField để tạo ra một trường kiểu String dạng Datetime
    # default=timezone.now sẽ gán giá trị mặc định là thời điểm tạo record
    created_at = models.DateTimeField(default=timezone.now)
    # auto_now sẽ tự động gán giá trị datetime mới mỗi khi record được update
    updated_at = models.DateTimeField(auto_now=True)
    # delete_at dùng để soft delete
    deleted_at = models.DateTimeField(null=True)
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=3)
    price = models.FloatField()
    discount = models.IntegerField()
    amount = models.IntegerField()
    is_public = models.BooleanField(null=True)
    thumbnail = models.CharField(max_length=128)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products', null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    class Meta:
        # Sắp xếp mặc định khi query là giảm dần theo ngày tạo
        ordering = ['-created_at']
        indexes = [
        # Chỉ mục index sẽ đánh theo field created_at
        models.Index(fields=['created_at'])
        ]
class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=128)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_images', null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
class ProductComment(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.IntegerField()
    comment = models.CharField(max_length=512)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_comments', null=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
class BlogProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    content = models.TextField()
    image_url = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
class CartItem(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)