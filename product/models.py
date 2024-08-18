from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Наименование категории",
        help_text="Введите наименование категории товара",
    )
    description = models.TextField(
        max_length=1000,
        verbose_name="Описание продукта",
        help_text="Введите описание продукта",
    )
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Наименование продукта",
        help_text="Введите наименование продукта",
    )
    description = models.TextField(
        max_length=1000,
        verbose_name="Описание продукта",
        help_text="Введите описание продукта",
    )
    image = models.ImageField(
        upload_to="photo/product",
        blank=True,
        null=True,
        verbose_name="Фото продукта",
        help_text="Загрузите фото",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        help_text="Введите категорию товара",
    )
    price = models.PositiveIntegerField(
        verbose_name="Цена за покупку", help_text="Введите цену продукта"
    )
    created_at = models.DateTimeField(verbose_name="Дата создания(записи в БД)")
    updated_at = models.DateTimeField(
        verbose_name="Дата последнего изменения(записи в БД)"
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество просмотров",
        help_text="Укажите количество просмотров",
    )
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Пользователь", blank=True, null=True)
    
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
    
    def __str__(self):
        return self.name


class Version(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="product_versions",
        on_delete=models.CASCADE,
        verbose_name="Продукт",
        help_text="Введите продукт",
    )
    version_number = models.PositiveIntegerField(
        default=0,
        verbose_name="Номер версии",
        help_text="Введите номер версии продукта"
    )
    version_name = models.CharField(
        max_length=200,
        verbose_name="Название версии",
        help_text="Введите название версии продукта",
    )
    current_version_indicator = models.BooleanField(
        verbose_name="Текущая версия",
        help_text="Укажите, является ли текущая версия",
        default=False,
    )
    
    class Meta:
        verbose_name = "Версия продукта"
        verbose_name_plural = "Версии продуктов"
    
    def __str__(self):
        return f'{self.product}, {self.version_number}, {self.version_name}, {self.current_version_indicator}'
    