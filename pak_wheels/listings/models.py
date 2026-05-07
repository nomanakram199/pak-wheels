from django.db import models
from django.conf import settings

# Create your models here.
class CarListing(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    city = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'
        ordering = ['-created']

    def __str__(self):
        return f"{self.year} {self.brand} {self.model}"
    
 

class CarImage(models.Model):
    """Images attached to a listing."""
    listing = models.ForeignKey(
        CarListing,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='listings/')
    is_primary = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.listing.title}"

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Set all other images for this listing to NOT primary
            CarImage.objects.filter(listing=self.listing).update(is_primary=False)
        super().save(*args, **kwargs)