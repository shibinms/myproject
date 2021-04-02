import random
from datetime import date

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from SCM_System.models import branch, login, manager, raw_material, product, notification, request_master


def adm_login(request):
    return render(request,"login.html")
def adm_login_post(request):
    username=request.POST['usname']
    password=request.POST['password']
    try:
        res=login.objects.get(username=username,password=password)
        request.session['lid']=res.pk
        if res.user_type=='admin':
            return adm_homepage(request)
        elif res.user_type=='manager':
            return manager_homepage(request)
        elif res.user_type=='production_staff':
            return staff_homepage(request)
        elif res.user_type=='sales_staff':
            return sale_homepage()
        else:
            return HttpResponse("Invalid!!")
    except Exception as e:
        return e

def manager_homepage(request):
    return render(request,"admin/homepage.html")

def staff_homepage(request):
    return render(request,"admin/homepage.html")
def sale_homepage(request):
    return render(request,"admin/homepage.html")


def adm_add_branch(request):
    return render(request,"admin/add_branch.html")

def adm_add_branch_post(request):
    branch_name=request.POST['branchname']
    place=request.POST['bplace']
    district=request.POST['bdistrict']
    state=request.POST['bstate']
    country=request.POST['bcountry']
    pin=request.POST['bpin']
    email=request.POST['bemail']
    phone=request.POST['bphone']
    qry=branch(branch_name=branch_name, place=place, district=district, state=state, country=country, pin=pin, email=email, phone=phone)
    qry.save()
    return adm_view_branch(request)

def adm_view_branch(request):
    res=branch.objects.all()
    return render(request,"admin/view_branch.html", {'data':res})

def adm_add_manager(request):
    res = branch.objects.all()
    return render(request, "admin/add_manager.html", {'data':res})

def adm_add_manager_post(request):
    manager_name=request.POST['mname']
    dob=request.POST['mdob']
    gender=request.POST['radio']
    branch_name=request.POST['bname']
    place=request.POST['place']
    district=request.POST['district']
    state = request.POST['state']
    pin=request.POST['pin']
    email=request.POST['email']
    phone=request.POST['phone']
    myfile=request.FILES['image']
    fs = FileSystemStorage()
    filename=fs.save(myfile.name, myfile)
    image = fs.url(filename)
    password=random.randint(0000,9999)
    log=login(username=email, password=password, user_type="manager")
    log.save()
    branch_id=branch(branch_name=branch_name)
    branch_id.save()
    qry = manager(manager_name=manager_name, dob=dob, gender=gender, BRANCH=branch_id, place=place, district=district, pin=pin, email=email, phone=phone, state=state, profile_img=image,LOGIN=log)
    qry.save()
    return adm_view_manager(request)


def adm_add_product(request):
    return render(request, "admin/add_product.html")

def adm_add_product_post(request):
    product_name=request.POST['productname']
    types=request.POST['type']
    price=request.POST['price']
    myfile = request.FILES['image']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    image = fs.url(filename)
    description=request.POST['description']
    qry = product(product_name=product_name, product_type=types, price=price, image=image, description=description)
    qry.save()
    return adm_view_product(request)

def adm_add_raw_material(request):
    return render(request, "admin/add_raw_material.html")

def adm_add_raw_material_post(request):
    material_name=request.POST['materialname']
    gsm=request.POST['gsm']
    price=request.POST['price']
    qry=raw_material(raw_material_name=material_name,gsm=gsm,price=price)
    qry.save()
    return adm_view_raw_material(request)
def adm_allocate_raw_material(request):
    return render(request,"admin/allocate_raw_material.html")
def adm_edit_branch(request):
    res = branch.objects.all()
    return render(request,"admin/edit_branch.html", {'data':res})
def adm_edit_manager(request):
    return render(request,"admin/edit_manager.html")
def adm_edit_product(request):
    return render(request,"admin/edit_product.html")
def adm_edit_raw_material(request):
    return render(request,"admin/edit_raw_material.html")
def adm_send_notification(request):
    res = branch.objects.all()
    return render(request,"admin/send_notification.html", {'data':res})
def adm_send_notification_post(request):
    title = request.POST['title']
    message = request.POST['message']
    branch_id = request.POST["branch_name"]
    qry = notification(date=date.today(), title=title, message=message, BRANCH_id=branch_id)
    qry.save()
    return adm_view_notification(request)

def adm_view_allocate_report(request):
    return render(request,"admin/view_allocate_report.html")
def adm_view_manager(request):
    res = manager.objects.all()
    return render(request,"admin/view_manager.html", {'data':res})
def adm_view_material_allocated(request):
    return render(request,"admin/view_material_allocated.html")
def adm_view_material_requested(request):
    return render(request,"admin/view_material_requested.html")
def adm_view_notification(request):
    res = notification.objects.all()
    return render(request,"admin/view_notification.html", {'data':res})
def adm_view_product(request):
    res = product.objects.all()
    return render(request,"admin/view_product.html", {'data':res})
def adm_view_production(request):
    return render(request,"admin/view_production.html")
def adm_view_raw_material(request):
    res = raw_material.objects.all()
    return render(request,"admin/view_raw_material.html", {'data':res})
def adm_view_request(request):
    res = request_master.objects.all()
    return render(request,"admin/view_request.html", {'data':res})
def adm_view_sales_details_admin(request):
    return render(request,"admin/view_sales_details_admin.html")
def adm_view_sales_report_admin(request):
    return render(request,"admin/view_sales_report_admin.html")
def adm_homepage(request):
    return render(request, "index.html")





