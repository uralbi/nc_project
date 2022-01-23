from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from PIL import Image


def image_process(photo_path):
    imag = Image.open(photo_path)
    width, height = imag.size
    ratio = height / width
    if ratio > 1.3 and width < 1000:
        cr_size = (height - width) / 2.5
        cropped = imag.crop((0, cr_size, width, height - cr_size))
        cropped.save(photo_path, "JPEG")
    elif ratio > 1.15 and width > 1000 or height > 900:
        cr_size = (height - width) / 2.5
        cropped = imag.crop((0, cr_size, width, height - cr_size))
        wid, hei = cropped.size
        rat = hei / wid
        output_size = (900, 900 * rat)
        cropped.thumbnail(output_size)
        cropped.save(photo_path, "JPEG")
    elif width > 1000 or height > 900:
        output_size = (900, 900 * ratio)
        imag.thumbnail(output_size)
        imag.save(photo_path, format='png')


class Products(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    city = models.CharField(max_length=50, verbose_name='City', default='Los Angeles')
    product = models.CharField(max_length=100, unique=True,  verbose_name='Product')
    price = models.IntegerField(verbose_name='Price')
    description = models.TextField(blank=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    photo1 = models.ImageField(upload_to='item_pics/%Y/%m/%d', verbose_name='Pic 1', blank=True)
    photo2 = models.ImageField(upload_to='item_pics/%Y/%m/%d', verbose_name='Pic 2', blank=True)
    photo3 = models.ImageField(upload_to='item_pics/%Y/%m/%d', verbose_name='Pic 3', blank=True)
    photo4 = models.ImageField(upload_to='item_pics/%Y/%m/%d', verbose_name='Pic 4', blank=True)
    main_category = models.ForeignKey('MainCategory', default='1', on_delete=models.PROTECT, verbose_name='Main Category')
    sub_category = models.ForeignKey('SubCategory', default='21', on_delete=models.PROTECT, verbose_name='Sub Categogry')
    views = models.IntegerField(default=0)

    def get_absolute_url(self): #redirect to this news item !
        return reverse('view_product', kwargs={"pk": self.pk})

        #передаем название маршрута и ключ. реверс для пайтон фалов.

    def __str__(self):
        return self.product

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo1:
            image_process(self.photo1.path)
        if self.photo2:
            image_process(self.photo2.path)
        if self.photo3:
            image_process(self.photo3.path)
        if self.photo4:
            image_process(self.photo4.path)

    def delete(self, *args, **kwargs):
        if self.photo1:
            self.photo1.delete()
        if self.photo2:
            self.photo2.delete()
        if self.photo3:
            self.photo3.delete()
        if self.photo4:
            self.photo4.delete()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']


class MainCategory(models.Model):
    main_category = models.CharField(max_length=100, db_index=True)
    parent_category = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('main_category', kwargs={"main_category_id": self.pk})

    def __str__(self):
        return self.main_category

    class Meta:
        verbose_name = 'Main_Category'
        verbose_name_plural = 'Main_Categories'
        ordering = ['main_category']


class SubCategory(models.Model):
    sub_category = models.CharField(max_length=100, db_index=True)

    def get_absolute_url(self):
        return reverse('sub_category', kwargs={"sub_category_id": self.pk})

    def __str__(self):
        return self.sub_category

    class Meta:
        verbose_name = 'Sub-Category'
        verbose_name_plural = 'Sub-Categories'
        ordering = ['sub_category']