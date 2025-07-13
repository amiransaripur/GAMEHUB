from django.db import models
from django.utils.text import slugify
from PIL import Image

class Game(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    genre = models.CharField(max_length=150)
    platform = models.CharField(max_length=150)
    description = models.TextField()
    release_date = models.DateField(null=True)
    trailer_url = models.URLField(max_length=200, blank=True, null=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.cover_image:
            img = Image.open(self.cover_image.path)

            max_width = 800
            if img.width > max_width:
                new_height = int((max_width / img.width) * img.height)
                img = img.resize((max_width, new_height), Image.LANCZOS)
                img.save(self.cover_image.path, quality=90)
                
    def __str__(self):
        return self.title
    
class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE,related_name='reviews')
    user_name = models.CharField(max_length=50)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.rating}/5"