from django.db import models
from django.utils.text import slugify


class CarBrand(models.Model):
    """e.g. Toyota, Honda, Suzuki"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """e.g. Civic, Corolla, Cultus — belongs to a brand"""
    brand = models.ForeignKey(
        CarBrand,
        on_delete=models.PROTECT,
        related_name='models'
    )
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        # Same model name can exist under different brands,
        # but not twice under the same brand
        unique_together = [['brand', 'name']]

    def __str__(self):
        return f"{self.brand.name} {self.name}"
