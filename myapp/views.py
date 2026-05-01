from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import *
from django.http import HttpResponseRedirect

from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)
from django.db.models import Count
from django.db.models import Q
from django.db.models import Sum
from django.contrib import messages
from django.db.models.functions import Random

# Create your views here.

def index(request):
    try:
        uid = request.session['log_id']


        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        proddata = product_detail.objects.filter(is_visible=True).order_by(Random())

        details = {
            'profiledata': profiledata,
            'proddata': proddata,
        }
        return render(request, 'index.html', details)
    except:
        pass

    proddata = product_detail.objects.filter(is_visible=True).order_by(Random())

    details = {
        'proddata': proddata,
    }
    return render(request, 'index.html', details)

def login_signup(request):
    try:
        uid = request.session['log_id']

        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        details = {
            'profiledata': profiledata,
        }
        return render(request, 'loginsignup.html', details)
    except:
        pass
    return render(request,'loginsignup.html')

def contactus(request):
    try:
        uid = request.session['log_id']


        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        details = {
            'profiledata': profiledata,
        }
        return render(request, 'contact.html', details)
    except:
        pass
    return render(request, 'contact.html')

def viewdata(request):
    if request.method == 'POST':
        name = request.POST.get("Name")
        email = request.POST.get("Email")
        phone = request.POST.get("Phone")
        address = request.POST.get("address")
        password = request.POST.get("Password")
        utype = request.POST.get("utype")

        try:
            alllogins = login.objects.get(Email=email)
        except login.DoesNotExist:
            alllogins = None

        if alllogins is None:
            if utype == "Seller":
                logindata = login(Email=email, Password=password, Phone=phone, Address=address,Name=name, is_seller=True)
                logindata.save()
                messages.success(request, 'Account Created Successfully and under verification. You can login and check status.')
            else:
                logindata = login(Email=email, Password=password, Phone=phone, Address=address, Name=name)
                logindata.save()
                messages.success(request, 'Account Created Successfully. you can login now')
        else:
            messages.error(request, 'Account already exist with same email')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'error occured')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def checklogin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        try:
            user = login.objects.get(Email=username, Password=password)
            request.session['log_user'] = user.Email
            request.session['log_id'] = user.id
            request.session.save()

        except login.DoesNotExist:
            user = None

        if user is not None:
            print("successfully logged in")
            messages.success(request, 'Successfully Logged In')

        else:
            print("not logged in")
            messages.error(request, 'Invalid USER ID')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect(index)

def logout(request):
    try:
        del request.session['log_user']
        del request.session['log_id']
    except:
        pass
    return redirect(index)


def yourprofile(request):
    try:
        uid = request.session['log_id']


        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        try:
            shopdata = shop.objects.get(L_id=login(id=uid))
        except shop.DoesNotExist:
            shopdata = None

        details = {
            'profiledata': profiledata,
            'shopdata': shopdata,
        }
        return render(request, 'yourprofile.html', details)
    except:
        pass
    return render(request,'yourprofile.html')

def editprofilesubmit(request):
    uid = request.session['log_id']
    if request.method == 'POST':
        uname = request.POST.get("Name")
        uemail = request.POST.get("Email")
        uphone = request.POST.get("Phone")
        uaddress = request.POST.get("address")

        logdata = login.objects.get(id=uid)
        logdata.Name = uname
        logdata.Email = uemail
        logdata.Phone = uphone
        logdata.Address = uaddress

        logdata.save()

        messages.success(request, 'Your profile has been updated successfully.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'error occured')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def changepwd(request):
    try:
        uid = request.session['log_id']
        userdata = login.objects.get(id=uid)
        pwd = userdata.Password

        if request.method == "POST":
            oldpwd = request.POST.get("oldpwd")
            newpwd = request.POST.get("newpwd")
            confirmpwd = request.POST.get("confirmpwd")

            if oldpwd == pwd:
                if newpwd == confirmpwd:
                    userdata.Password = newpwd
                    userdata.save()
                    messages.success(request, 'Password Updated Successfully.')
                    del request.session['log_user']
                    del request.session['log_id']
                    return redirect(login_signup)
                else:
                    messages.error(request, "New Password and confirm not same")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, "Invalid Old Password")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except userdata.DoesNotExist:
        messages.error(request, 'This account does not exist.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def completeprofilesubmit(request):
    uid = request.session['log_id']
    if request.method == 'POST':
        sname = request.POST.get("Name")
        sid = request.FILES['id']
        shopcert = request.FILES['shopcert']

        shopdata = shop(L_id=login(id=uid), seller_name=sname, owner_id=sid, shop_certificate=shopcert)
        shopdata.save()

        messages.success(request, 'Your profile completed successfully. Please wait for admin approval')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'error occured')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def editcompleteprofilesubmit(request):
    uid = request.session['log_id']
    if request.method == 'POST':
        sname = request.POST.get("sname")


        shopdata = shop.objects.get(L_id=login(id=uid))
        shopdata.seller_name = sname

        if 'id' in request.FILES:
            sid = request.FILES["id"]
            shopdata.owner_id = sid

        if 'shopcert' in request.FILES:
            shopcert = request.FILES["shopcert"]
            shopdata.shop_certificate = shopcert

        shopdata.save()

        messages.success(request, 'Your shop details has been updated successfully.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'error occured')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def addproduct(request):
    try:
        uid = request.session['log_id']


        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        try:
            shopdata = shop.objects.get(L_id=login(id=uid))
        except shop.DoesNotExist:
            shopdata = None

        catdata = product_category.objects.all()
        subcatdata = product_subcategory.objects.all()

        details = {
            'profiledata': profiledata,
            'shopdata': shopdata,
            'catdata': catdata,
            'subcatdata': subcatdata,
        }
        return render(request, 'addproduct.html', details)
    except:
        pass
    return render(request,'addproduct.html')

# views.py

from django.http import JsonResponse

def get_subcategories(request):
    cat_id = request.GET.get('cat_id')
    subcategories = product_subcategory.objects.filter(Pro_Cat_id=cat_id)
    data = [{'id': sub.id, 'name': sub.Product_subcategory_name} for sub in subcategories]
    return JsonResponse(data, safe=False)

def addproductsubmit(request):
    uid = request.session['log_id']
    if request.method == 'POST':
        pname = request.POST.get("pname")
        bname = request.POST.get("bname")
        price = request.POST.get("price")
        pcat = request.POST.get("pcat")
        psubcat = request.POST.get("psubcat")
        pdesc = request.POST.get("pdesc")
        pimage = request.FILES['pimage']


        proddata = product_detail(L_id=login(id=uid), Pro_name=pname,Pro_brandname=bname,Pro_Cat=product_category(id=pcat),Pro_subcat=product_subcategory(id=psubcat), Pro_image=pimage, Pro_description=pdesc,Pro_price=price)
        proddata.save()

        messages.success(request, 'Your product is added.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'error occured')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

from django.shortcuts import render, redirect
from .models import product_detail, product_image

def add_product_image(request):
    uid = request.session['log_id']
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = product_detail.objects.get(id=product_id)
        images = request.FILES.getlist('product_images')
        for image in images:
            product_image.objects.create(L_id=login(id=uid),Product_id=product, Pro_image=image)
        return redirect('/')  # Replace 'success_page' with the name of your success URL
    else:
        products = product_detail.objects.all()
        return render(request, 'add_product_image.html', {'products': products})

def manageproduct(request):
    try:
        uid = request.session['log_id']


        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        try:
            shopdata = shop.objects.get(L_id=login(id=uid))
        except shop.DoesNotExist:
            shopdata = None

        proddata = product_detail.objects.filter(L_id=login(id=uid), is_visible=True)
        catdata = product_category.objects.all()
        subcatdata = product_subcategory.objects.all()

        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(proddata, 3)  # Set the number of items per page

        try:
            proddata = paginator.page(page)
        except PageNotAnInteger:
            proddata = paginator.page(1)
        except EmptyPage:
            proddata = paginator.page(paginator.num_pages)


        details = {
            'profiledata': profiledata,
            'shopdata': shopdata,
            'proddata': proddata,
            'catdata': catdata,
            'subcatdata': subcatdata,
        }
        return render(request, 'manageproduct.html', details)
    except:
        pass
    return render(request,'manageproduct.html')

def editproduct(request, epid):
    try:
        uid = request.session['log_id']


        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        try:
            shopdata = shop.objects.get(L_id=login(id=uid))
        except shop.DoesNotExist:
            shopdata = None

        proddata = product_detail.objects.get(id=epid)
        catdata = product_category.objects.all()
        subcatdata = product_subcategory.objects.all()


        details = {
            'profiledata': profiledata,
            'shopdata': shopdata,
            'proddata': proddata,
            'catdata': catdata,
            'subcatdata': subcatdata,
        }
        return render(request, 'editproduct.html', details)
    except:
        pass
    return render(request,'editproduct.html')

def editproductdetails(request):
    uid = request.session['log_id']
    if request.method == 'POST':
        pid = request.POST.get("pid")
        pname = request.POST.get("pname")
        price = request.POST.get("price")
        pdesc = request.POST.get("pdesc")
        pcat = request.POST.get("pcat")
        psubcat = request.POST.get("psubcat")

        selcat = product_category.objects.get(id=pcat)
        selsubcat = product_subcategory.objects.get(id=psubcat)

        mylogin = login.objects.get(id=uid)
        productdata = product_detail.objects.get(id=pid)
        productdata.L_id = mylogin
        productdata.Pro_name = pname
        productdata.Pro_description = pdesc
        productdata.Pro_price = price
        productdata.Pro_Cat = selcat
        productdata.Pro_subcat = selsubcat

        if 'pimage' in request.FILES:
            pimage = request.FILES["pimage"]
            productdata.Pro_image = pimage

        productdata.save()

        messages.success(request, 'Product details has been updated successfully.')
        return redirect(manageproduct)
    else:
        messages.error(request, 'error occured')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def removeprod(request, rpid):
    try:
        uid = request.session['log_id']


        selprod = product_detail.objects.get(id=rpid)
        selprod.is_visible = False
        selprod.save(update_fields=['is_visible'])

        messages.warning(request, 'Product Removed.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def allproducts(request):
    try:
        uid = request.session['log_id']

        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        proddata = product_detail.objects.filter(is_visible=True)
        catdata = product_category.objects.all()
        subcatdata = product_subcategory.objects.all()

        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(proddata, 3)  # Set the number of items per page

        try:
            proddata = paginator.page(page)
        except PageNotAnInteger:
            proddata = paginator.page(1)
        except EmptyPage:
            proddata = paginator.page(paginator.num_pages)

        details = {
            'profiledata': profiledata,
            'proddata': proddata,
            'catdata': catdata,
            'subcatdata': subcatdata,
        }
        return render(request, 'allproducts.html', details)
    except:
        pass
    proddata = product_detail.objects.filter(is_visible=True)
    catdata = product_category.objects.all()
    subcatdata = product_subcategory.objects.all()

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(proddata, 3)  # Set the number of items per page

    try:
        proddata = paginator.page(page)
    except PageNotAnInteger:
        proddata = paginator.page(1)
    except EmptyPage:
        proddata = paginator.page(paginator.num_pages)

    details = {
        'proddata': proddata,
        'catdata': catdata,
        'subcatdata': subcatdata,
    }
    return render(request, 'allproducts.html', details)

def catwiseprod(request, cpid):
    try:
        uid = request.session['log_id']

        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        proddata = product_detail.objects.filter(is_visible=True, Pro_Cat=product_category(id=cpid))
        catdata = product_category.objects.all()
        subcatdata = product_subcategory.objects.all()

        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(proddata, 3)  # Set the number of items per page

        try:
            proddata = paginator.page(page)
        except PageNotAnInteger:
            proddata = paginator.page(1)
        except EmptyPage:
            proddata = paginator.page(paginator.num_pages)

        details = {
            'profiledata': profiledata,
            'proddata': proddata,
            'catdata': catdata,
            'subcatdata': subcatdata,
        }
        return render(request, 'catwiseprod.html', details)
    except:
        pass
    proddata = product_detail.objects.filter(is_visible=True, Pro_Cat=product_category(id=cpid))
    catdata = product_category.objects.all()
    subcatdata = product_subcategory.objects.all()

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(proddata, 3)  # Set the number of items per page

    try:
        proddata = paginator.page(page)
    except PageNotAnInteger:
        proddata = paginator.page(1)
    except EmptyPage:
        proddata = paginator.page(paginator.num_pages)

    details = {
        'proddata': proddata,
        'catdata': catdata,
        'subcatdata': subcatdata,
    }
    return render(request, 'catwiseprod.html', details)

def subcatprod(request, scpid):
    try:
        uid = request.session['log_id']

        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        proddata = product_detail.objects.filter(is_visible=True, Pro_subcat=product_subcategory(id=scpid))
        catdata = product_category.objects.all()
        subcatdata = product_subcategory.objects.all()

        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(proddata, 3)  # Set the number of items per page

        try:
            proddata = paginator.page(page)
        except PageNotAnInteger:
            proddata = paginator.page(1)
        except EmptyPage:
            proddata = paginator.page(paginator.num_pages)

        details = {
            'profiledata': profiledata,
            'proddata': proddata,
            'catdata': catdata,
            'subcatdata': subcatdata,
        }
        return render(request, 'subcatprod.html', details)
    except:
        pass
    proddata = product_detail.objects.filter(is_visible=True, Pro_subcat=product_subcategory(id=scpid))
    catdata = product_category.objects.all()
    subcatdata = product_subcategory.objects.all()

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(proddata, 3)  # Set the number of items per page

    try:
        proddata = paginator.page(page)
    except PageNotAnInteger:
        proddata = paginator.page(1)
    except EmptyPage:
        proddata = paginator.page(paginator.num_pages)

    details = {
        'proddata': proddata,
        'catdata': catdata,
        'subcatdata': subcatdata,
    }
    return render(request, 'subcatprod.html', details)


def viewprod(request, pdid):
    try:
        uid = request.session['log_id']

        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        proddata = product_detail.objects.get(id=pdid)
        images = product_image.objects.filter(Product_id=proddata)
        details = {
            'profiledata': profiledata,
            'proddata': proddata,
            'images': images
        }
        return render(request, 'viewprod.html', details)
    except:
        pass
    proddata = product_detail.objects.get(id=pdid)

    details = {
        'proddata': proddata,
    }
    return render(request, 'viewprod.html', details)


def addtocart(request):
    if request.method == 'POST':

        uid = request.session['log_id']
        quantity = request.POST.get('quantity')
        proid = request.POST.get('pid')


        getprod = product_detail.objects.get(id=proid)
        prodprice = getprod.Pro_price
        prodname = getprod.Pro_name
        iquantity = int(quantity)
        finalprice = prodprice * iquantity



        cartdata = product_cart()
        cartdata.L_id_id = uid
        cartdata.Product_id_id = proid
        cartdata.Product_name = prodname
        cartdata.Price = prodprice
        cartdata.Quantity = iquantity
        cartdata.Final_price = finalprice

        cartdata.save()


        # Redirect or render a success page
        messages.success(request, 'Added to cart.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'Error adding')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
import razorpay
from django.db import transaction
from django.core.serializers import serialize
import json
def mycart(request):
    uid = request.session.get('log_id')  # Use `.get()` to avoid KeyError
    if not uid:
        messages.error(request, "User not authenticated.")
        return redirect('login')

    cart_items = product_cart.objects.filter(L_id__id=uid, Order_status=0)
    total_deposite = sum(((item.Product_id.Pro_price * item.Quantity) * 0.25) for item in cart_items)

    total_price2 = 0  # Initialize total price

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        payment_mode = request.POST.get('payment_mode')

        if not start_date or not end_date:
            messages.error(request, "Please select a start and end date.")
            return redirect('mycart')

        # In your mycart view function:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            total_days = (end - start).days  # REMOVED the +1 for exclusive counting
            if total_days < 1:  # Changed from <= 0 to < 1
                messages.error(request, "Rental period must be at least 1 day.")
                return redirect('mycart')
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('mycart')

        if total_days <= 0:
            messages.error(request, "End date must be after start date.")
            return redirect('mycart')

            # Calculate total price: (price × quantity) × days
        total_price2 = 0
        for item in cart_items:
            item.Final_price = (item.Product_id.Pro_price * item.Quantity) * total_days
            total_price2 += item.Final_price
            item.save()



        context = {
            'cartitems': cart_items,
            'total_price2': total_price2,
            'start_date': start_date,
            'end_date': end_date,
            "total_deposite" : total_deposite
        }

        if payment_mode == 'online':
            # Razorpay integration
            client = razorpay.Client(auth=('rzp_test_VQhEfe2NCXbbwI', '2ibreCYL78DA3kjOhobCvz0f'))
            amount = int((total_price2+total_deposite)* 100)  # Convert to paisa
            data = {
                "amount": amount,
                "currency": "INR",
                "receipt": f"order_{uid}",
                "payment_capture": 1
            }

            try:
                razorpay_payment = client.order.create(data=data)
                razorpay_order_id = razorpay_payment['id']

                with transaction.atomic():
                    order, created = product_order.objects.get_or_create(
                        user=login(id=uid),
                        razorpay_order_id=razorpay_order_id,
                        defaults={'amount': (total_price2+total_deposite), 'start_date': start_date,
                                  'end_date': end_date, 'payment_mode': 'online'},
                    )
                    cart_items.update(Order_id=order.id, Order_status=1)

                context.update({
                    'razorpay_payment': {
                        'amount': amount,
                        'order_id': razorpay_order_id,
                        'key': "rzp_test_VQhEfe2NCXbbwI",
                    },
                    "total_deposite":total_deposite
                })
                return render(request, 'mycart.html', context)

            except razorpay.errors.BadRequestError as e:
                messages.error(request, f'BadRequestError: {str(e)}')
            except razorpay.errors.ServerError as e:
                messages.error(request, f'ServerError: {str(e)}')
            except Exception as e:
                messages.error(request, f'Unexpected error: {str(e)}')

        elif payment_mode == 'offline':
            address = request.POST.get("address")
            reference = request.POST.get("reference")
            remark = request.POST.get("remark")

            with transaction.atomic():
                order = product_order.objects.create(
                    user=login(id=uid),
                    amount=(total_price2+total_deposite),
                    address=address,
                    start_date=start_date,
                    end_date=end_date,
                    offline_reference=reference,
                    offline_remarks=remark,
                    payment_mode='offline',
                    status='Pending',
                )
                cart_items.update(Order_id=order.id, Order_status=1)

            messages.success(request, "Offline payment details submitted successfully.")
            return redirect('index')

        else:
            messages.error(request, "Invalid payment mode selected.")
            return redirect('mycart')

    cartitems_json = json.dumps([
        {
            "Product_id": item.Product_id.id,
            "Pro_price": float(item.Product_id.Pro_price),
            "Quantity": item.Quantity,
            "Final_price": float(item.Final_price if item.Final_price else 0),
        }
        for item in cart_items
    ])

    return render(request, 'mycart.html', {
        "cartitems": cart_items,
        "cartitems_json": cartitems_json,
        "total_price2": sum((item.Product_id.Pro_price * item.Quantity) for item in cart_items),
        "total_deposite" : total_deposite
    })


from django.core.mail import send_mail
from django.shortcuts import render, redirect
import razorpay

def success(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature'],
    }

    client = razorpay.Client(
        auth=('rzp_test_VQhEfe2NCXbbwI', '2ibreCYL78DA3kjOhobCvz0f')
    )

    try:
        # Verify the payment signature
        client.utility.verify_payment_signature(params_dict)

        # Fetch the existing order
        order = product_order.objects.get(razorpay_order_id=response['razorpay_order_id'])

        # Update the payment details
        order.razorpay_payment_id = response['razorpay_payment_id']
        order.razorpay_signature = response['razorpay_signature']
        order.status = 'Paid'
        order.save()

        # Update the cart items' status to indicate they've been paid for
        product_cart.objects.filter(L_id=order.user, Order_status=0).update(Order_status=1, Order_id=order.id)

        # Send a confirmation email
        subject = 'Payment Successful'
        message = f"Dear {order.user.Name},\n\n" \
                  f"Your payment for Order ID {order.id} has been successfully processed. Thank you for choosing us!\n\n" \
                  f"Best regards,\nYour Team"
        sender_email = 'dpoza8125@gmail.com'
        recipient_email = [order.user.Email]

        send_mail(subject, message, sender_email, recipient_email, fail_silently=False)

        return render(request, 'success.html', {'status': True})

    except razorpay.errors.SignatureVerificationError:
        print("Signature verification failed.")
        return render(request, 'success.html', {'status': False})

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return render(request, 'success.html', {'status': False})
def removefromcart(request, rcid):
    product_cart.objects.get(id=rcid).delete()
    messages.error(request, 'Removed from Cart.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def checkout(request):
    try:
        uid = request.session['log_id']

        userdata = login.objects.get(id=uid)

        cartitems = product_cart.objects.filter(L_id=login(id=uid), Order_status=0)
        carttotal = product_cart.objects.filter(L_id=login(id=uid), Order_status=0).aggregate(Sum("Final_price"))
        carttotal = carttotal.get("Final_price__sum")

        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        details = {
            'userdata': userdata,
            'cartitems': cartitems,
            'carttotal': carttotal,
            'profiledata': profiledata,
        }
        return render(request, 'checkout.html', details)
    except:
        pass

    return render(request, 'checkout.html')

def placeorder(request):
    uid = request.session['log_id']
    if request.method == 'POST':
        paymentMethod = request.POST.get("paymentopt")
        oname = request.POST.get("oname")
        ophone = request.POST.get("ophone")
        saddress = request.POST.get("oaddress")
        grandtotal = request.POST.get("grandtotal")
        number_int = int(grandtotal)

        if paymentMethod == "Card":
            orderdata = product_order(L_id=login(id=uid),Name=oname,Phone=ophone, Address=saddress, Total_amount=number_int,
                                      Payment_status="online", order_status="Placed")
            orderdata.save()

            lasstid = product_order.objects.latest('id')

            print(lasstid)

            objid = lasstid.id
            print(objid)

            obj = product_cart.objects.filter(L_id=login(id=uid), Order_status=0)
            for object in obj:
                object.Order_id = objid
                object.Order_status = 1
                object.save()

            messages.success(request, 'Order Placed Successfully.')
            return redirect(orderplaced)

        else:
            orderdata = product_order(L_id=login(id=uid),Name=oname,Phone=ophone, Address=saddress, Total_amount=number_int,
                                      Payment_status="Cash On Delivery", order_status="Placed")
            orderdata.save()

            lasstid = product_order.objects.latest('id')

            print(lasstid)

            objid = lasstid.id
            print(objid)

            obj = product_cart.objects.filter(L_id=login(id=uid), Order_status=0)
            for object in obj:
                object.Order_id = objid
                object.Order_status = 1
                object.save()


            messages.success(request, 'Order Placed Successfully.')
            return redirect(orderplaced)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def myorders(request):
    try:
        uid = request.session['log_id']

        userdata = login.objects.get(id=uid)

        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        orderdata = product_order.objects.filter(user=login(id=uid))


        details = {
            'userdata': userdata,
            'orderdata': orderdata,
            'profiledata': profiledata,
        }
        return render(request, 'orders.html', details)
    except:
        pass

    return render(request, 'orders.html')

def singleorder(request, yoid):
    try:
        uid = request.session['log_id']

        order = product_order.objects.get(id=yoid, user=uid)
        orderid = order.id
        cartdetail = product_cart.objects.filter(L_id=uid, Order_id=orderid, Order_status=1)

        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        details = {
            'cartdetail': cartdetail,
            'profiledata': profiledata,

        }
        return render(request, 'yourordersingle.html', details)
    except:
        pass
    return render(request, 'yourordersingle.html')

def orderplaced(request):
    try:
        uid = request.session['log_id']

        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        details = {
            'profiledata': profiledata,

        }
        return render(request, 'orderplaced.html', details)
    except:
        pass
    return render(request, 'orderplaced.html')

def SubmitReview(request):
    uid = request.session['log_id']
    if request.method == 'POST':
        ratings = request.POST.get("input-1")
        feedback = request.POST.get("feedback")

        subreview = FEEDBACK_TABLE(L_ID=login(id=uid), RATINGS=ratings, COMMENT=feedback)
        subreview.save()
        messages.success(request, 'Review Submitted Successfully.')

    return redirect(index)


def cancelorder(request, coid):
    uid = request.session['log_id']
    ordupd = product_order.objects.get(id=coid)
    ordupd.status = 'Cancelled'
    ordupd.save()
    messages.warning(request, 'Order Cancelled')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def sellerorders(request):
    try:
        uid = request.session['log_id']

        userdata = login.objects.get(id=uid)

        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        proddatas = product_detail.objects.filter(L_id=login(id=uid))
        orderdata = product_cart.objects.filter(Product_id__in=proddatas, Order_status=1)
        print("hi")


        # Step 4: Fetch product_order data based on the extracted Order IDs

        details = {
                'userdata': userdata,
                'orderdata': orderdata,
                'profiledata': profiledata,
            }
        return render(request, 'sellerorders.html', details)
    except:
        pass

    return render(request, 'sellerorders.html')


def singleorderseller(request, syoid):
    try:
        uid = request.session['log_id']

        proddatas = product_detail.objects.filter(L_id=login(id=uid))
        cartdetail = product_cart.objects.filter(Order_id=syoid,Product_id__in=proddatas)

        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        details = {
            'cartdetail': cartdetail,
            'profiledata': profiledata,

        }
        return render(request, 'singleorderseller.html', details)
    except:
        pass
    return render(request, 'singleorderseller.html')

def submitcontact(request):
    uid = request.session['log_id']
    if request.method == 'POST':
        con_name = request.POST.get("con_name")
        con_email = request.POST.get("con_email")
        con_message = request.POST.get("con_message")

        subreview = Contact(name=con_name,email=con_email, message=con_message)
        subreview.save()
        messages.success(request, 'Response recorded successfully.')
        return redirect(index)

def searchresults(request):
    try:
        uid = request.session['log_id']
        search = request.GET.get('search')

        try:
            profiledata = login.objects.get(id=uid)
        except login.DoesNotExist:
            profiledata = None

        productdata = product_detail.objects.all().filter(Pro_name__icontains=search, is_visible=True)

        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(productdata, 3)  # Set the number of items per page

        try:
            productdata = paginator.page(page)
        except PageNotAnInteger:
            productdata = paginator.page(1)
        except EmptyPage:
            productdata = paginator.page(paginator.num_pages)

        details = {
            'profiledata': profiledata,
            'productdata': productdata,
        }
        return render(request, 'searchresult.html', details)
    except:
        pass
    search = request.POST.get('search')
    productdata = product_detail.objects.all().filter(Pro_name__icontains=search, is_visible=True)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(productdata, 3)  # Set the number of items per page

    try:
        productdata = paginator.page(page)
    except PageNotAnInteger:
        productdata = paginator.page(1)
    except EmptyPage:
        productdata = paginator.page(paginator.num_pages)

    details = {
        'productdata': productdata,
    }
    return render(request, 'searchresult.html', details)

def registerpage(request):
    return render(request,"register.html")