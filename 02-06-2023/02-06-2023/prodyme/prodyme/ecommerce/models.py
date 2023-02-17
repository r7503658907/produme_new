from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100,primary_key=True)

    def __str__(self):
        return self.category_name

class Item_Category(models.Model):
    category_name = models.ManyToManyField(Category)
    item_category_name = models.CharField(max_length=100,primary_key=True)

    def __str__(self):
        return self.item_category_name

class Item_Type(models.Model):
    item_category_name = models.ManyToManyField(Item_Category)
    item_type = models.CharField(max_length=100,primary_key=True)

    def __str__(self):
        return self.item_type