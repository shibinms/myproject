import random
from datetime import date

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render,redirect

# Create your views here.
from SCM_System.models import branch, login, manager, raw_material, product, notification, request_master


def lognindex(request):
    return render(request,"lognindex.html")
def lognindex_post(request):
    username=request.POST['usname']
    password=request.POST['password']

    # try:
    res=login.objects.filter(username=username,password=password)
    if res.exists():
        res=res[0]
        print(res)
        request.session['lid']=res.pk
        if res.user_type=='admin':
            print(res.user_type)
            return adm_homepage(request)
        elif res.user_type=='manager':
            return manager_homepage(request)
        elif res.user_type=='production_staff':
            return staff_homepage(request)
        elif res.user_type=='sales_staff':
            return sale_homepage()
        else:
            return HttpResponse("Invalid!!")
    # except Exception as e:
    #     return e

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

def adm_del_manager(request,id):
    qry=manager.objects.get(pk=id)
    qry.delete()
    return redirect("myapp:adm_view_manager")

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
    #branch_id=branch(id=branch_name)
    #branch_id.save()
    bid = branch.objects.get(pk=branch_name)
    qry = manager(manager_name=manager_name, dob=dob, gender=gender, place=place, district=district, state=state, pin=pin, email=email, phone=phone,  profile_img=image, BRANCH=bid, LOGIN=log)
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

def adm_del_product(request,id):
    qry=product.objects.get(pk=id)
    qry.delete()
    return redirect("myapp:adm_view_product")

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
def adm_del_branch(request,id):
    qry=branch.objects.get(pk=id)
    qry.delete()
    return redirect("myapp:adm_view_branch")

def adm_edit_branch(request,id):
    res = branch.objects.get(pk=id)
    request.session['upid1']=id
    return render(request,"admin/edit_branch.html", {'data':res})
def adm_update_branch(request):
    branch_name=request.POST['branchname']
    place=request.POST['bplace']
    district=request.POST['bdistrict']
    state = request.POST['bstate']
    country=request.POST['bcountry']
    pin=request.POST['bpin']
    phone = request.POST['bphone']
    res=branch.objects.filter(pk=request.session['upid1']).update(branch_name=branch_name, place=place, district=district, state=state, country=country, pin=pin, phone=phone)

    return redirect("myapp:adm_view_branch")

def adm_branch_name_search(request):
    if request.method=="POST":
        branch_name=request.POST['bnamesearch']
        print(branch_name)
        comb_obj=branch.objects.filter(branch_name__contains=branch_name)
        return render(request,"admin/view_branch.html", {'data': comb_obj})

def adm_edit_manager(request,id):
    res = manager.objects.get(pk=id)
    print(res)
    res2=branch.objects.all()
    request.session['upid2']=id
    return render(request,"admin/edit_manager.html",{'data':res,'data2':res2})
def adm_update_manager(request):
    manager_name=request.POST['mname']
    dob=request.POST['date']
    gender=request.POST['radio']
    place=request.POST['place']
    district=request.POST['district']
    state = request.POST['state']
    pin=request.POST['pin']
    phone = request.POST['phone']
    myfile = request.FILES['image']
    fs = FileSystemStorage()
    filename=fs.save(myfile.name, myfile)
    image = fs.url(filename)
    branch_name = request.POST['bname']

    bid = branch.objects.get(pk=branch_name)

    res=manager.objects.filter(pk=request.session['upid2']).update(manager_name=manager_name, dob=dob, gender=gender, place=place, district=district, state=state, pin=pin, phone=phone, profile_img=image, BRANCH=bid)

    return redirect("myapp:adm_view_manager")

def adm_manager_name_search(request):
    if request.method=="POST":
        manager_name=request.POST['mnamesearch']
        print(manager_name)
        comb_obj=manager.objects.filter(manager_name__contains=manager_name)
        return render(request,"admin/view_manager.html", {'data': comb_obj})


def adm_edit_product(request,id):
    res = product.objects.get(pk=id)
    request.session['upid3']=id
    return render(request,"admin/edit_product.html", {'data':res})

def adm_update_product(request):
    product_name=request.POST['productname']
    type=request.POST['type']
    price=request.POST['price']
    description = request.POST['description']
    myfile=request.FILES['image']
    fs = FileSystemStorage()
    filename=fs.save(myfile.name, myfile)
    image = fs.url(filename)
    res = product.objects.filter(pk=request.session['upid3']).update(product_name=product_name, product_type=type, image=image, description=description, price=price)

    return redirect("myapp:adm_view_product")

def adm_product_name_search(request):
    if request.method=="POST":
        product_name=request.POST['productsearch']
        print(product_name)
        comb_obj=product.objects.filter(product_name__contains=product_name)
        return render(request,"admin/view_product.html", {'data': comb_obj})


def adm_edit_raw_material(request,id):
    res = raw_material.objects.get(pk=id)
    request.session['upid4']=id
    return render(request,"admin/edit_raw_material.html", {'data':res})

def adm_update_raw_material(request):
    material_name=request.POST['materialname']
    gsm=request.POST['gsm']
    price=request.POST['price']

    res = raw_material.objects.filter(pk=request.session['upid4']).update(raw_material_name=material_name, gsm=gsm, price=price)

    return redirect("myapp:adm_view_raw_material")

def adm_raw_material_name_search(request):
    if request.method=="POST":
        raw_material_name=request.POST['rawmaterialname']
        print(raw_material_name)
        comb_obj=raw_material.objects.filter(raw_material_name__contains=raw_material_name)
        return render(request,"admin/view_raw_material.html", {'data': comb_obj})

def adm_del_raw_material(request,id):
    qry=raw_material.objects.get(pk=id)
    qry.delete()
    return redirect("myapp:adm_view_raw_material")


