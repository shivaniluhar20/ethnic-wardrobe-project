from django.contrib import admin
from .models import login, shop, product_category, product_subcategory, product_detail, product_cart, product_order, feedback, FEEDBACK_TABLE, Contact, product_image
# Define the admin classes for each model
class loginAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Email', 'Phone', 'is_verified','is_seller')
    list_filter = ('is_verified',)
    search_fields = ('Name', 'Email')

class shopAdmin(admin.ModelAdmin):
    list_display = ('seller_name', 'L_id', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('seller_name',)

class product_categoryAdmin(admin.ModelAdmin):
    list_display = ('Product_category_name',)

class product_subcategoryAdmin(admin.ModelAdmin):
    list_display = ('Product_subcategory_name', 'Pro_Cat')

class product_detailAdmin(admin.ModelAdmin):
    list_display = ('L_id','Pro_name','Pro_brandname', 'Pro_Cat', 'Pro_subcat', 'Pro_price', 'added_date','is_visible')
    list_filter = ('Pro_Cat', 'Pro_subcat')
    search_fields = ('Pro_name',)

class product_imageAdmin(admin.ModelAdmin):
    list_display = ('L_id','Product_id','Pro_image')


class product_cartAdmin(admin.ModelAdmin):
    list_display = ('id','Product_name', 'Product_id', 'L_id','Price','Quantity','Final_price', 'Date_time', 'Order_status','Order_id')
    list_filter = ('Order_status',)
    search_fields = ('Product_name',)

class product_orderAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'start_date','end_date','razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature','payment_mode','status','offline_reference','offline_remarks','address')
    list_filter = ['payment_mode']
    search_fields =['user__Name']

class feedbackAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Email', 'Comment')

class FEEDBACK_TABLEAdmin(admin.ModelAdmin):
    list_display = ('L_ID', 'RATINGS', 'COMMENT')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'timestamp')

# Register your models with the customized admin classes
admin.site.register(login, loginAdmin)
admin.site.register(shop, shopAdmin)
admin.site.register(product_category, product_categoryAdmin)
admin.site.register(product_subcategory, product_subcategoryAdmin)
admin.site.register(product_detail, product_detailAdmin)
admin.site.register(product_cart, product_cartAdmin)
admin.site.register(product_order, product_orderAdmin)
#admin.site.register(feedback, feedbackAdmin)
#admin.site.register(FEEDBACK_TABLE, FEEDBACK_TABLEAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(product_image, product_imageAdmin)