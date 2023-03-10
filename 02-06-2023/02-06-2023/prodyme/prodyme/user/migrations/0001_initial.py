# Generated by Django 4.0.2 on 2023-02-06 08:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='bookAService',
            fields=[
                ('serviceid', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('requestType', models.CharField(max_length=100)),
                ('requestDescription', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=1)),
                ('professionalUsername', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='GetInTouchModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('existing_order_number', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('description', models.CharField(max_length=10000)),
                ('upload_attachments', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('product_type', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('brand', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('status_ticket', models.CharField(choices=[('InProgress', 'InProgress'), ('Closed', 'Closed')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='notification',
            fields=[
                ('notification_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('notificationfrom', models.CharField(max_length=100)),
                ('notificationto', models.CharField(default='group', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PartitionBasketDetails',
            fields=[
                ('partition_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('clear_height', models.CharField(max_length=100)),
                ('height1', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('height2', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('height3', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('height4', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('height5', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('height6', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('height7', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('height8', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('height9', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('height10', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('height11', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('height12', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('productName', models.CharField(max_length=100)),
                ('brandName', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('category_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.category')),
            ],
        ),
        migrations.CreateModel(
            name='prodymeUser',
            fields=[
                ('username', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
                ('is_verified_email', models.BooleanField(default=False)),
                ('is_verified_mobile', models.BooleanField(default=False)),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='professional',
            fields=[
                ('professionalUsername', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('email', models.CharField(default='', max_length=100, null=True)),
                ('mobile', models.CharField(default='', max_length=100, null=True)),
                ('password', models.CharField(max_length=100)),
                ('c_password', models.CharField(max_length=100)),
                ('professional_type', models.CharField(max_length=100)),
                ('expert_areas', models.TextField(blank=True, null=True)),
                ('assign_work_status', models.TextField(blank=True, null=True)),
                ('is_verified_email', models.BooleanField(default=False)),
                ('is_verified_mobile', models.BooleanField(default=False)),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SmartBuilder',
            fields=[
                ('type_of_kitchen', models.CharField(choices=[('L', 'L'), ('U', 'U'), ('Parallel', 'Parallel'), ('G', 'G'), ('O', 'O')], max_length=100, primary_key=True, serialize=False)),
                ('nomenclature', models.CharField(max_length=1)),
                ('no_of_len', models.CharField(max_length=1)),
                ('no_of_corners', models.CharField(max_length=1)),
                ('corner_placed_on_side', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='smartBuilderPartitionCalculator',
            fields=[
                ('partitionaliascalculator', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('length_data_condition_check1', models.CharField(default='', max_length=100, null=True)),
                ('length_data_condition_check2', models.CharField(default='', max_length=100, null=True)),
                ('length_data_condition_check3', models.CharField(default='', max_length=100, null=True)),
                ('length_data_condition_check4', models.CharField(default='', max_length=100, null=True)),
                ('partition_value1', models.CharField(max_length=100)),
                ('partition_value2', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='subCategory',
            fields=[
                ('subCategory_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('category_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.category')),
            ],
        ),
        migrations.CreateModel(
            name='workChart',
            fields=[
                ('workid', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(default=datetime.datetime(2023, 2, 6, 13, 55, 1, 973823))),
                ('status', models.CharField(default='In Progress', max_length=100)),
                ('professionalUsername', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.professional')),
                ('serviceid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.bookaservice')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('product_list', models.TextField()),
                ('wishlist_ID', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=1)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.prodymeuser')),
            ],
        ),
        migrations.CreateModel(
            name='subSubCategory',
            fields=[
                ('item_type', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('category_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.category')),
                ('subCategory_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='SmartBuilderDesign',
            fields=[
                ('design_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('length_name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('balance_after_sink', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('corner_on_which_side', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('balance_after_corner', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('no_of_columns', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.prodymeuser')),
            ],
        ),
        migrations.CreateModel(
            name='SavedCart',
            fields=[
                ('product_list', models.TextField()),
                ('SavedCart_ID', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=1)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.prodymeuser')),
            ],
        ),
        migrations.CreateModel(
            name='profile_address',
            fields=[
                ('address_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('address_type', models.CharField(choices=[('HOME', 'HOME'), ('OFFICE', 'OFFICE'), ('OTHER', 'OTHER')], default='HOME', max_length=10)),
                ('address_nickname', models.CharField(default='', max_length=100, null=True)),
                ('address', models.CharField(default='', max_length=100, null=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.prodymeuser')),
            ],
        ),
        migrations.CreateModel(
            name='profile',
            fields=[
                ('profile_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('business_name', models.CharField(default='', max_length=100)),
                ('gst', models.CharField(default='', max_length=100)),
                ('email', models.CharField(default='', max_length=100, null=True)),
                ('mobile', models.CharField(default='', max_length=100, null=True)),
                ('password', models.CharField(default='', max_length=100, null=True)),
                ('zipcode', models.CharField(default='', max_length=100, null=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.prodymeuser')),
            ],
        ),
        migrations.CreateModel(
            name='productSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productSaleCount', models.IntegerField()),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.product')),
            ],
        ),
        migrations.CreateModel(
            name='productRateing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productRating', models.FloatField()),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.product')),
            ],
        ),
        migrations.CreateModel(
            name='productDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productFeature', models.TextField()),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='item_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.subsubcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='subCategory_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.subcategory'),
        ),
        migrations.CreateModel(
            name='Loyalty',
            fields=[
                ('order_amount', models.IntegerField()),
                ('loyaltyPoints', models.FloatField()),
                ('loyalty_ID', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.prodymeuser')),
            ],
        ),
        migrations.CreateModel(
            name='CommunicationPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('communication_preference', models.CharField(default='False', max_length=100)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.prodymeuser')),
            ],
        ),
        migrations.CreateModel(
            name='boqAudit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=200)),
                ('datetime', models.DateTimeField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.prodymeuser')),
            ],
        ),
        migrations.AddField(
            model_name='bookaservice',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.prodymeuser'),
        ),
    ]
