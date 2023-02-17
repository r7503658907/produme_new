from rest_framework import serializers

class signupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    is_verified_email = serializers.BooleanField(default=False)
    is_verified_mobile = serializers.BooleanField(default=False)

class locationdetectorserializer(serializers.Serializer):
    Latitude = serializers.CharField(max_length=100)
    Longitude = serializers.CharField(max_length=100)

class smartBuilderSerializer(serializers.Serializer):
    type_of_kitchen = serializers.CharField(max_length=100)
    length1 = serializers.CharField(max_length=100,required=False,allow_null=True,allow_blank=True)
    length2 = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    length3 = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    length4 = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    length5 = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    length6 = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    corner_side = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    sink_side = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    clear_height = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    design_name = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    partitionaliascalculator = serializers.CharField(max_length=100,required=False, allow_null=True, allow_blank=True)

class partitionModificationSerializer(serializers.Serializer):
    length1 = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    length2 = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    length3 = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    length4 = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    length5 = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    length6 = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    clear_height = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    no_of_columns_per_length = serializers.IntegerField()


class updateProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    business_name = serializers.CharField(max_length=100, required=False)
    gst = serializers.CharField(max_length=100, required=False)
    email = serializers.CharField(max_length=100, required=False)
    mobile = serializers.CharField(max_length=100, required=False,allow_null=True,allow_blank=True)
    password = serializers.CharField(max_length=100, required=False,allow_null=True,allow_blank=True)


class forgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)

class emailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)

class emailVerifyValidateSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    otp = serializers.CharField()

class verifyResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)
    otp = serializers.CharField()

class cabinetstructure1Serializer(serializers.Serializer):
    total_length_of_slab = serializers.CharField(max_length=10)
    slab_depth = serializers.CharField(max_length=10)
    no_of_corner = serializers.CharField(max_length=10)
    no_of_partition = serializers.CharField(max_length=10)
    clear_height = serializers.CharField(max_length=10)
    area_chosen = serializers.CharField(max_length=10)


class userLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    mobile = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    password = serializers.CharField(max_length=100)


class getInTouchSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)
    mobile = serializers.CharField(max_length=100)
    zipcode = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    subject = serializers.CharField(max_length=100)
    existing_order_number = serializers.CharField(max_length=100,allow_null=True,allow_blank=True,default='')
    description = serializers.CharField(max_length=10000)
    upload_attachments = serializers.CharField(max_length=100,allow_null=True,allow_blank=True,default='')
    product_type = serializers.CharField(max_length=100,allow_null=True,allow_blank=True,default='')
    brand = serializers.CharField(max_length=100,allow_null=True,allow_blank=True)

class getInTouchChangeStatusserializer(serializers.Serializer):
    status_ticket = serializers.CharField(max_length=100)
    id = serializers.IntegerField()

class postAddressSerializer(serializers.Serializer):
    address_type = serializers.CharField(max_length=10, default='HOME')
    address_nickname = serializers.CharField(max_length=100, allow_null=True, default='')
    address = serializers.CharField(max_length=100, default='', allow_null=True)


class UpdateAddresserializer(serializers.Serializer):
    address_type = serializers.CharField(max_length=10)
    address_nickname = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=100)
    address_id = serializers.CharField(max_length=100)

class DeleteAddressserializer(serializers.Serializer):
    address_id = serializers.CharField(max_length=100)

class checkpartitionSerializer(serializers.Serializer):
    width = serializers.CharField(max_length=100)
    existing_partition = serializers.JSONField()
    input_required = serializers.CharField(max_length=100)


class ColumnModificationSerializer(serializers.Serializer):
    width = serializers.CharField(max_length=100)
    existing_partition = serializers.JSONField()
    input_required = serializers.CharField(max_length=100)
    column_number = serializers.CharField(max_length=10)


class ColumnDeletionSerializer(serializers.Serializer):
    delete_width = serializers.CharField(max_length=100)
    left_width = serializers.CharField(max_length=100)
    existing_partition = serializers.JSONField()


class RowModification(serializers.Serializer):
    delete_basket = serializers.CharField(max_length=100)
    existing_partition = serializers.JSONField()
    occupy = serializers.CharField(max_length=100)


class ChangeBasketSerializer(serializers.Serializer):
    existing_partition = serializers.JSONField()
    oldBasketName = serializers.CharField(max_length=100)
    newBasketName = serializers.CharField(max_length=100)
    rownumber = serializers.CharField(max_length=100)

class WishlistUserSerializer(serializers.Serializer):
    product_list = serializers.JSONField()

class StatusChangeWishlistSerializer(serializers.Serializer):
    wishlist_ID = serializers.CharField(max_length=100)


class StatusChangeSavecartSerializer(serializers.Serializer):
    savecart_ID = serializers.CharField(max_length=100)


class assignloyaltySerializer(serializers.Serializer):
    order_amount = serializers.IntegerField()


class calculateQuantificationSerializer(serializers.Serializer):
    total_length_of_slab = serializers.IntegerField(required=False,allow_null=True)
    slab_depth = serializers.IntegerField(required=False,allow_null=True)
    no_of_corners = serializers.IntegerField(required=False, allow_null=True)
    clear_height = serializers.IntegerField(required=False, allow_null=True)
    no_of_partitions = serializers.IntegerField(required=False, allow_null=True)
    product_category = serializers.CharField(max_length=100)
    usecase = serializers.CharField(max_length=100)
    area_choosen = serializers.CharField(max_length=100,required=False,allow_null=True)


class professionalSignupSerializer(serializers.Serializer):
    professionalUsername = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100, default='')
    mobile = serializers.CharField(max_length=100, default='')
    password = serializers.CharField(max_length=100)
    c_password = serializers.CharField(max_length=100)
    professional_type = serializers.CharField(max_length=100)
    expert_areas = serializers.JSONField(allow_null=True)
    assign_work_status = serializers.JSONField(allow_null=True,required=False)
    is_verified_email = serializers.BooleanField(default=False)
    is_verified_mobile = serializers.BooleanField(default=False)
    otp = serializers.CharField(max_length=6, allow_null=True,required=False)


class bookAServiceSerializer(serializers.Serializer):
    requestType = serializers.CharField(max_length=100)
    requestDescription = serializers.CharField(max_length=100)

class optAServiceSerializer(serializers.Serializer):
    serviceid = serializers.CharField(max_length=100)


class UpdatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100)


class communicationPreferenceSerializer(serializers.Serializer):
    communication_preference = serializers.CharField(max_length=100)

class CategorySerializer(serializers.Serializer):
    category_name = serializers.CharField(max_length=100)


class subCategorySerializer(serializers.Serializer):
    subCategory_name = serializers.CharField(max_length=100)


class subSubCategorySerializer(serializers.Serializer):
    item_type = serializers.CharField(max_length=100)


class product(serializers.Serializer):
    product_id = serializers.CharField(max_length=100)
    productName = serializers.CharField(max_length=100)
    brandName = serializers.CharField(max_length=100)
    price = serializers.IntegerField()

class productDetail(serializers.Serializer):
    productFeature = serializers.JSONField()