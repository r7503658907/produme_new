import json
import datetime
from datetime import datetime
from .serializers import *
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import *
import random
import string
# from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
import math
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .emails import send_otp_forgot_mail
from django.contrib.auth.hashers import make_password
import requests
from geopy.geocoders import Nominatim
import pandas as pd
from pathlib import Path


def calculate_basket(key, value, length_basket_mapping, final_basket, clear_height):
    partition_name = length_basket_mapping[value + 1]
    print(partition_name)
    final_partition_name = str(partition_name) + str(clear_height)
    print("final_partition_name===", final_partition_name)
    basket_data = PartitionBasketDetails.objects.filter(partition_name=final_partition_name).values()[0]
    # print(basket_data)
    final_basket[key + str(partition_name)] = basket_data
    return final_basket


def width_caluclator(length_data, key, width_data_per_length, partitionCalculator):
    if int(length_data[key]) < int(partitionCalculator['length_data_condition_check1']):
        print('Ist condition width')

    elif int(length_data[key]) in range(int(partitionCalculator['length_data_condition_check1']),
                                        int(partitionCalculator['length_data_condition_check2'])):
        value = int(length_data[key]) / 2
        print(value)
        for i in range(2):
            width_data_per_length[str(i + 1) + key] = value

        return width_data_per_length

    elif int(length_data[key]) >= int(partitionCalculator['length_data_condition_check2']):
        value = int(length_data[key]) / int(partitionCalculator['length_data_condition_check3'])
        int_value = int(value)
        for i in range(int_value):
            width_data_per_length[str(i + 1) + key] = int(partitionCalculator['length_data_condition_check3'])
        width_partition = int(partitionCalculator['length_data_condition_check3']) * int_value
        remaining_value = int(length_data[key]) - width_partition
        # print(width_data_per_length)
        if remaining_value < int(partitionCalculator['length_data_condition_check4']):
            value = remaining_value / int_value
            # print(value)
            for i in range(int_value):
                width_data_per_length[str(i + 1) + key] = width_data_per_length[str(i + 1) + key] + value

        elif remaining_value >= int(partitionCalculator['length_data_condition_check4']):
            print(remaining_value)
            width_data_per_length["Extra" + key] = remaining_value

        print('final=', width_data_per_length)
        return width_data_per_length


def no_of_columns_caluclator(length_data, key, no_of_columns_per_length, partitionCalculator):
    print("no_of_columns_caluclator=", int(length_data[key]))
    if int(length_data[key]) < int(partitionCalculator['length_data_condition_check1']):
        no_of_columns_per_length[key] = int(partitionCalculator['partition_value1'])
        return no_of_columns_per_length

    elif int(length_data[key]) in range(int(partitionCalculator['length_data_condition_check1']),
                                        int(partitionCalculator['length_data_condition_check2'])):
        no_of_columns_per_length[key] = int(partitionCalculator['partition_value2'])
        return no_of_columns_per_length

    elif int(length_data[key]) >= int(partitionCalculator['length_data_condition_check2']):
        # print('elif block=',int(length_data[key]))
        value = int(length_data[key]) % int(partitionCalculator['length_data_condition_check3'])
        var = int(length_data[key]) / int(partitionCalculator['length_data_condition_check3'])
        # print("div float value=", var)
        div_value = int(length_data[key]) / int(partitionCalculator['length_data_condition_check3'])
        # div_value = math.floor(div_value_int) + 1 #roundup
        # print("Remainder=",value," ","actual_value =",div_value)

        if value < int(partitionCalculator['length_data_condition_check4']):
            no_of_columns_per_length[key] = int(div_value)

        elif value >= int(partitionCalculator['length_data_condition_check4']):
            no_of_columns_per_length[key] = int(div_value) + 1

        # elif value ==6:
        #     no_of_columns_per_length[key] = div_value + 1

        return no_of_columns_per_length


class userSignup(APIView):
    def post(self, request):
        serializer = signupSerializer(data=request.data)
        try:
            if serializer.is_valid():
                email = serializer.data['email']
                name = serializer.data["name"]
                password = serializer.data['password']
                username = 'prodyme' + ''.join(
                    random.choices(string.digits + string.ascii_letters, k=random.randint(10, 14)))

                prodymeUser.objects.create(
                    email=email,
                    name=name,
                    password=password,
                    username=username,
                )
                User.objects.create_user(username=username, password=password, email=email)
                data = prodymeUser.objects.filter(username=username).values()[0]["username"]
                print(data)
                
                profile.objects.create(
                    username_id=data,
                    profile_id=username,
                    email=email,
                    password=password,
                    first_name=name
                )
                CommunicationPreference.objects.create(
                    username_id=email,
                    communication_preference="False"
                )
                return JsonResponse({
                    'status': 200,
                    'message': 'Registration Successfully',
                    'is_verified_email': serializer.data['is_verified_email'],
                    'is_verified_mobile': serializer.data['is_verified_email']
                })
            return JsonResponse({
                "status": 400,
                "message": serializer.errors
            })
            # if prodymeUser.objects.filter(email=email).exists():
            #     return JsonResponse({
            #         "status": 400,
            #         "message": "User Already Exist With Provided Email-ID",
            #         })
            # if mobile == '' and email == '':
            #     return JsonResponse({
            #     "status": 400,
            #     "message": "Please Enter Either E-mail or Phone Number",
            #     })
            # if email!='':
            #     if prodymeUser.objects.filter(email=email).exists():
            #         return JsonResponse({
            #         "status": 400,
            #         "message": "User Already Exist With Provided Email-ID",
            #         })
            # if mobile !='':
            #     if prodymeUser.objects.filter(mobile=mobile).exists():
            #         return JsonResponse({
            #         "status": 400,
            #         "message": "User Already Exist With Provided Mobile",
            #         })

            # if len(mobile) not in (0, 10):
            #     return JsonResponse({
            #         "status": 400,
            #         "message": "Incorrect Phone Number Length",
            #     })

        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })


class smartBuilder(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = smartBuilderSerializer(data=request.data)
        if serializer.is_valid():
            type_of_kitchen = serializer.data['type_of_kitchen']
            length1 = serializer.data['length1']
            length2 = serializer.data['length2']
            length3 = serializer.data['length3']
            length4 = serializer.data['length4']
            length5 = serializer.data['length5']
            length6 = serializer.data['length6']
            corner_side = serializer.data['corner_side']
            partitionaliascalculator = serializer.data['partitionaliascalculator']
            partitionCalculator = \
                smartBuilderPartitionCalculator.objects.filter(
                    partitionaliascalculator=partitionaliascalculator).values()[
                    0]
            print("partitionCalculator=", partitionCalculator)
            smartbuilderdesignsave = {}
            sink_side = serializer.data['sink_side']
            clear_height = serializer.data['clear_height']
            design_name = serializer.data['design_name']
            smartbuilder_data = SmartBuilder.objects.filter(type_of_kitchen=type_of_kitchen).values()[0]
            # print(smartbuilder_data)

            no_of_len = smartbuilder_data['no_of_len']
            print("no_of_len===", no_of_len)
            no_of_corners = smartbuilder_data['no_of_corners']
            corner_placed_on_side = smartbuilder_data['corner_placed_on_side']
            length_data = {}
            for var in range(int(no_of_len)):
                key = "length" + str(var + 1)
                length_data[key] = key
            print("length_data = ", length_data)
            for var in length_data.keys():
                length_data[var] = serializer.data[var]
            print("Final user len data =", length_data)
            smartbuilderdesignsave['length_name'] = length_data  # 1st Save
            # Balance after sink
            key_sink_deduct = 'length' + sink_side
            print("key_sink_deduct =", key_sink_deduct)
            length_data[key_sink_deduct] = int(length_data[key_sink_deduct]) - 24
            print("Balance after sink deduction = ", length_data)
            smartbuilderdesignsave['balance_after_sink'] = length_data

            # corner_placed_on_side #glitch
            corner_data = smartbuilder_data['corner_placed_on_side']
            corner_loop = corner_data.split(":")
            # print(corner_loop)
            for var in corner_loop:
                length_data[var] = int(length_data[var]) - 17

            print("corner_placed_on_side = ", length_data)
            smartbuilderdesignsave['corner_on_which_side'] = str(corner_data)
            smartbuilderdesignsave['balance_after_corner'] = length_data
            no_of_columns_per_length = {}
            width_data_per_length = {}
            for key, value in length_data.items():
                print('key = ', key)
                # print('value = ', value)
                # print('length_data = ', length_data)
                no_of_columns_caluclator(length_data, key, no_of_columns_per_length, partitionCalculator)
                width_caluclator(length_data, key, width_data_per_length, partitionCalculator)

            print("NOFCPL=", no_of_columns_per_length)
            smartbuilderdesignsave['no_of_columns'] = no_of_columns_per_length
            smartbuilderdesignsave['design_name'] = design_name
            smart_builder_design = {}
            smart_builder_design['design_name'] = design_name
            smart_builder_design['length_data'] = length_data
            smart_builder_design['no_of_columns_per_length'] = no_of_columns_per_length

            length_basket_mapping = {1: "PA", 2: "PB", 3: "PC", 4: "PD", 5: "PE", 6: "PF"}
            final_basket = {}
            for key in no_of_columns_per_length:
                print("key=======", key)
                for value in range(no_of_columns_per_length[key]):
                    print("value=", value)
                    print("length_basket_mapping===", length_basket_mapping)
                    print("final_basket===", final_basket)
                    print("clear_height", clear_height)
                    calculate_basket(key, value, length_basket_mapping, final_basket, clear_height)
            # print(final_basket)
            result = {

                "Message": "Smart Builder Design Details",
                "results": serializer.data,
                "width_calculator": width_data_per_length,
                "smart_builder_design": smart_builder_design,
                "partition_data": final_basket

            }

            # userprodyme = prodymeUser.objects.get(username=request.user)
            # print(userprodyme)
            # smartbuilderdesignsave['user_id'] = str(userprodyme)
            print("smartbuilderdesignsave=", smartbuilderdesignsave)
            # SmartBuilderDesign.objects.create(**smartbuilderdesignsave)

            return JsonResponse(result, status=status.HTTP_200_OK, safe=False)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class partitionModification(APIView):
    def post(self, request):
        serializer = partitionModificationSerializer(data=request.data)
        if serializer.is_valid():
            input_dict = serializer.data
            clear_height = serializer.data['clear_height']
            no_of_columns_per_length = serializer.data['no_of_columns_per_length']
            lenght_list_name = ['length1', 'length2', 'length3', 'length4', 'length5', 'length6']
            for key in input_dict.keys():
                if input_dict[key] is not None and key in lenght_list_name:
                    print("key=", key)

            length_basket_mapping = {1: "PA", 2: "PB", 3: "PC", 4: "PD"}
            final_basket = {}

            for value in range(no_of_columns_per_length):
                print("value=", value)
                calculate_basket(key, value, length_basket_mapping, final_basket, clear_height)

            result = {

                "Message": "Smart Builder Modification Partition Details",
                "partition_data": final_basket

            }

            return JsonResponse(result, status=status.HTTP_200_OK, safe=False)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class updateProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            serializer = updateProfileSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                mobile = serializer.data['mobile']
                password = serializer.data['password']
                first_name = serializer.data['first_name']
                last_name = serializer.data['last_name']
                business_name = serializer.data['business_name']
                gst = serializer.data['gst']

                print(serializer.data)
                user = request.user
                input_dict = {}
                for key in serializer.data.keys():
                    if serializer.data[key] is not None:
                        input_dict[key] = serializer.data[key]
                print(input_dict)
                profile.objects.filter(profile_id=user).update(
                    **input_dict
                )
                return Response({
                    'status': 200,
                    'message': 'Profile Update Successfully',
                    'data': input_dict
                })
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong'
            })


class userForgotPassword(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = forgotPasswordSerializer(data=data)
            if serializer.is_valid():
                print(serializer.data['email'])
                send_otp_forgot_mail(serializer.data['email'])
                return Response({
                    'status': 200,
                    'message': 'E-mail sent successfully Please check email'
                })
            return Response({
                'status': 400,
                'message': 'Something went Wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)


class verifyResetPassword(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = verifyResetPasswordSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                password = serializer.data['password']
                confirm_password = serializer.data['confirm_password']

                user = prodymeUser.objects.filter(email=email)

                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': 'Something went worng',
                        'data': 'Invalid Email'
                    })

                if password != confirm_password:
                    return JsonResponse({
                        "status": 400,
                        "message": "Passwords Don't Match",
                    })

                if not user[0].otp == otp:
                    return Response({
                        'status': 400,
                        'message': 'Something went wrong',
                        'data': 'Wrong OTP'
                    })
                user = user.first()
                user.password = password
                user.save()
                print(user)
                profile.objects.filter(profile_id=user).update(
                    password=password
                )
                User.objects.filter(username=user).update(
                    password=make_password(password))
                return Response({
                    'status': 200,
                    'message': 'Password Reset Successfully',
                    'data': serializer.data
                })
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)


class emailVerify(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            serializer = forgotPasswordSerializer(data=data)
            if serializer.is_valid():
                print(serializer.data['email'])
                send_otp_forgot_mail(serializer.data['email'])
                return Response({
                    'status': 200,
                    'message': 'E-mail sent successfully Please check email'
                })
            return Response({
                'status': 400,
                'message': 'Something went Wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)


class emailVerifyValidate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            serializer = emailVerifyValidateSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = prodymeUser.objects.filter(email=email)

                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': 'Something went worng',
                        'data': 'Invalid Email'
                    })

                if not user[0].otp == otp:
                    return Response({
                        'status': 400,
                        'message': 'Something went wrong',
                        'data': 'Wrong OTP'
                    })

                prodymeUser.objects.filter(email=email).update(
                    is_verified_email=True
                )
                return Response({
                    'status': 200,
                    'message': 'Email Verified Successfully',
                    'data': serializer.data
                })
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)


class cabinetstructure1(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            serializer = cabinetstructure1Serializer(data=data)
            if serializer.is_valid():
                total_length_of_slab = int(serializer.data['total_length_of_slab'])
                slab_depth = int(serializer.data['slab_depth'])
                no_of_corner = int(serializer.data['no_of_corner'])
                no_of_partition = int(serializer.data['no_of_partition'])
                clear_height = int(serializer.data['clear_height'])
                area_chosen = serializer.data['area_chosen']
                area_split = area_chosen.split('*')
                # print(area_split)
                final_area = int(area_split[0]) * int(area_split[1])
                # print(final_area)
                required_quantity = 2 * (total_length_of_slab * slab_depth + (no_of_corner * (slab_depth ^ 2))) + ((
                                                                                                                           no_of_partition + 1) * clear_height * slab_depth) + no_of_corner * clear_height * slab_depth
                # print(required_quantity)
                value = required_quantity / final_area
                # print(value)
                primary_display_quantity = math.floor(value) + 1  # roundup
                print(primary_display_quantity)

                secondary_display_amount = primary_display_quantity * final_area
                print(secondary_display_amount)

                return Response({
                    'status': 200,
                    'message': 'Cabinet Structure Required Quantity',
                    'data': {
                        "primary_display_quantity": primary_display_quantity,
                        "secondary_display_amount": secondary_display_amount
                    }
                })
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)


class userLogin(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = userLoginSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']

                data = prodymeUser.objects.filter(email=email).values()[0]
                print(data)
                url = "http://127.0.0.1:8000/login2/"
                cred = {"email": data['email'], "password": password}
                login_status = requests.post(url, data=cred)
                x = login_status.json()
                print(x, type(x))
                print(list(x.keys()))
                if list(x.keys())[0] in "non_field_errors":
                    return JsonResponse({
                        'status': 400,
                        'message': 'Invalid Credential'
                    })

                return Response({
                    'status': 200,
                    'message': "Login Successful",
                    'token': login_status.text,

                })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': "Username & Password Not Correct"
            })


class getProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            print(user)
            data = profile.objects.filter(profile_id=user).values()[0]
            print(data)
            return Response({
                'status': 200,
                'data': data
            })

        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'Error': str(e)
            })


class getInTouch(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = getInTouchSerializer(data=data)
            if serializer.is_valid():
                first_name = serializer.data['first_name']
                last_name = serializer.data['last_name']
                email = serializer.data['email']
                mobile = serializer.data['mobile']
                zipcode = serializer.data['zipcode']
                state = serializer.data['state']
                subject = serializer.data['subject']
                existing_order_number = serializer.data['existing_order_number']
                description = serializer.data['description']
                upload_attachments = serializer.data['upload_attachments']
                product_type = serializer.data['product_type']
                brand = serializer.data['brand']
                input_dict = {}
                username = 'prodyme' + ''.join(
                    random.choices(string.digits + string.ascii_letters, k=random.randint(10, 14)))
                for key in serializer.data.keys():
                    if serializer.data[key] is not None:
                        input_dict[key] = serializer.data[key]
                print(input_dict)
                GetInTouchModel.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    mobile=mobile,
                    zipcode=zipcode,
                    state=state,
                    subject=subject,
                    existing_order_number=existing_order_number,
                    description=description,
                    upload_attachments=upload_attachments,
                    product_type=product_type,
                    brand=brand
                )
                try:
                    emailData = prodymeUser.objects.filter(email=email).values()[0]
                    print(emailData)
                    if str(emailData["email"]) == email:
                        return Response({
                            'status': 200,
                            'message': 'Thanks for the Query! Will Update you soon',
                        })
                except Exception as e:
                    prodymeUser.objects.create(
                        email=email,
                        password="password",
                        username=username,
                    )
                    User.objects.create_user(username=username, password=make_password("password"), email=email)
                    profile.objects.create(
                        username_id=username,
                        profile_id=username,
                        email=email,
                        mobile=mobile,
                        password="password"
                    )
                    CommunicationPreference.objects.create(
                        username_id=email,
                        communication_preference="False"
                    )
                    return Response({
                        'status': 200,
                        'message': 'Thanks for the Query! Will Update you soon',
                    })
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong'
            })


class postAddress(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = postAddressSerializer(data=request.data)
            if serializer.is_valid():
                address_type = serializer.data['address_type']
                address_nickname = serializer.data['address_nickname']
                address = serializer.data['address']

                address_id = 'prodyme_add_' + ''.join(
                    random.choices(string.digits + string.ascii_letters, k=random.randint(10, 14)))
                user = request.user
                print("user=", user)
                profile_address.objects.create(
                    username_id=user,
                    address_id=address_id,
                    address_type=address_type,
                    address_nickname=address_nickname,
                    address=address
                )

            return Response({
                'status': 200,
                'data': "Address Added Successfully"
            })

        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'Error': str(e)
            })


class getAddress(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            print(user, type(user))
            data = profile_address.objects.filter(username_id=str(user)).values()
            print(data)
            return Response({
                'status': 200,
                'data': data
            })

        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'Error': str(e)
            })


class getDetailAddres(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, address_id):
        try:
            user = request.user
            print(user, type(user))
            data = profile_address.objects.filter(username_id=str(user), address_id=address_id).values()
            print(data)
            return Response({
                'status': 200,
                'data': data
            })

        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'Error': str(e)
            })


class UpdateAddres(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = UpdateAddresserializer(data=request.data)
            if serializer.is_valid():
                address_id = serializer.data["address_id"]
                user = request.user
                print(user, type(user))
                data = profile_address.objects.filter(username_id=str(user), address_id=address_id).update(
                    **serializer.data
                )
                print(data)
                return Response({
                    'status': 200,
                    'data': data
                })
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'Error': str(e)
            })


class DeleteAddress(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = DeleteAddressserializer(data=request.data)
            if serializer.is_valid():
                address_id = serializer.data["address_id"]
                user = request.user
                print(user, type(user))
                data = profile_address.objects.filter(username_id=str(user), address_id=address_id).delete()
                print(data)
                return Response({
                    'status': 200,
                    'message': "Address Deleted Successfully"
                })
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'Error': str(e)
            })


class getLoggedTickets(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            print(user, type(user))
            email_data = prodymeUser.objects.filter(username=str(user)).values()[0]
            print(email_data['email'])
            data = GetInTouchModel.objects.filter(email=email_data['email']).values()
            print(data)
            return Response({
                'status': 200,
                'data': data
            })

        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'Error': str(e)
            })


class getspecificloggedTickets(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            user = request.user
            print(user, type(user))
            email_data = prodymeUser.objects.filter(username=str(user)).values()[0]
            print(email_data['email'])
            data = GetInTouchModel.objects.filter(email=email_data['email'], id=id).values()
            print(data)
            return Response({
                'status': 200,
                'data': data
            })

        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'Error': str(e)
            })


class getInTouchChangeStatus(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = getInTouchChangeStatusserializer(data=request.data)
            if serializer.is_valid():
                status_ticket = serializer.data["status_ticket"]
                id = serializer.data["id"]
                user = request.user
                print(user, type(user))
                email_data = prodymeUser.objects.filter(username=str(user)).values()[0]
                print(email_data['email'])
                data = GetInTouchModel.objects.filter(email=email_data['email'], id=id).update(
                    status_ticket=status_ticket)
                print(data)
            return Response({
                'status': 200,
                'data': "Ticket Status Updated Sucessfully"
            })

        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'Error': str(e)
            })


class checkPartions(APIView):
    def post(self, request):
        try:
            validator = {
                "Bottle Rack": 6,
                "General": 12,
                "Plates & Cups Saucer ": 12,
                "Cultlery": 12
            }
            data = request.data
            serializer = checkpartitionSerializer(data=data)
            if serializer.is_valid():
                width = serializer.data['width']
                existing_partition = serializer.data['existing_partition']
                input_required = serializer.data['input_required']

                print(width, existing_partition, input_required)
                final_width = int(width) - int(validator[input_required])
                print('width After Adjusting=', final_width)

                for i in validator.keys():
                    if validator[i] > final_width:
                        return Response({
                            'status': 200,
                            'message': 'Component cannot Attach',
                        })
                return Response({
                    'status': 200,
                    'message': 'Component can Attach',
                })
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)


class columnModification(APIView):
    def post(self, request):
        validator = {
            "General": 12,
            "Plates": 12,
            "Cutlery": 12,
            "Bottle Rack": 6
        }
        data = request.data
        serializer = ColumnModificationSerializer(data=data)
        if serializer.is_valid():
            width = serializer.data['width']
            existing_partition = serializer.data['existing_partition']
            input_required = serializer.data['input_required']
            column_number = serializer.data['column_number']

            if input_required == "Bottle Rack":
                old_width_rem = int(width) - int(validator["Bottle Rack"])
                print("old_width_rem=", old_width_rem)
                for i in validator.keys():
                    if old_width_rem < validator[i]:
                        return Response({
                            'status': 400,
                            'message': 'Modification Cant be achieved with this configuration',

                        })
                    else:
                        existing_partition[validator["Bottle Rack"]] = "Bottle Rack"
                        existing_partition[old_width_rem] = existing_partition[width]
                        del existing_partition[width]

                        return Response({
                            'status': 200,
                            'message': 'New Column Redistribution',
                            'new_partition': existing_partition
                        })

            if input_required == "General":
                old_width_rem = int(width) - int(validator["General"])
                print("old_width_rem=", old_width_rem)
                for i in validator.keys():
                    if old_width_rem < validator[i]:
                        return Response({
                            'status': 400,
                            'message': 'Modification Cant be achieved with this configuration',

                        })
                    else:
                        length_of_existing = len(existing_partition[width])
                        existing_partition[str(int(column_number) + 1) + '_' + str(validator["General"])] = list(
                            ["General"]) * length_of_existing
                        existing_partition[str(column_number) + '_' + str(old_width_rem)] = existing_partition[width]
                        del existing_partition[width]

                        return Response({
                            'status': 200,
                            'message': 'New Column Redistribution',
                            'new_partition': existing_partition
                        })

            if input_required == "Plates":
                old_width_rem = int(width) - int(validator["Plates"])
                print("old_width_rem=", old_width_rem)
                for i in validator.keys():
                    if old_width_rem < validator[i]:
                        return Response({
                            'status': 400,
                            'message': 'Modification Cant be achieved with this configuration',

                        })
                    else:
                        length_of_existing = len(existing_partition[width])
                        list_of_baskets = list(["Plates"]) * length_of_existing
                        list_of_baskets[0] = "Cups & Sauccer"
                        existing_partition[
                            str(int(column_number) + 1) + '_' + str(validator["Plates"])] = list_of_baskets
                        existing_partition[str(column_number) + '_' + str(old_width_rem)] = existing_partition[width]
                        del existing_partition[width]

                        return Response({
                            'status': 200,
                            'message': 'New Column Redistribution',
                            'new_partition': existing_partition
                        })

            if input_required == "Cutlery":
                old_width_rem = int(width) - int(validator["Cutlery"])
                print("old_width_rem=", old_width_rem)
                for i in validator.keys():
                    if old_width_rem < validator[i]:
                        return Response({
                            'status': 400,
                            'message': 'Modification Cant be achieved with this configuration',

                        })
                    else:
                        length_of_existing = len(existing_partition[width])
                        list_of_baskets = list(["General"]) * length_of_existing
                        list_of_baskets[0] = "Cutlery"
                        existing_partition[
                            str(int(column_number) + 1) + '_' + str(validator["Cutlery"])] = list_of_baskets
                        existing_partition[str(column_number) + '_' + str(old_width_rem)] = existing_partition[width]
                        del existing_partition[width]

                        return Response({
                            'status': 200,
                            'message': 'New Column Redistribution',
                            'new_partition': existing_partition
                        })
        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })


class columnDeletion(APIView):
    def post(self, request):
        data = request.data
        serializer = ColumnDeletionSerializer(data=data)
        if serializer.is_valid():
            delete_width = serializer.data['delete_width']
            left_width = serializer.data['left_width']
            existing_partition = serializer.data['existing_partition']

            new_width = int(delete_width) + int(left_width)
            existing_partition[new_width] = existing_partition[delete_width]
            del existing_partition[delete_width]

            return Response({
                'status': 200,
                'message': 'New Column Redistribution',
                'new_partition': existing_partition
            })
        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })


class rowAddition(APIView):
    def post(self, request):
        data = request.data
        serializer = RowModification(data=data)
        if serializer.is_valid():
            existing_partition = serializer.data['existing_partition']
            delete_basket = serializer.data['delete_basket']
            occupy = serializer.data['occupy']
            del existing_partition[delete_basket]
            new_width = int(occupy) + int(delete_basket)
            existing_partition[str(new_width)] = existing_partition[occupy]
            del existing_partition[occupy]

            return Response({
                'status': 200,
                'message': 'New Column Redistribution',
                'new_partition': existing_partition
            })
        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })


class changeBasket(APIView):
    def post(self, request):
        data = request.data
        serializer = ChangeBasketSerializer(data=data)
        if serializer.is_valid():
            existing_partition = serializer.data['existing_partition']
            oldBasketName = serializer.data['oldBasketName']
            newBasketName = serializer.data['newBasketName']
            rownumber = serializer.data['rownumber']

            return Response({
                'status': 200,
                'message': 'New Column Redistribution',
                'new_partition': existing_partition
            })
        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })


class WishlistUserCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = WishlistUserSerializer(data=data)
        if serializer.is_valid():
            product_list = serializer.data['product_list']
            user = request.user
            userprodyme = prodymeUser.objects.get(username=request.user)
            print(userprodyme)
            wishlist_ID = 'wishlist' + ''.join(
                random.choices(string.digits + string.ascii_letters, k=random.randint(10, 14)))

            Wishlist.objects.create(
                username_id=str(user),
                product_list=product_list,
                wishlist_ID=wishlist_ID,
                status=0
            )

            return Response({
                'status': 200,
                'message': "Product List Added to WishList",
                'new_partition': product_list
            })
        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })


class StatusChangeWishlist(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = StatusChangeWishlistSerializer(data=data)
        if serializer.is_valid():
            wishlist_ID = serializer.data['wishlist_ID']
            user = request.user
            userprodyme = prodymeUser.objects.get(username=request.user)
            print(userprodyme)

            Wishlist.objects.filter(wishlist_ID=wishlist_ID).update(status="1")
            Wishlist.objects.filter(wishlist_ID=wishlist_ID).delete()

            return Response({
                'status': 200,
                'message': "Products Removed From WishList"
            })
        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })


class getWishlist(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            userprodyme = prodymeUser.objects.get(username=request.user)
            print(userprodyme)
            data = Wishlist.objects.filter(username_id=str(user)).values()
            print(data)
            return Response({
                'status': 200,
                'message': "Wishlist ALl Data",
                "wishlist": data
            })
        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })


class savecartUserCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = WishlistUserSerializer(data=data)
        if serializer.is_valid():
            product_list = serializer.data['product_list']
            user = request.user
            userprodyme = prodymeUser.objects.get(username=request.user)
            print(userprodyme)
            savecartID = 'savecart' + ''.join(
                random.choices(string.digits + string.ascii_letters, k=random.randint(10, 14)))

            SavedCart.objects.create(
                username_id=str(user),
                product_list=product_list,
                SavedCart_ID=savecartID,
                status=0
            )
            return Response({
                'status': 200,
                'message': "Product List Added to SaveCart",
                'new_partition': product_list
            })
        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })


class StatusChangeSaveCart(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = StatusChangeSavecartSerializer(data=data)
        if serializer.is_valid():
            savecart_ID = serializer.data['savecart_ID']
            user = request.user
            userprodyme = prodymeUser.objects.get(username=request.user)
            print(userprodyme)

            SavedCart.objects.filter(SavedCart_ID=savecart_ID).update(status="1")
            SavedCart.objects.filter(SavedCart_ID=savecart_ID).delete()

            return Response({
                'status': 200,
                'message': "Products Removed From SaveCart"
            })
        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })


class getSaveCart(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            userprodyme = prodymeUser.objects.get(username=request.user)
            print(userprodyme)
            data = SavedCart.objects.filter(username_id=str(user)).values()
            print(data)
            return Response({
                'status': 200,
                'message': "SaveCart ALl Data",
                "wishlist": data
            })
        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })


class getSaveCartPanda(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            userprodyme = prodymeUser.objects.get(username=request.user)
            print(userprodyme)
            data = SavedCart.objects.filter(username_id=str(user)).values()
            print(data)
            finalResult = []
            for var in data:
                finalResult.append(var["product_list"])
            df = pd.DataFrame()
            data2 = df.append(finalResult, ignore_index=True)
            # print(data2)

            output = pd.DataFrame(data2)
            filePath = Path().absolute()
            print(filePath)
            filename = str(filePath) + "/" + "report" + "/" + str(user) + ".xlsx"
            print(filename)
            boqAudit.objects.create(
                username_id=str(user),
                filename=filename,
                datetime=datetime.datetime.now()
            )
            output.to_excel(filename)
            print(output)

            return Response({
                'status': 200,
                'message': "SaveCart ALl Data",
                "SaveCart": data2
            })
        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })


class getSaveCartWishlist(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            userprodyme = prodymeUser.objects.get(username=request.user)
            print(userprodyme)
            data = Wishlist.objects.filter(username_id=str(user)).values()
            print(data)
            finalResult = []
            for var in data:
                finalResult.append(var["product_list"])
            df = pd.DataFrame()
            data2 = df.append(finalResult, ignore_index=True)
            # print(data2)

            output = pd.DataFrame(data2)
            filePath = Path().absolute()
            print(filePath)
            filename = str(filePath) + "/" + "report" + "/" + str(user) + ".xlsx"
            print(filename)
            boqAudit.objects.create(
                username_id=str(user),
                filename=filename,
                datetime=datetime.datetime.now()
            )
            print(boqAudit)
            output.to_excel(filename)
            print(output)

            return Response({
                'status': 200,
                'message': "wishlist ALl Data",
                "SaveCart": data2
            })
        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })


class assignloyaltyUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = assignloyaltySerializer(data=data)
        if serializer.is_valid():
            order_amount = serializer.data['order_amount']
            user = request.user
            userprodyme = prodymeUser.objects.get(username=request.user)
            print(userprodyme)
            loyalty_ID = 'loyalty_ID' + ''.join(
                random.choices(string.digits + string.ascii_letters, k=random.randint(10, 14)))

            loyaltyPoints = (int(order_amount) * 10) / 100
            print(loyaltyPoints)

            Loyalty.objects.create(
                username_id=str(user),
                order_amount=order_amount,
                loyaltyPoints=loyaltyPoints,
                loyalty_ID=loyalty_ID
            )

            return Response({
                'status': 200,
                'message': "Loyalty Points Added",
            })
        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })


class getLoyaltyPoints(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            userprodyme = prodymeUser.objects.get(username=request.user)
            print(userprodyme)
            data = Loyalty.objects.filter(username_id=str(user)).values()
            print(data)
            total_loyalty_points = 0
            for var in data:
                print(var['loyaltyPoints'])
                total_loyalty_points += int(var['loyaltyPoints'])
            return Response({
                'status': 200,
                'message': "Loyalty Points Data",
                'loyaltyPoints': total_loyalty_points
            })
        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': str(e)
            })


class calculateQuantification(APIView):
    def post(self, request):
        data = request.data
        serializer = calculateQuantificationSerializer(data=data)
        if serializer.is_valid():
            product_category = serializer.data['product_category']
            usecase = serializer.data['usecase']
            print(product_category)
            print(usecase)
            if product_category == "Cabinet Structure" and usecase == "kitchen cabinets":
                total_length_of_slab = serializer.data['total_length_of_slab']
                slab_depth = serializer.data['slab_depth']
                no_of_corners = serializer.data['no_of_corners']
                clear_height = serializer.data['clear_height']
                no_of_partitions = serializer.data['no_of_partitions']
                area_choosen = serializer.data['area_choosen']

                formula = 2 * (total_length_of_slab * slab_depth + (no_of_corners * (slab_depth ** 2))) + (
                        (no_of_partitions + 1) * clear_height * slab_depth) + (
                                  no_of_corners * clear_height * slab_depth)
                no_of_boards = formula
                area_choosen_lsit = area_choosen.split("*")
                print(area_choosen_lsit)
                area_of_item_chosen = int(area_choosen_lsit[0]) * int(area_choosen_lsit[1])
                primary_display_quantity = math.floor((formula / area_of_item_chosen) + 1)
                print(primary_display_quantity)
                Secondary_display_quantity = primary_display_quantity * area_of_item_chosen
                print(Secondary_display_quantity)

                return Response({
                    'status': 200,
                    'message': "Quantification Data",
                    "no_of_boards": no_of_boards,
                    "primary_display_quantity": primary_display_quantity,
                    "Secondary_display_quantity": Secondary_display_quantity
                })

            if product_category == "Cabinet Structure" and usecase == "Shutters":
                total_length_of_slab = serializer.data['total_length_of_slab']
                clear_height = serializer.data['clear_height']
                area_choosen = serializer.data['area_choosen']
                formula = total_length_of_slab * clear_height
                area_choosen_lsit = area_choosen.split("*")
                print(area_choosen_lsit)
                area_of_item_chosen = int(area_choosen_lsit[0]) * int(area_choosen_lsit[1])
                primary_display_quantity = math.floor((formula / area_of_item_chosen) + 1)
                print(primary_display_quantity)
                Secondary_display_quantity = primary_display_quantity * area_of_item_chosen
                print(Secondary_display_quantity)
                return Response({
                    'status': 200,
                    'message': "Quantification Data",
                    "no_of_boards": formula,
                    "primary_display_quantity": primary_display_quantity,
                    "Secondary_display_quantity": Secondary_display_quantity
                })
        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })


class locationdetector(APIView):
    def post(self, request):
        try:
            serializer = locationdetectorserializer(data=request.data)
            if serializer.is_valid():
                Latitude = serializer.data["Latitude"]
                Longitude = serializer.data["Longitude"]
                print(Latitude, Longitude)
                geolocator = Nominatim(user_agent="geoapiExercises")
                location = geolocator.reverse(Latitude + "," + Longitude)
                print(location)
                address = location.raw['address']
                print(address)

            return Response({
                'status': 200,
                'message': "Location Details",
                "location": str(location),
                "address": str(address)

            })
        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': str(e)
            })


class professionalSignup(APIView):
    def post(self, request):
        serializer = professionalSignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            mobile = serializer.data['mobile']
            password = serializer.data['password']
            c_password = serializer.data['c_password']
            professionalUsername = 'prodymeF' + ''.join(
                random.choices(string.digits + string.ascii_letters, k=random.randint(10, 14)))

            if mobile == '' and email == '':
                return JsonResponse({
                    "status": 400,
                    "message": "Please Enter Either E-mail or Phone Number",
                })
            if email != '':
                if professional.objects.filter(email=email).exists():
                    return JsonResponse({
                        "status": 400,
                        "message": "User Already Exist With Provided Email-ID",
                    })
            if mobile != '':
                if professional.objects.filter(mobile=mobile).exists():
                    return JsonResponse({
                        "status": 400,
                        "message": "User Already Exist With Provided Mobile",
                    })

            if len(mobile) not in (0, 10):
                return JsonResponse({
                    "status": 400,
                    "message": "Incorrect Phone Number Length",
                })
            if password != c_password:
                return JsonResponse({
                    "status": 400,
                    "message": "Passwords Don't Match",
                })
            professional.objects.create(
                **serializer.data
            )

            User.objects.create_user(username=professionalUsername, password=password)
            return JsonResponse({
                'status': 200,
                'message': 'Professional User Created Successfully',
                'is_verified_email': serializer.data['is_verified_email'],
                'is_verified_mobile': serializer.data['is_verified_email']
            })

        return JsonResponse({
            'status': 400,
            'message': 'Something Went Wrong',
            'error': serializer.errors
        })


class bookAServiceRequest(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = bookAServiceSerializer(data=request.data)
        if serializer.is_valid():
            requestType = serializer.data['requestType']
            requestDescription = serializer.data['requestDescription']
            serviceid = 'service' + ''.join(
                random.choices(string.digits + string.ascii_letters, k=random.randint(10, 14)))

            bookAService.objects.create(
                username_id=request.user,
                serviceid=serviceid,
                requestType=requestType,
                requestDescription=requestDescription,
                status="0"

            )

            notification.objects.create(
                notification_id=serviceid,
                notificationfrom=request.user
            )

            return JsonResponse({
                'status': 200,
                'message': 'Thanks for booking the Service',
            })

        return JsonResponse({
            'status': 400,
            'message': 'Something Went Wrong',
            'error': serializer.errors
        })


class optAServiceRequest(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = optAServiceSerializer(data=request.data)
        if serializer.is_valid():
            serviceid = serializer.data['serviceid']
            workid = 'workid' + ''.join(
                random.choices(string.digits + string.ascii_letters, k=random.randint(10, 14)))

            workChart.objects.create(
                professionalUsername_id=request.user,
                serviceid_id=serviceid,
                workid=workid,
            )
            data = notification.objects.filter(notification_id=serviceid).values()[0]
            print(data['notificationfrom'])
            notification.objects.create(
                notification_id=workid,
                notificationfrom=request.user,
                notificationto=data['notificationfrom']
            )

            return JsonResponse({
                'status': 200,
                'message': 'Booking Assigned to Profession',
            })

        return JsonResponse({
            'status': 400,
            'message': 'Something Went Wrong',
            'error': serializer.errors
        })


class UpdatePassword(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            password = serializer.data["password"]
            prodymeUser.objects.filter(
                username=request.user).update(password=password)

            profile.objects.filter(profile_id=user).update(
                password=password
            )
            User.objects.filter(username=user).update(
                password=make_password(password))

            return JsonResponse({
                'status': 200,
                'message': 'Password Updated Successfully',
            })
        return JsonResponse({
            'status': 400,
            'message': 'Something Went Wrong',
            'error': serializer.errors
        })


class PostcommunicationPreference(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = communicationPreferenceSerializer(data=request.data)
        if serializer.is_valid():
            communication_preference = serializer.data["communication_preference"]
            data2 = list(prodymeUser.objects.filter(username=request.user).values())[0]
            print(data2["email"])
            CommunicationPreference.objects.filter(
                username=data2["email"]).update(communication_preference=communication_preference)

            return JsonResponse({
                'status': 200,
                'message': 'Communication Preference Updated Successfully',
            })
        return JsonResponse({
            'status': 400,
            'message': 'Something Went Wrong',
            'error': serializer.errors
        })


class getCommunicationPreference(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data2 = list(prodymeUser.objects.filter(username=request.user).values())[0]
            print(data2["email"])
            data = list(CommunicationPreference.objects.filter(username_id=data2["email"]).values())
            print(data)

            return JsonResponse({
                'status': 200,
                'message': 'Communication Preference',
                "values": data
            })
        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong'
            })


###part4


class getsubCategory(APIView):
    def get(self, request, category_name, ):
        try:
            data1 = list(subCategory.objects.filter(category_name_id=category_name, ).values())
            print(data1)

            for var in data1:
                del var["category_name_id"]

            return Response({
                'status': 200,
                'data': data1
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })


class getCategorys(APIView):
    def get(self, request, ):
        try:
            data = list(Category.objects.filter().values())
            result = ["ALL"]
            for i in data:
                result.append(list(i.values())[0])
            return Response({
                'status': 200,
                'data': result
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })


class getSubSubCategory(APIView):
    def get(self, request, category_name, subCategory_name):
        try:
            data2 = list(subSubCategory.objects.filter(category_name_id=category_name,
                                                       subCategory_name_id=subCategory_name).values())
            print(data2)

            for var in data2:
                del var["category_name_id"]
                del var["subCategory_name_id"]

            return Response({
                'status': 200,
                'data': data2
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })


class getProduct(APIView):
    def get(self, request, category_name, subCategory_name, item_type):
        try:
            productData = list(
                Product.objects.filter(category_name_id=category_name, subCategory_name_id=subCategory_name,
                                       item_type_id=item_type).values())
            print(productData)

            for var in productData:
                del var["category_name_id"]
                del var["subCategory_name_id"]
                del var["item_type_id"]

            return Response({
                'status': 200,
                'data': productData
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })


class uploadItemData(APIView):
    def get(self, request, fileName):
        try:
            filePath = Path().absolute()
            if fileName == "category":
                fullFileName = str(filePath) + "/" + "user/" + fileName + ".csv"
                print(fullFileName)
                df = pd.read_csv(fullFileName, encoding='ISO-8859-1')
                index_data = list(df.index)
                print(index_data)
                for var in index_data:
                    x = dict(df.iloc[var])
                    print(type(x), x)
                    Category.objects.create(
                        category_name=x["category_name"]
                    )
                return JsonResponse({
                    'status': 200,
                    'message': 'Category Data Inserted Successfully',

                })

            elif fileName == "subcategory":
                fullFileName = str(filePath) + "/" + "user/" + fileName + ".csv"
                print(fullFileName)
                df = pd.read_csv(fullFileName, encoding='ISO-8859-1')
                index_data = list(df.index)
                print(index_data)
                for var in index_data:
                    x = dict(df.iloc[var])
                    print(type(x), x)
                    subCategory.objects.create(
                        category_name_id=x["category_name"],
                        subCategory_name=x["subCategory_name"]
                    )
                return JsonResponse({
                    'status': 200,
                    'message': 'SubCategory Data Inserted Successfully',

                })
            elif fileName == "product":
                fullFileName = str(filePath) + "/" + "user/" + fileName + ".csv"
                print(fullFileName)
                df = pd.read_csv(fullFileName, encoding='ISO-8859-1')
                index_data = list(df.index)
                print(index_data)
                for var in index_data:
                    x = dict(df.iloc[var])
                    print(type(x), x)
                    Product.objects.create(
                        category_name_id=x["category_name"],
                        subCategory_name_id=x["subCategory_name"],
                        item_type_id= x["item_type"],
                        product_id=x["product_id"],
                        productName=x["productName"],
                        brandName=x["brandName"],
                        price=x["price"]
                    )
                return JsonResponse({
                    'status': 200,
                    'message': 'SubCategory Data Inserted Successfully',

                })
            elif fileName == "productRating":
                fullFileName = str(filePath) + "/" + "user/" + fileName + ".csv"
                print(fullFileName)
                df = pd.read_csv(fullFileName, encoding='ISO-8859-1')
                index_data = list(df.index)
                print(index_data)
                for var in index_data:
                    x = dict(df.iloc[var])
                    print(type(x), x)
                    productRateing.objects.create(
                        product_id_id=x["product_id"],
                        productRating=x["productRating"]
                    )
                return JsonResponse({
                    'status': 200,
                    'message': 'SubCategory Data Inserted Successfully',

                })
            elif fileName == "productsale":
                fullFileName = str(filePath) + "/" + "user/" + fileName + ".csv"
                print(fullFileName)
                df = pd.read_csv(fullFileName, encoding='ISO-8859-1')
                index_data = list(df.index)
                print(index_data)
                for var in index_data:
                    x = dict(df.iloc[var])
                    print(type(x), x)
                    productSale.objects.create(
                        product_id_id=x["product_id"],
                        productSaleCount=x["productSaleCount"]
                    )
                return JsonResponse({
                    'status': 200,
                    'message': 'SubCategory Data Inserted Successfully',

                })
            elif fileName == "subSubcategory":
                fullFileName = str(filePath) + "/" + "user/" + fileName + ".csv"
                print(fullFileName)
                df = pd.read_csv(fullFileName, encoding='ISO-8859-1')
                index_data = list(df.index)
                print(index_data)
                for var in index_data:
                    x = dict(df.iloc[var])
                    print(type(x), x)
                    subSubCategory.objects.create(
                        category_name_id=x["category_name"],
                        subCategory_name_id=x["subCategory_name"],
                        item_type=x["item_type"]
                    )
                return JsonResponse({
                    'status': 200,
                    'message': 'SubCategory Data Inserted Successfully',

                })
            elif fileName == "productData":
                fullFileName = str(filePath) + "/" + "user/" + fileName + ".csv"
                print(fullFileName)
                df = pd.read_csv(fullFileName, encoding='ISO-8859-1')
                index_data = list(df.index)
                print(index_data)
                for var in index_data:
                    x = dict(df.iloc[var])
                    print(type(x), x)
                    productDetail.objects.create(

                        product_id_id=x["product_id"],
                        productFeature=x["productFeature"],

                    )
                return JsonResponse({
                    'status': 200,
                    'message': 'Product Data Successfully',
                })
        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })


class getProductDetail(APIView):
    def get(self, request, product_id):
        try:
            data3 = list(Product.objects.filter(product_id=product_id).values())
            # print(data3)
            productData = list(productDetail.objects.filter(product_id_id=product_id).values())
            # print(productData)
            for var in productData:
                data3.append(var)
                print(data3)

            return JsonResponse({
                'status': 200,
                'data': data3

            })
        except Exception as e:
            # print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })


class getproductall(APIView):
    def get(self, request, category_name):
        try:
            data3 = list(Product.objects.filter(category_name_id=category_name).values())
            # print(data3)
            for var in data3:
                del var["item_type_id"]
                del var["subCategory_name_id"]
            return Response({
                'status': 200,
                'data': data3
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })


# class getProductRaleted(APIView):
#     def get(self, request, productName):
#         try:
#             data3 = list(Product.objects.filter(productName=productName).values())
#             print(data3)
#             for var in data3:
#                 del var["product_id"]
#                 del var["productName"]
#                 del var["brandName"]
#                 del var["price"]
#             return Response({
#                 'status': 200,
#                 'data': data3
#             })
#
#         except Exception as e:
#             return Response({
#                 'status': 400,
#                 'message': 'Something went wrong',
#                 'errors': str(e)
#             })


class getProductsimilar(APIView):
    def get(self, request, product_id):
        try:
            similar = Product.objects.filter(product_id=product_id).values()
            print(similar)
            for var in similar:
                x = var["category_name_id"]
                y = var["subCategory_name_id"]
                z = var["item_type_id"]
            secoundProduct = Product.objects.filter(category_name_id=x, subCategory_name_id=y, item_type_id=z).values()

            return Response({
                'status': 200,
                'data': secoundProduct
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })


class getProductRecommended(APIView):
    def get(self, request, product_id):
        try:
            similar = Product.objects.filter(product_id=product_id).values()
            for var in similar:
                x = var["category_name_id"]
            secoundProduct = Product.objects.filter(category_name_id=x).values()
            # for var in secoundProduct:
            #     del var["subCategory_name_id"]
            #     del var["item_type_id"]

            return Response({
                'status': 200,
                'data': secoundProduct
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })


class getProductRating(APIView):
    def get(self, request, productRating):
        try:
            data3 = list(productRateing.objects.filter(productRating=productRating).values())
            print(data3)
            return Response({
                'status': 200,
                'data': data3
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })


class getProductSeller(APIView):
    def get(self, request,productSaleCount):
        try:
            data = productSale.objects.filter().values()
            print(data)
            result = []
            for i in data:
                if i["productSaleCount"] >= int(productSaleCount):
                    result.append(i)

            return Response({
                'status': 200,
                'data': result
            })

        except Exception as e:
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'errors': str(e)
            })

class searchFilter(APIView):
    def get(self, request, productName,categorName):
        try:
            if categorName== "ALL":
                data = list(Product.objects.filter(productName__icontains=productName).values())
                return JsonResponse({
                    'status': 200,
                    'data': data,
                })

            else:
                data = list(Product.objects.filter(productName__icontains=productName,category_name_id=categorName).values())
                return JsonResponse({
                    'status': 200,
                    'data': data,
                })


        except Exception as e:
            print(str(e))
            return JsonResponse({
                'status': 400,
                'message': 'Something Went Wrong',
                'error': str(e)
            })