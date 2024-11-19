from django.db import models
from django.urls import reverse

from ckeditor.fields import RichTextField
from services.utils import unique_slugify


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория')
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='Тег')
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    content = RichTextField(verbose_name="Описание")
    excerpt = models.TextField(verbose_name='Отрывок', blank=True)
    featured_image = models.ImageField(blank=True, default="default.jpg", upload_to="images/")
    slug = models.SlugField(unique=True, blank=True)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.excerpt:
            self.excerpt = self.content[:100]
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.name}"
