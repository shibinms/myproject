import random
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from itertools import count

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render,redirect

# Create your views here.
from SCM_System.models import branch, login, manager, raw_material, product, notification, request_master, staff, \
    production, stock, user, raw_material_used, cart, sales_master, sales_sub, request_sub, allocate

def homepage(request):

    return render(request,"home.html")


def lognindex(request):

    return render(request,"lognindex.html")
def lognindex_post(request):
    username=request.POST['usname']
    password=request.POST['password']

    # try:
    res=login.objects.filter(username=username,password=password)
    if res.exists():
        res=res[0]
        # print(res)
        request.session['lid']=res.pk

        if res.user_type=='admin':

            # print(res.user_type)
            return adm_homepage(request)
        elif res.user_type=='manager':
            log = request.session['lid']
            aa = manager.objects.get(LOGIN=log)
            print(aa)
            bbid = aa.BRANCH.id
            print(bbid)
            request.session['branch_id'] = bbid
            return manager_home(request)
        elif res.user_type=='Production Staff':

            logn = request.session['lid']
            bbb = staff.objects.get(LOGIN=logn)
            print(bbb)
            bpid = bbb.BRANCH.id
            print(bpid)
            request.session['pbranch_id'] = bpid
            return production_home(request)
        elif res.user_type=='Sales Staff':

            log = request.session['lid']
            bb = staff.objects.get(LOGIN=log)
            print(bb)
            brid = bb.BRANCH.id
            print(brid)
            request.session['sbranch_id'] = brid
            return sales_home(request)
        else:
            return HttpResponse("Invalid!!")
    # except Exception as e:
    #     return e



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
    text="<script>alert('Branch Added'); window.location='/myapp/adm_add_branch';</script>"
    return HttpResponse(text)

def adm_view_branch(request):
    res=branch.objects.all()
    return render(request,"admin/view_branch.html", {'data':res})

def adm_add_manager(request):
    res = branch.objects.all()
    return render(request, "admin/add_manager.html", {'data':res})

def adm_del_manager(request,id):
    qry=manager.objects.get(pk=id)
    lid=qry.LOGIN.id
    login_id=login(id=lid)
    login_id.delete()
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
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("shibinriz106@gmail.com", "9526385712Ms")
    msg = MIMEMultipart()  # create a message.........."
    message = "Messege from LINEN CLUB Admin"
    msg['From'] = "shibinriz106@gmail.com"
    msg['To'] = email
    msg['Subject'] = "Your Password for Login"
    body = "Your Password is:- - " + str(password)
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)
    #branch_id=branch(id=branch_name)
    #branch_id.save()
    bid = branch.objects.get(pk=branch_name)
    qry = manager(manager_name=manager_name, dob=dob, gender=gender, place=place, district=district, state=state, pin=pin, email=email, phone=phone,  profile_img=image, BRANCH=bid, LOGIN=log)
    qry.save()
    text="<script>alert('Manager Assigned'); window.location='/myapp/adm_add_manager';</script>"
    return HttpResponse(text)


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
    text="<script>alert('Product Added'); window.location='/myapp/adm_add_product';</script>"
    return HttpResponse(text)

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
    quantity=request.POST['quantity']
    qry=raw_material(raw_material_name=material_name,gsm=gsm,price=price, quantity=quantity)
    qry.save()
    text="<script>alert('Raw Material Added'); window.location='/myapp/adm_add_raw_material';</script>"
    return HttpResponse(text)
def adm_allocate_raw_material(request,id):
    res = request_sub.objects.get(pk=id)
    sub_id = res.id
    request.session['sub_id'] = sub_id
    # res = request_sub.objects.get(REQUEST_MASTER=id)
    return render(request,"admin/allocate_raw_material.html", {'data':res})

def adm_allocate_raw_material_post(request):
    # material = request.POST['material_name']
    allocated_qty = request.POST['allocated_qty']
    narration = request.POST['narration']

    #iid = request_sub.objects.get(pk=request.session['sub_id'])
    #q = iid.quantity
    #qq = int(q) - int(allocated_qty)
    #print("minus",qq)
    #request.session['quantity_left'] = qq

    qry = allocate(allocated_quantity=allocated_qty, narration=narration, REQUEST_SUB_id=request.session['sub_id'], date=date.today())
    qry.save()





    req_sub = request_sub.objects.get(pk=request.session['sub_id'])

    req_master = req_sub.REQUEST_MASTER.id
    print(req_master)
    # res3 = request_sub.objects.filter(pk=request.session['sub_id']).update(quantity= qq)




    brnch=req_sub.REQUEST_MASTER.STAFF.BRANCH
    raw_mat=req_sub.RAW_MATERIAL
    stock_obj=stock.objects.filter(BRANCH=brnch,RAW_MATERIAL=raw_mat)
    if stock_obj.exists():
        stt=stock_obj[0]
        stt.quantity=int(stt.quantity)+int(allocated_qty)
        stt.save()
    else:
        stt=stock()
        stt.BRANCH=brnch
        stt.RAW_MATERIAL=raw_mat
        stt.quantity = int(allocated_qty)
        stt.save()

    all_sub=[]
    alct_obj=allocate.objects.all()
    for jj in alct_obj:
        all_sub.append(jj.REQUEST_SUB.id)

    request_sub_obj=request_sub.objects.filter(REQUEST_MASTER_id=req_master)
    flg=0
    for kk in request_sub_obj:
        if kk.id not in all_sub:
            flg+=1
    if flg==0:
        res2 = request_master.objects.filter(pk=req_master).update(status="allocated")

    #qry2 = stock(quantity= + int(allocated_qty), BRANCH_id=, RAW_MATERIAL_id=)
    #qry2.save()
    print(raw_mat)

    stock_obj = raw_material.objects.filter(pk=raw_mat.id)
    if stock_obj.exists():
        stt = stock_obj[0]
        stt.quantity = int(stt.quantity) - int(allocated_qty)
        stt.save()

    res = request_master.objects.filter(status="Pending")

    text="<script>alert('Material Allocated'); window.location='/myapp/adm_view_request';</script>"
    return HttpResponse(text)
    # return render(request,"admin/view_request.html", {'data':res})

def adm_view_notification(request):
    res = notification.objects.all()
    return render(request,"admin/view_notification.html", {'data':res})

def adm_notification_branch_name_search(request):
    if request.method=="POST":
        branch_name=request.POST['branchsearch']
        print(branch_name)
        comb_obj=branch.objects.filter(branch_name__contains=branch_name)
        return render(request,"admin/view_notification.html", {'data': comb_obj})

def adm_send_notification(request):
    res = branch.objects.all()
    return render(request,"admin/send_notification.html", {'data':res})

def adm_send_notification_post(request):
    title = request.POST['title']
    message = request.POST['message']
    branch_id = request.POST["branch_name"]
    qry = notification(date=date.today(), title=title, message=message, BRANCH_id=branch_id)
    qry.save()
    text="<script>alert('Notification Send'); window.location='/myapp/adm_send_notification';</script>"
    return HttpResponse(text)

def adm_view_allocate_report(request):
    br=[]
    data=[]
    res = allocate.objects.all()
    for ii in res:
        if ii.REQUEST_SUB.REQUEST_MASTER.STAFF.BRANCH_id not in br:
                data.append({'branch_name':ii.REQUEST_SUB.REQUEST_MASTER.STAFF.BRANCH.branch_name, 'district':ii.REQUEST_SUB.REQUEST_MASTER.STAFF.BRANCH.district, 'phone':ii.REQUEST_SUB.REQUEST_MASTER.STAFF.BRANCH.phone, 'branch_id':ii.REQUEST_SUB.REQUEST_MASTER.STAFF.BRANCH_id})
                br.append(ii.REQUEST_SUB.REQUEST_MASTER.STAFF.BRANCH_id)
    return render(request,"admin/view_allocate_report.html", {'data':data})


def adm_view_manager(request):
    res = manager.objects.all()
    return render(request,"admin/view_manager.html", {'data':res})

def adm_view_material_allocated(request,id):
    res = allocate.objects.filter(REQUEST_SUB__REQUEST_MASTER__STAFF__BRANCH__id=id)
    # res2 = request_sub.objects.get(pk=id)
    return render(request,"admin/view_material_allocated.html", {'data':res})

def adm_view_material_requested(request,id):
    res = request_sub.objects.filter(REQUEST_MASTER=id)
    ar=[]
    for i in res:
        d={}
        req_qty=i.quantity

        tot=0
        d['pk']=i.pk
        d['material']=i.RAW_MATERIAL.raw_material_name
        d['quantity']=req_qty
        alloc_obj=allocate.objects.filter(REQUEST_SUB=i)
        if alloc_obj.exists():
            for j in alloc_obj:
                tot+=int(j.allocated_quantity)
            print(req_qty,"::::",tot)
            if int(req_qty) > tot:
                ar.append(d)
        else:
            ar.append(d)

    return render(request,"admin/view_material_requested.html", {'data':ar})

def adm_view_product(request):
    res = product.objects.all()
    return render(request,"admin/view_product.html", {'data':res})
def adm_view_production(request):


    bd=[]
    data=[]


    res = production.objects.all()
    for ii in res:

        if ii.STAFF.BRANCH not in bd:

                data.append({'branch_name': ii.STAFF.BRANCH.branch_name, 'id': ii.STAFF.BRANCH.id})
                bd.append(ii.STAFF.BRANCH)

    print(bd)
    return render(request,"admin/view_production.html", {'data':data})

def adm_production_details(request,id):



    pd=[]
    data=[]

    res = production.objects.filter(STAFF__BRANCH=id)
    for ii in res:

        if ii.PRODUCT not in pd:

                data.append({'product_name': ii.PRODUCT.product_name,'quantity': ii.stock, 'id': ii.PRODUCT.id})
                pd.append(ii.PRODUCT)

    print(pd)

    return render(request,"admin/production details.html", {'data':data})

def adm_view_raw_material(request):
    res = raw_material.objects.all()

    return render(request,"admin/view_raw_material.html", {'data':res})
def adm_view_request(request):

    res = request_master.objects.filter(status="Forwarded")
    # res = request_master.objects.all()
    return render(request,"admin/view_request.html", {'data':res})

def adm_date_search_view_request(request):
    if request.method=="POST":
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        print(start_date)
        print(end_date)
        res = request_master.objects.filter(date__range=(start_date,end_date), status='Forwarded')
        print(res)


        return render(request,"admin/view_request.html", {'data': res})

def adm_branch_name_search_view_requst(request):
    if request.method=="POST":
        branch_name=request.POST['bnames_search']

        comb_obj=branch.objects.filter(branch_name__contains=branch_name)
        return render(request,"admin/view_request.html", {'data': comb_obj})


def adm_view_sales_report_admin(request):


    bd=[]
    data=[]


    res = sales_master.objects.all()
    for ii in res:
        tot = 0
        branch_id=ii.STAFF.BRANCH_id
        if branch_id not in bd:
            res2=sales_master.objects.filter(STAFF__BRANCH__id=branch_id)
            for jj in res2:
                tot += float(jj.amount)
            data.append({'branch_name': ii.STAFF.BRANCH.branch_name, 'id': ii.STAFF.BRANCH.id, 'amount': tot})
            bd.append(branch_id)


    print(bd)
    #return render(request, "production staff/view_production_report_production_staff.html", {'data': data})

    return render(request,"admin/view_sales_report_admin.html", {'data':data})

def adm_view_sales_details_admin(request,id):
    res = sales_sub.objects.filter(SALES_MASTER__STAFF__BRANCH__id=id)

    pd=[]
    data=[]
    for ii in res:
        qty=0
        pro_id=ii.PRODUCT
        if pro_id not in pd:
            re2=sales_sub.objects.filter(PRODUCT_id=pro_id,SALES_MASTER__STAFF__BRANCH__id=id)
            for jj in re2:
                qty+=int(jj.quantity)
            data.append({'product_name': ii.PRODUCT.product_name, 'id': ii.PRODUCT.id, 'quantity': qty, 'amount': int(qty) * int(ii.PRODUCT.price)})
            pd.append(pro_id)

    return render(request,"admin/view_sales_details_admin.html", {'data': data})

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

    text="<script>alert('Updated Successfully'); window.location='/myapp/adm_view_branch';</script>"
    return HttpResponse(text)

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

    branch_name = request.POST['bname']

    bid = branch.objects.get(pk=branch_name)

    res=manager.objects.filter(pk=request.session['upid2']).update(manager_name=manager_name, dob=dob, gender=gender, place=place, district=district, state=state, pin=pin, phone=phone, BRANCH=bid)

    text="<script>alert('Updated Successfully'); window.location='/myapp/adm_view_manager';</script>"
    return HttpResponse(text)

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

    text="<script>alert('Updated Successfully'); window.location='/myapp/adm_view_product';</script>"
    return HttpResponse(text)

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
    quantity=request.POST['quantity']

    res = raw_material.objects.filter(pk=request.session['upid4']).update(raw_material_name=material_name, gsm=gsm, price=price, quantity=quantity)

    text="<script>alert('Updated Success Fully'); window.location='/myapp/adm_view_raw_material';</script>"
    return HttpResponse(text)

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

def sales_home(request):

    return render(request,"sales_home.html")

def sales_sales_entry(request):
    res = product.objects.all()
    res3 = raw_material.objects.all()
    #request.session['a'] = ""
    request.session['cust_email'] = ""
    request.session['cust_phn'] = ""
    request.session['tot'] = ""
    return render(request,"sales_staff/sales_entry.html", {'data': res, 'data3': res3,'cust_email':"", 'cust_phn':""})


def sales_sales_entry_post(request):
    save=request.POST['button']
    add=request.POST['button']
    submit=request.POST['button']

    if save=="Save":
        cemail = request.POST['cemail']
        cust_phn = request.POST['phone']
        request.session['cust_email'] = cemail
        request.session['cust_phn'] = cust_phn
        res = product.objects.all()
        res3 = raw_material.objects.all()

        password = random.randint(0000, 9999)
        log = login(username=cemail, password=password, user_type='user')
        log.save()

        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("shibinriz106@gmail.com", "9526385712Ms")
        msg = MIMEMultipart()  # create a message.........."
        message = "Messege from LINEN CLUB Admin"
        msg['From'] = "shibinriz106@gmail.com"
        msg['To'] = cemail
        msg['Subject'] = "Your Password for Login"
        body = "Your Password is:- - " + str(password)
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)

        qq = user(user_name="Null", gender="Null", place="Null", post="Null", pin=000000, district="Null", state="Null", email=cemail, phone=cust_phn, profile_img="Null", LOGIN=log)
        qq.save()



        return render(request, "sales_staff/sales_entry.html", {'data': res, 'data3': res3, 'cust_email': request.session['cust_email'], 'cust_phn': request.session['cust_phn']})
    elif add=="Add":
        prod_id = request.POST['pname']
        request.session['prod_name'] = prod_id
        pid = product.objects.get(pk=prod_id)
        price = pid.price
        product_name = pid.product_name
        quantity = request.POST['qty']

        size = request.POST['radio']
        material_id = request.POST['mname']
        request.session['mat_name'] = material_id
        mid = raw_material.objects.get(pk=material_id)
        mat_price = mid.price
        material_name = mid.raw_material_name

        print(size)
        print(material_id)
        print(mat_price)
        print(material_name)



        # request.session['sbranch_id'] = branch_id
        qry = cart(product_name=product_name, quantity=quantity, price=price, product_id=prod_id, size=size, material_price=mat_price, material_name=material_name, material_id=material_id)
        qry.save()
        res = product.objects.all()
        res3 = raw_material.objects.all()
        cart_obj=cart.objects.all()
        ar=[]
        tot=0
        tailoring=0
        t_price=0
        for i in cart_obj:
            tailoring+=int(i.price)*int(i.quantity)
            t_price+=int(i.material_price)*float(i.size)
            tot+=(int(i.price)*int(i.quantity))+(int(i.material_price)*float(i.size))
            request.session['tot'] = tot
            ar.append({'id':i.id,'product_name':i.product_name,'quantity':i.quantity,'price':i.price,'tailoring':int(i.price)*int(i.quantity), 'size': i.size, 'material': i.material_name, 'mprice': i.material_price, 'price': int(i.material_price)*float(i.size),'amount': round(int(i.price)*int(i.quantity))+(int(i.material_price)*float(i.size))})
        return render(request, "sales_staff/sales_entry.html",{'data': res, 'data3': res3, 'cust_email': request.session['cust_email'], 'cust_phn': request.session['cust_phn'], 'data2': ar , 'total':tot, 'tailoring': tailoring, 'tprice': t_price})
    elif submit == 'Submit':
        cart_obj = cart.objects.all()
        user_email = request.session['cust_email']
        user_phone = request.session['cust_phn']
        discount = request.POST['discount']
        total = request.session['tot']

        log = request.session['lid']
        aa = staff.objects.get(LOGIN=log)
        staff_id = aa.pk
        print(staff_id)



        qry = sales_master(date=date.today(), discount=discount, amount=total, status='Paid', user_email=user_email, user_phone=user_phone,STAFF_id=staff_id)
        sss=qry.save()
        sales_master_id = sales_master.objects.latest('id')
        sid = sales_master_id.id

        print(sid)


        for i in cart_obj:
            pid = i.product_id
            qty = i.quantity
            size = i.size
            mid = i.material_id

            qry2 = sales_sub(quantity=qty, size=size, PRODUCT_id=pid, RAW_MATERIAL_id=mid, SALES_MASTER_id=sid)
            qry2.save()
        cartobj = cart.objects.all()
        cartobj.delete()


        return sales_view_sales_report_common(request)


def sales_del_cart(request,id):
    qry=cart.objects.get(pk=id)
    qry.delete()
    res = product.objects.all()
    res3 = raw_material.objects.all()
    cart_obj = cart.objects.all()
    ar = []
    tot = 0
    for i in cart_obj:
        tot += int(i.price) * int(i.quantity)
        request.session['tot'] = tot
        ar.append({'id': i.id, 'product_name': i.product_name, 'quantity': i.quantity, 'price': i.price,
                   'amount': int(i.price) * int(i.quantity)})
    return render(request, "sales_staff/sales_entry.html",{'data': res, 'data3': res3, 'cust_email': request.session['cust_email'], 'cust_phn': request.session['cust_phn'],'data2': ar, 'total': tot})

def sales_view_sales_report_common(request):
    res = sales_master.objects.filter(STAFF__BRANCH=request.session['sbranch_id'])

    return render(request, "sales_staff/view_sales_report_common.html", {'data':res})

def sales_view_sales_details(request,id):
    res2 = sales_sub.objects.filter(SALES_MASTER=id)
    print("hello")
    print(res2)
    res = sales_master.objects.get(pk=id)
    print(res)


    return render(request, "sales_staff/view_sales_details.html", {'data2': res2, 'data': res})

def sales_view_product_new_sales_staff(request):
    res = sales_master.objects.filter(STAFF__BRANCH=request.session['sbranch_id'], status='Out For Deliver')
    return render(request, "sales_staff/view_product_sales_staff.html", {'data2':res})

def sales_phone_number_search(request):
    if request.method=="POST":
        phone_number=request.POST['phonenumber']
        comb_obj=sales_master.objects.filter(user_phone__contains=phone_number, status='Out For Deliver')
        return render(request,"sales_staff/view_product_sales_staff.html", {'data2': comb_obj})

def sales_view_product_new_details_sales_staff(request,id):
    res = sales_sub.objects.filter(SALES_MASTER_id=id)
    return render(request, "sales_staff/view_product_details_sales_staff.html", {'data':res})

def sales_delivered(request,id):

    res = sales_master.objects.filter(pk=id).update(status='Delivered')

    text = "<script>alert('Delivered'); window.location='/myapp/sales_view_product_delivered_sales_staff';</script>"
    return HttpResponse(text)

def sales_view_product_delivered_sales_staff(request):
    res = sales_master.objects.filter(STAFF__BRANCH=request.session['sbranch_id'], status='Delivered')
    return render(request, "sales_staff/view_product_delivered_sales_staff.html", {'data':res})

def sales_view_product_delivered_details_sales_staff(request,id):
    res = sales_sub.objects.filter(SALES_MASTER_id=id)
    return render(request, "sales_staff/view_product_deliverd_details_sales_staff.html", {'data':res})

def sales_view_profile(request):
    aa=login.objects.get(id=request.session['lid'])
    print("aa=",aa)
    res = staff.objects.get(LOGIN=aa)
    print(aa)

    return render(request, "sales_staff/view_profile_sales_staff.html", {'data':res})

def sales_edit_profile(request,id):
    aa = login.objects.get(id=request.session['lid'])
    res = staff.objects.get(LOGIN=aa)
    request.session['upid']=id
    return render(request, "sales_staff/edit_sales_profile.html", {'data':res})

def sales_edit_profile_update(request):
    staff_name=request.POST['sname']
    dob=request.POST['dob']
    gender=request.POST['radio']
    place=request.POST['place']
    post=request.POST['post']
    district=request.POST['district']
    state=request.POST['state']
    pin = request.POST['pin']
    phone=request.POST['phone']

    res=staff.objects.filter(pk=request.session['upid']).update(staff_name=staff_name, dob=dob, gender=gender, place=place, post=post, district=district, state=state, pin=pin, phone=phone)

    return sales_view_profile(request)




def sales_phone_number_search(request):
    if request.method=="POST":
        phonenumber=request.POST['phonenumber']
        comb_obj=sales_master.objects.filter(user_phone__contains=phonenumber, status='Delivered')
        return render(request,"sales_staff/view_product_delivered_sales_staff.html", {'data': comb_obj})


def sales_date_search_sales_report(request):
    if request.method=="POST":
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        print(start_date)
        print(end_date)
        res = sales_master.objects.filter(date__range=(start_date,end_date))
        print(res)


        return render(request,"sales_staff/view_sales_report_common.html", {'data': res})

def adm_del_notification(request,id):
    qry=notification.objects.get(pk=id)
    qry.delete()
    return adm_view_notification(request)

def production_home(request):

    return render(request,"production_home.html")



def production_update_material_usage(request,id):
    res = raw_material.objects.get(pk=id)
    request.session['rid']=id
    return render(request,"production staff/update_material_usage.html", {'data': res})

def production_update_material_usage_post(request):
    qty=request.POST['qty']
    rid = raw_material.objects.get(id=request.session['rid'])
    print(rid)
    #rid=request.session['rid']

    aa=login.objects.get(id=request.session['lid'])
    sid=staff.objects.get(LOGIN=aa)
    bid=sid.BRANCH.id
    # cc=sid.BRANCH.id
    # bid = branch.objects.get(id=cc)
    print("sid",sid)
    print("rid",rid)

    qry = raw_material_used(date=date.today(), quantity_used=qty, STAFF=sid, RAW_MATERIAL=rid)
    qry.save()

    # qry2 = stock.objects.filter(BRANCH=bid, RAW_MATERIAL=rid).update(quantity=

    stock_obj = stock.objects.filter(BRANCH_id=bid, RAW_MATERIAL_id=rid)
    if stock_obj.exists():
        stt = stock_obj[0]
        stt.quantity = int(stt.quantity) - float(qty)
        stt.save()

    #srid=stock.objects.get(RAW_MATERIAL=rid)
    #aqty=srid.quantity

    #sqty=stock.objects.get(quantity=aqty)
    #print("hello")

    #fqty = sqty - qty
    #print("vale =",fqty)

    # branch_id = raw_material_used.objects.get(RAW_MATERIAL_id=bid)
    # bbid = branch_id.RAW_MATERIAL
     #qry2 = stock(rid.update(int(rid.quantity) - int(rid.qty_left)))

    return production_view_material_usage(request)
    #return render(request, "production staff/view_material_usage.html")

def production_view_rawmaterial(request):

    rw=[]
    data=[]
    res = stock.objects.filter(BRANCH_id=request.session['pbranch_id'])
    for ii in res:
        if ii.RAW_MATERIAL_id not in rw:
            data.append({'raw_material_name': ii.RAW_MATERIAL.raw_material_name, 'id': ii.RAW_MATERIAL_id, 'stock': ii.quantity, 'gsm': ii.RAW_MATERIAL.gsm})
            rw.append(ii.RAW_MATERIAL_id)

    print(rw)


    return render(request,"production staff/view_raw_material_production_staff.html", {'data': data})


def production_view_material_usage(request):
    #res = raw_material_used.objects.all()

    rw=[]
    data=[]
    res = raw_material_used.objects.filter(STAFF__BRANCH=request.session['pbranch_id'])
    for ii in res:
        if ii.RAW_MATERIAL_id not in rw:
            data.append({'raw_material_name': ii.RAW_MATERIAL.raw_material_name, 'id': ii.RAW_MATERIAL_id})
            rw.append(ii.RAW_MATERIAL_id)

    print(rw)


    return render(request, "production staff/view_material_usage.html", {'data': data})

def production_usage_details(request,id):

    res = raw_material_used.objects.filter(STAFF__BRANCH=request.session['pbranch_id'],RAW_MATERIAL=id)
    return render(request, "production staff/usage_details.html", {'data': res})

def production_update_production(request):
    res = sales_master.objects.filter(STAFF__BRANCH=request.session['pbranch_id'],status='Paid')
    return render(request, "production staff/update_production.html", {'data': res})

def production_out_for_delivery(request,id):

    res = sales_master.objects.filter(pk=id).update(status='Out For Deliver')

    res2 = sales_sub.objects.filter(SALES_MASTER_id=id)
    for ii in res2:
        rid =ii.RAW_MATERIAL
        qty =ii.size
        pqty =ii.quantity
        pid = ii.PRODUCT

    #rid=request.session['rid']

        aa=login.objects.get(id=request.session['lid'])
        sid=staff.objects.get(LOGIN=aa)
        bid=sid.BRANCH.id
    # cc=sid.BRANCH.id
    # bid = branch.objects.get(id=cc)
        print("sid",sid)
        print("rid",rid)

        qry = raw_material_used(date=date.today(), quantity_used=qty, STAFF=sid, RAW_MATERIAL=rid)
        qry.save()

        stock_obj = stock.objects.filter(BRANCH_id=bid, RAW_MATERIAL_id=rid)
        if stock_obj.exists():
            print("stockkkk")
            stt = stock_obj[0]
            stt.quantity = int(stt.quantity) - float(qty)
            stt.save()
        pid = product.objects.get(pk=pid.id)
        aa = login.objects.get(id=request.session['lid'])
        sid = staff.objects.get(LOGIN=aa)
        qry1 = production(date=date.today(), stock=pqty, PRODUCT=pid, STAFF_id=sid.id)
        qry1.save()

    # return render(request, "production staff/update_production.html")
    text = "<script>alert('Production Updated'); window.location='/myapp/production_update_production';</script>"
    return HttpResponse(text)

def production_update_production_post(request):
    product_name=request.POST['pname']
    qty=request.POST['qty']
    pid = product.objects.get(pk=product_name)
    aa=login.objects.get(id=request.session['lid'])
    sid=staff.objects.get(LOGIN=aa)
    qry1 = production(date=date.today(), stock=qty, PRODUCT=pid, STAFF_id=sid.id)
    qry1.save()
    #return production_view_production_report(request)
    text = "<script>alert('Production Updated'); window.location='/myapp/production_update_production';</script>"
    return HttpResponse(text)
def production_update_production_details(request,id):

    res = sales_sub.objects.filter(SALES_MASTER__STAFF__BRANCH=request.session['pbranch_id'],SALES_MASTER_id=id)

    return render(request, "production staff/update_production_details.html", {'data': res})


def production_view_production_report(request):

    pd=[]
    data=[]
    res = production.objects.filter(STAFF__BRANCH=request.session['pbranch_id'])
    for ii in res:
        if ii.PRODUCT not in pd:
                data.append({'product_name': ii.PRODUCT.product_name, 'id': ii.PRODUCT_id})
                pd.append(ii.PRODUCT)

    print(pd)
    return render(request, "production staff/view_production_report_production_staff.html", {'data': data})

def production_production_details(request,id):

    res = production.objects.filter(PRODUCT_id=id,STAFF__BRANCH=request.session['pbranch_id'])

    return render(request, "production staff/production_details.html", {'data': res})

def production_date_search(request):
    if request.method=="POST":
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        print(start_date)
        print(end_date)
        res = production.objects.filter(date__range=(start_date,end_date))
        print(res)


        return render(request,"production staff/production_details.html", {'data': res})

def production_request_material_production(request):
    res = raw_material.objects.all()
    request.session["flag"] = 0

    return render(request, "production staff/request_material_production.html", {'data': res})


def production_request_material_post(request):
    material = request.POST['raw_material']
    quantity = request.POST['quantity']
    btn=request.POST["button"]

    aa=login.objects.get(id=request.session['lid'])
    sid=staff.objects.get(LOGIN_id=aa.id)
    if btn=="Add":
        # request.session["flag"] = 0

        print("Add")

        if request.session["flag"]==0:
            print("Add2")


            qry = request_master(date=date.today(), status="Pending", STAFF_id=sid.id)
            qry.save()
            # request_master_id = request_master.objects.latest('id')
            mid = qry.id
            print(mid)

            request.session["masterid"]=mid
            print("hi")
            qry2 = request_sub(quantity=quantity, RAW_MATERIAL_id=material, REQUEST_MASTER_id=mid)
            qry2.save()
            print("llllll")

            print("hiiii")

            res = raw_material.objects.all()

            request.session["flag"] = 1
            qry4=request_sub.objects.filter(REQUEST_MASTER_id=mid)

            print(qry4)

            return render(request, "production staff/request_material_production.html", {'sub':qry4, 'data': res})

        else:
            qry2 = request_sub(quantity=quantity, RAW_MATERIAL_id=material, REQUEST_MASTER_id=request.session["masterid"])
            qry2.save()
            res = raw_material.objects.all()
            qry4 = request_sub.objects.filter(REQUEST_MASTER_id=request.session["masterid"])
            print("else")
            # return production_request_material_production(request)
            return render(request, "production staff/request_material_production.html", {'sub': qry4, 'data': res})
    elif btn=="Submit":
        request.session["flag"]=1

        return production_request_material_production(request)

def production_del_cart(request,id):
    qry=request_sub.objects.get(pk=id)
    qry.delete()
    res = raw_material.objects.all()
    qry4 = request_sub.objects.filter(REQUEST_MASTER_id=request.session["masterid"])

    return render(request, "production staff/request_material_production.html", {'sub': qry4, 'data': res})


def production_product_name_search(request):
    if request.method=="POST":
        product_name=request.POST['productsearch']
        print(product_name)
        comb_obj=production.objects.filter(product_name__contains=product_name)
        return render(request,"production staff/view_production_report_production_staff.html", {'data': comb_obj})


def manager_home(request):

    return render(request,"manager_home.html")

def manager_add_staff(request):

    return render(request,"manager/add_staff.html")

def manager_view_staff(request):
    res = staff.objects.filter(BRANCH=request.session['branch_id'])
    return render(request,"manager/view_staff.html", {'data': res})

def manager_add_staff_post(request):

    staff_name=request.POST['sname']
    dob=request.POST['dob']
    gender=request.POST['radio']
    position=request.POST['position']
    place=request.POST['place']
    post=request.POST['post']
    district=request.POST['district']
    state=request.POST['state']
    pin = request.POST['pin']
    email=request.POST['email']
    phone=request.POST['phone']
    myfile=request.FILES['image']
    fs = FileSystemStorage()
    filename=fs.save(myfile.name, myfile)
    image = fs.url(filename)
    password=random.randint(0000,9999)

    aa=login.objects.get(id=request.session['lid'])
    #aaa=aa.id
    print(aa)

    bb=manager.objects.get(LOGIN=aa)
    #bbb=bb.id
    print(bb)
    bids=bb.BRANCH.id
    branch_id=branch(id=bids)
    branch_id.save()
    log=login(username=email, password=password, user_type=position)
    log.save()
    #bid = branch.objects.get(pk=staff_name)
    qry = staff(staff_name=staff_name, dob=dob, gender=gender, position=position, place=place, post=post, district=district, state=state, pin=pin, email=email, phone=phone,  profile_img=image, BRANCH=branch_id, LOGIN=log)
    qry.save()
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("shibinriz106@gmail.com", "9526385712Ms")
    msg = MIMEMultipart()  # create a message.........."
    message = "Message From LINEN CLUB Admin Team"
    msg['From'] = "shibinriz106@gmail.com"
    msg['To'] = email
    msg['Subject'] = "Message From LINEN CLUB Admin Team"
    body = "Your Password is:- - " + str(password)
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)

    # return manager_view_staff(request)
    text = "<script>alert('Staff Added'); window.location='/myapp/manager_add_staff';</script>"
    return HttpResponse(text)

def manager_edit_staff(request,id):
    res = staff.objects.get(pk=id)
    print(res)
    request.session['upid']=id
    return render(request, "manager/edit_staff.html", {'data':res})

def manager_update_staff(request):
    staff_name=request.POST['sname']
    dob=request.POST['dob']
    gender=request.POST['radio']
    position=request.POST['position']
    place=request.POST['place']
    post=request.POST['post']
    district=request.POST['district']
    state=request.POST['state']
    pin = request.POST['pin']
    phone=request.POST['phone']


    #bid = branch.objects.get(pk=branch_name)

    res=staff.objects.filter(pk=request.session['upid']).update(staff_name=staff_name, dob=dob, gender=gender, position=position, place=place, post=post, district=district, state=state, pin=pin, phone=phone)

    # return manager_view_staff(request)
    text = "<script>alert('Updated Successfully'); window.location='/myapp/manager_view_staff';</script>"
    return HttpResponse(text)

def manager_del_staff(request,id):
    qry=staff.objects.get(pk=id)
    lid=qry.LOGIN.id
    login_id=login(id=lid)
    login_id.delete()
    qry.delete()
    return manager_view_staff(request)

def manager_view_profile(request):
    aa=login.objects.get(id=request.session['lid'])
    print("aa=",aa)
    res = manager.objects.get(LOGIN=aa)
    print(aa)

    return render(request, "manager/view_profile-manager.html", {'data': res})

def manager_view_products(request):
    res = sales_master.objects.filter(STAFF__BRANCH=request.session['branch_id'], status='Delivered')

    return render(request, "manager/view_product_manager.html", {'data': res})

def manager_view_products_delivered_details(request,id):
    res = sales_sub.objects.filter(SALES_MASTER_id=id)

    return render(request, "manager/view_product_delivered_details_manager.html", {'data': res})

def manager_phone_number_search(request):
    if request.method=="POST":
        phonenumber=request.POST['phonenumber']
        comb_obj=sales_master.objects.filter(user_phone__contains=phonenumber, status='Delivered')
        return render(request,"manager/view_product_manager.html", {'data': comb_obj})

def manager_staff_name_search(request):
    if request.method=="POST":
        staff_name=request.POST['staff_search']
        print(staff_name)
        comb_obj=staff.objects.filter(staff_name__contains=staff_name)
        return render(request,"manager/view_staff.html", {'data': comb_obj})

def manager_product_name_search(request):
    if request.method=="POST":
        product_name=request.POST['productname']
        print(product_name)
        comb_obj=product.objects.filter(product_name__contains=product_name)
        return render(request,"manager/view_product_manager.html", {'data': comb_obj})

def manager_view_request(request):

    res = request_master.objects.filter(STAFF__BRANCH=request.session['branch_id'],status="Pending")

    return render(request, "manager/view_request_from_production.html", {'data': res})

def manager_view_request_details(request,id):
    res2 = request_sub.objects.filter(REQUEST_MASTER=id)
    # res = sales_master.objects.get(pk=id)
    return render(request, "manager/request_details.html", {'data': res2})

def manager_forwarded(request,id):

    res = request_master.objects.filter(pk=id).update(status='Forwarded')

    return render(request, "manager/view_request_from_production.html")

def manager_del_staff(request,id):
    qry=staff.objects.get(pk=id)
    lid=qry.LOGIN.id
    login_id=login(id=lid)
    login_id.delete()
    qry.delete()
    return manager_view_staff(request)

def manager_del_rqst(request,id):
    qry=request_master.objects.get(pk=id)
    qry2=request_sub.objects.filter(REQUEST_MASTER_id=id)
    qry.delete()
    qry2.delete()
    return manager_view_request(request)

def manager_edit_profile(request,id):
    res = manager.objects.get(pk=id)
    request.session['upid2']=id
    return render(request,"manager/edit_manager_profile.html",{'data':res})
def manager_edit_profile_post(request):
    manager_name=request.POST['mname']
    dob=request.POST['date']
    gender=request.POST['radio']
    place=request.POST['place']
    district=request.POST['district']
    state = request.POST['state']
    pin=request.POST['pin']
    phone = request.POST['phone']


    res=manager.objects.filter(pk=request.session['upid2']).update(manager_name=manager_name, dob=dob, gender=gender, place=place, district=district, state=state, pin=pin, phone=phone)

    #return redirect("myapp:manager_view_profile")
    # return manager_view_profile(request)
    text = "<script>alert('Updated Successfully'); window.location='/myapp/manager_view_profile';</script>"
    return HttpResponse(text)

def manager_view_materials_allocated(request):

    # res = allocate.objects.all()
    rw=[]
    data=[]
    res = allocate.objects.filter(REQUEST_SUB__REQUEST_MASTER__STAFF__BRANCH=request.session['branch_id'])
    for ii in res:
        rid = ii.REQUEST_SUB.RAW_MATERIAL.id
        if rid not in rw:
            data.append({'raw_material_name': ii.REQUEST_SUB.RAW_MATERIAL.raw_material_name,  'allocated_quantity': ii.allocated_quantity, 'date': ii.date, 'id': rid})
            rw.append(rid)

    print(rw)

    return render(request, "manager/view_material_allocated.html", {'data': data})

def manager_allocate_details(request,id):
    res1=request_sub.objects.filter(RAW_MATERIAL=id)
    rw = []
    for ii in res1:
        mureq_sub=ii.id
        res = allocate.objects.filter(REQUEST_SUB=mureq_sub)

    print(res)
    return render(request, "manager/allocate_details.html", {'data': res})

def manager_view_stock(request):

    res = stock.objects.filter(BRANCH=request.session['branch_id'])

    return render(request, "manager/view_stock.html", {'data': res})

def manager_view_notification(request):

    res = notification.objects.filter(BRANCH_id=request.session['branch_id'])

    return render(request, "manager/view_notification_branch.html", {'data': res})

def manager_date_search_view_request(request):
    if request.method=="POST":
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        print(start_date)
        print(end_date)
        res = request_master.objects.filter(date__range=(start_date,end_date), status='Pending')
        print(res)


        return render(request,"manager/view_request_from_production.html", {'data': res})





