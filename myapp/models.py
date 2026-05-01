from django.db import models
from django.utils.safestring import mark_safe
from django.contrib import messages


# Create your models here.
class login(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.EmailField()
    Password = models.CharField(max_length=25)
    Phone = models.BigIntegerField()
    Address = models.CharField(max_length=128)
    is_seller = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    admin_comment = models.CharField(max_length=200, default="Account created. Under verification.")

    def __str__(self):
        return self.Name

class shop(models.Model):
    L_id = models.ForeignKey(login, on_delete=models.CASCADE, default="")
    seller_name = models.CharField(max_length=100)
    owner_id = models.ImageField(upload_to="photos")
    shop_certificate = models.ImageField(upload_to="photos", default="")
    is_verified = models.BooleanField(default=False)

    def ownerid_images(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.owner_id.url))

    ownerid_images.allow_tags = True

    def shopcertificate(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.shop_certificate.url))

    shopcertificate.allow_tags = True

    def __str__(self):
        return self.seller_name

    def save(self, *args, **kwargs):
        try:
            existing_instance = self._meta.model.objects.get(pk=self.pk)
        except self._meta.model.DoesNotExist:
            existing_instance = None

        if existing_instance and self.is_verified != existing_instance.is_verified:
            self.L_id.is_verified = self.is_verified
            self.L_id.admin_comment = "Account verified" if self.is_verified else "Account created. Under verification."
            self.L_id.save()
        super(shop, self).save(*args, **kwargs)


class product_category(models.Model):
    Product_category_name = models.CharField(max_length=25)

    def __str__(self):
        return self.Product_category_name


class product_subcategory(models.Model):
    Product_subcategory_name = models.CharField(max_length=25)
    Pro_Cat = models.ForeignKey(product_category, on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.Product_subcategory_name

class product_detail(models.Model):
    L_id = models.ForeignKey(login, on_delete=models.CASCADE, default="")
    Pro_name = models.CharField(max_length=70)
    Pro_brandname = models.CharField(max_length=50, default="Prexa Wear")
    Pro_Cat = models.ForeignKey(product_category, on_delete=models.CASCADE, default="")
    Pro_subcat = models.ForeignKey(product_subcategory, on_delete=models.CASCADE, default="")
    Pro_image = models.ImageField(upload_to="photos")
    Pro_description = models.CharField(max_length=500)
    Pro_price = models.IntegerField()
    is_visible = models.BooleanField(default=True)
    added_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.Pro_name

    def Pro_images(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.Pro_image.url))

    Pro_images.allow_tags = True

class product_image(models.Model):
    L_id = models.ForeignKey(login, on_delete=models.CASCADE, default="", null=True,blank=True)
    Product_id = models.ForeignKey(product_detail, on_delete=models.CASCADE, default="", null=True,blank=True)
    Pro_image = models.ImageField(upload_to="photos")

    def Pro_images(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.Pro_image.url))

    Pro_images.allow_tags = True
class product_cart(models.Model):
    Product_id = models.ForeignKey(product_detail, on_delete=models.CASCADE, default="")
    L_id = models.ForeignKey(login, on_delete=models.CASCADE, default="")
    Product_name = models.CharField(max_length=300)
    Date_time = models.DateTimeField(auto_now=True, editable=False)
    Price = models.IntegerField(default=100)
    Quantity = models.IntegerField()
    Final_price = models.IntegerField()
    Order_id = models.IntegerField(default=0)
    Order_status = models.IntegerField(default=0)

from django.utils import timezone
from django.utils.timezone import now

class product_order(models.Model):
    PAYMENT_MODE_CHOICES = [
        ('online', 'Online Payment'),
        ('offline', 'Offline Payment'),
    ]

    PAYMENT_STATUS = (
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
        ("Cancelled", "Cancelled")
    )

    user = models.ForeignKey(login, on_delete=models.CASCADE)
    amount = models.FloatField()  # Store the total order amount
    start_date = models.DateField(null=True, blank=True)  # Added field
    end_date = models.DateField(null=True, blank=True)  # Added field
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODE_CHOICES)  # Payment mode
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="Pending")
    offline_reference = models.CharField(max_length=255, blank=True, null=True)  # Reference number for offline payment
    offline_remarks = models.TextField(blank=True, null=True)  # Optional remarks for offline payments
    address = models.TextField(blank=True, null=True)  # Optional remarks for offline payments
    timestamp = models.DateTimeField(default=timezone.now)

    def get_total_amount(self):
        return self.amount


class feedback(models.Model):
    Name=models.CharField(max_length=50,default="")
    Email=models.EmailField(default="")
    Comment=models.CharField(max_length=250,default="")


class FEEDBACK_TABLE(models.Model):
    L_ID = models.ForeignKey(login, on_delete=models.CASCADE, default="")
    RATINGS = models.CharField(max_length=300)
    COMMENT = models.CharField(max_length=300, default="")



class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name