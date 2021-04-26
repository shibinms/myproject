from django.db import models

# Create your models here.
class login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    user_type = models.CharField(max_length=50)

class branch(models.Model):
    branch_name = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pin = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)

class manager(models.Model):
    manager_name = models.CharField(max_length=50)
    dob = models.DateField(max_length=50)
    gender = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    profile_img = models.CharField(max_length=300)
    BRANCH = models.ForeignKey(branch, on_delete=models.CASCADE)
    LOGIN = models.ForeignKey(login, on_delete=models.CASCADE)


class product(models.Model):
    product_name = models.CharField(max_length=50)
    product_type = models.CharField(max_length=50)
    image = models.CharField(max_length=300)
    description = models.CharField(max_length=50)
    price = models.CharField(max_length=50)



class raw_material(models.Model):
    raw_material_name = (models.CharField(max_length=50))
    gsm = models.CharField(max_length=50)
    price = models.CharField(max_length=50)

class stock(models.Model):
    quantity = models.CharField(max_length=50)
    BRANCH = models.ForeignKey(branch, on_delete=models.CASCADE)
    RAW_MATERIAL = models.ForeignKey(raw_material, on_delete=models.CASCADE)

class request_master(models.Model):
    date = models.DateField(max_length=50)
    status = models.CharField(max_length=50)
    MANAGER = models.ForeignKey(manager, on_delete=models.CASCADE)


class request_sub(models.Model):
    quantity = models.CharField(max_length=50)
    RAW_MATERIAL = models.ForeignKey(raw_material, on_delete=models.CASCADE)
    REQUEST_MASTER = models.ForeignKey(request_master, on_delete=models.CASCADE)

class allocate(models.Model):
    allocated_quantity=models.CharField(max_length=50)
    narration=models.CharField(max_length=50)
    REQUEST_MASTER = models.ForeignKey(request_master, on_delete=models.CASCADE)

class notification(models.Model):
    date = models.DateField(max_length=50)
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=50)
    BRANCH = models.ForeignKey(branch, on_delete=models.CASCADE)


class user(models.Model):
    user_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    post = models.CharField(max_length=50)
    pin = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    profile_img = models.CharField(max_length=300)
    LOGIN = models.ForeignKey(login, on_delete=models.CASCADE)

class feedback(models.Model):
    feedback = models.CharField(max_length=50)
    date = models.DateField(max_length=50)
    PRODUCT = models.ForeignKey(product, on_delete=models.CASCADE)
    USER = models.ForeignKey(user, on_delete=models.CASCADE)

class staff(models.Model):
    staff_name = models.CharField(max_length=50)
    dob = models.DateField(max_length=50)
    gender = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    post = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    profile_img = models.CharField(max_length=300)
    BRANCH = models.ForeignKey(branch, on_delete=models.CASCADE)
    LOGIN = models.ForeignKey(login, on_delete=models.CASCADE)

class request_product(models.Model):
    date =(models.DateField(max_length=50))
    quantity = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    USER = models.ForeignKey(user, on_delete=models.CASCADE)
    PRODUCT = models.ForeignKey(product, on_delete=models.CASCADE)


class raw_material_used(models.Model):
    date=(models.DateField(max_length=50))
    quantity_used=models.CharField(max_length=50)
    STAFF = models.ForeignKey(staff, on_delete=models.CASCADE)
    RAW_MATERIAL = models.ForeignKey(raw_material, on_delete=models.CASCADE)


class sales_master(models.Model):
    date = (models.DateField(max_length=50))
    discount = models.CharField(max_length=50)
    amount = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)
    user_phone = models.CharField(max_length=50)

class sales_sub(models.Model):
    quantity = models.CharField(max_length=50)
    PRODUCT = models.ForeignKey(product, on_delete=models.CASCADE)
    SALES_MASTER = models.ForeignKey(sales_master, on_delete=models.CASCADE)

class production(models.Model):
    date = (models.DateField(max_length=50))
    stock = models.CharField(max_length=50)
    PRODUCT = models.ForeignKey(product, on_delete=models.CASCADE)
    #STAFF = models.ForeignKey(staff, on_delete=models.CASCADE)

class cart(models.Model):
    product_name = (models.CharField(max_length=50))
    quantity = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    product_id = models.CharField(max_length=50)