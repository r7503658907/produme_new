from django.db import models
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

status_ticket = (
    ("InProgress", "InProgress"),
    ("Closed", "Closed")
)

addressType = (
    ("HOME", "HOME"),
    ("OFFICE", "OFFICE"),
    ("OTHER", "OTHER")
)

kitchen_type = (
    ("L", "L"),
    ("U", "U"),
    ("Parallel", "Parallel"),
    ("G", "G"),
    ("O", "O")
)


class prodymeUser(models.Model):
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, primary_key=True)
    # mobile = models.CharField(max_length=100, default='', null=True)
    password = models.CharField(max_length=100)
    is_verified_email = models.BooleanField(default=False)
    is_verified_mobile = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class profile(models.Model):
    username = models.ForeignKey(prodymeUser, on_delete=models.CASCADE)
    profile_id = models.CharField(primary_key=True, max_length=100)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    business_name = models.CharField(max_length=100, default='')
    gst = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='', null=True)
    mobile = models.CharField(max_length=100, default='', null=True)
    password = models.CharField(max_length=100, default='', null=True)
    zipcode = models.CharField(max_length=100, default='', null=True)

    def __str__(self):
        return self.profile_id


class Wishlist(models.Model):
    username = models.ForeignKey(prodymeUser, on_delete=models.CASCADE)
    product_list = models.TextField()
    wishlist_ID = models.CharField(max_length=100, primary_key=True)
    status = models.CharField(max_length=1)

    def __str__(self):
        return self.wishlist_ID


class profile_address(models.Model):
    username = models.ForeignKey(prodymeUser, on_delete=models.CASCADE)
    address_id = models.CharField(primary_key=True, max_length=100)
    address_type = models.CharField(max_length=10, choices=addressType, default='HOME')
    address_nickname = models.CharField(max_length=100, null=True, default='')
    address = models.CharField(max_length=100, default='', null=True)

    def __str__(self):
        return self.address_id


class CommunicationPreference(models.Model):
    username = models.ForeignKey(prodymeUser, on_delete=models.CASCADE)
    communication_preference = models.CharField(default="False", max_length=100)


class GetInTouchModel(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    existing_order_number = models.CharField(max_length=100, null=True, blank=True, default='')
    description = models.CharField(max_length=10000)
    upload_attachments = models.CharField(max_length=100, null=True, blank=True, default='')
    product_type = models.CharField(max_length=100, null=True, blank=True, default='')
    brand = models.CharField(max_length=100, null=True, blank=True, default='')
    status_ticket = models.CharField(max_length=100, choices=status_ticket)

    def __str__(self):
        return self.email


class SmartBuilder(models.Model):
    type_of_kitchen = models.CharField(choices=kitchen_type, max_length=100, primary_key=True)
    nomenclature = models.CharField(max_length=1)
    no_of_len = models.CharField(max_length=1)
    no_of_corners = models.CharField(max_length=1)
    corner_placed_on_side = models.CharField(max_length=100)

    def __str__(self):
        return self.type_of_kitchen


class SmartBuilderDesign(models.Model):
    user = models.ForeignKey(prodymeUser, on_delete=models.CASCADE)
    design_name = models.CharField(max_length=100, primary_key=True)
    length_name = models.CharField(max_length=100, default='', null=True, blank=True)
    balance_after_sink = models.CharField(max_length=100, default='', null=True, blank=True)
    corner_on_which_side = models.CharField(max_length=100, default='', null=True, blank=True)
    balance_after_corner = models.CharField(max_length=100, default='', null=True, blank=True)
    no_of_columns = models.CharField(max_length=100, default='', null=True, blank=True)

    def __str__(self):
        return self.design_name


class PartitionBasketDetails(models.Model):
    partition_name = models.CharField(max_length=100, primary_key=True)
    clear_height = models.CharField(max_length=100)
    height1 = models.CharField(max_length=100, default='', null=True, blank=True)
    height2 = models.CharField(max_length=100, default='', null=True, blank=True)
    height3 = models.CharField(max_length=100, default='', null=True, blank=True)
    height4 = models.CharField(max_length=100, default='', null=True, blank=True)
    height5 = models.CharField(max_length=100, default='', null=True, blank=True)
    height6 = models.CharField(max_length=100, default='', null=True, blank=True)
    height7 = models.CharField(max_length=100, default='', null=True, blank=True)
    height8 = models.CharField(max_length=100, default='', null=True, blank=True)
    height9 = models.CharField(max_length=100, default='', null=True, blank=True)
    height10 = models.CharField(max_length=100, default='', null=True, blank=True)
    height11 = models.CharField(max_length=100, default='', null=True, blank=True)
    height12 = models.CharField(max_length=100, default='', null=True, blank=True)

    def __str__(self):
        return self.partition_name


class smartBuilderPartitionCalculator(models.Model):
    partitionaliascalculator = models.CharField(max_length=100, primary_key=True)
    length_data_condition_check1 = models.CharField(max_length=100, null=True, default='')
    length_data_condition_check2 = models.CharField(max_length=100, null=True, default='')
    length_data_condition_check3 = models.CharField(max_length=100, null=True, default='')
    length_data_condition_check4 = models.CharField(max_length=100, null=True, default='')
    partition_value1 = models.CharField(max_length=100)
    partition_value2 = models.CharField(max_length=100)

    def __str__(self):
        return self.partitionaliascalculator


class SavedCart(models.Model):
    username = models.ForeignKey(prodymeUser, on_delete=models.CASCADE)
    product_list = models.TextField()
    SavedCart_ID = models.CharField(max_length=100, primary_key=True)
    status = models.CharField(max_length=1)

    def __str__(self):
        return self.SavedCart_ID


class Loyalty(models.Model):
    username = models.ForeignKey(prodymeUser, on_delete=models.CASCADE)
    order_amount = models.IntegerField()
    loyaltyPoints = models.FloatField()
    loyalty_ID = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.loyalty_ID


class professional(models.Model):
    professionalUsername = models.CharField(max_length=100, primary_key=True)
    email = models.CharField(max_length=100, default='', null=True)
    mobile = models.CharField(max_length=100, default='', null=True)
    password = models.CharField(max_length=100)
    c_password = models.CharField(max_length=100)
    professional_type = models.CharField(max_length=100)
    expert_areas = models.TextField(null=True, blank=True)
    assign_work_status = models.TextField(null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)
    is_verified_mobile = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.professionalUsername


class bookAService(models.Model):
    username = models.ForeignKey(prodymeUser, on_delete=models.CASCADE)
    serviceid = models.CharField(max_length=100, primary_key=True)
    requestType = models.CharField(max_length=100)
    requestDescription = models.CharField(max_length=100)
    status = models.CharField(max_length=1)
    professionalUsername = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.serviceid


class notification(models.Model):
    notification_id = models.CharField(max_length=100, primary_key=True)
    notificationfrom = models.CharField(max_length=100)
    notificationto = models.CharField(max_length=100, default='group')

    def __str__(self):
        return self.notification_id


class workChart(models.Model):
    serviceid = models.ForeignKey(bookAService, on_delete=models.CASCADE)
    professionalUsername = models.ForeignKey(professional, on_delete=models.CASCADE)
    workid = models.CharField(max_length=100, primary_key=True)
    datetime = models.DateTimeField(default=datetime.datetime.now())
    status = models.CharField(default="In Progress", max_length=100)

    def __str__(self):
        return self.workid


class Category(models.Model):
    category_name = models.CharField(max_length=100, primary_key=True)


class subCategory(models.Model):
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    subCategory_name = models.CharField(max_length=100, primary_key=True)


class subSubCategory(models.Model):
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    subCategory_name = models.ForeignKey(subCategory, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=100, primary_key=True)


class Product(models.Model):
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    subCategory_name = models.ForeignKey(subCategory, on_delete=models.CASCADE)
    item_type = models.ForeignKey(subSubCategory, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=100, primary_key=True)
    productName = models.CharField(max_length=100)
    brandName = models.CharField(max_length=100)
    price = models.IntegerField()

class productDetail(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    productFeature = models.TextField()


class boqAudit(models.Model):
    username = models.ForeignKey(prodymeUser, on_delete=models.CASCADE)
    filename = models.CharField(max_length=200)
    datetime = models.DateTimeField()

class productRateing(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    productRating= models.FloatField()


class productSale(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    productSaleCount= models.IntegerField()








