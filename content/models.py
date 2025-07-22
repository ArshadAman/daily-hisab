from django.db import models


class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Tutorial(models.Model):
    title = models.CharField(max_length=100)
    video_url = models.URLField()
    language = models.CharField(max_length=5, choices=[('en', 'English'), ('hi', 'Hindi'), ('mr', 'Marathi')])
    created_at = models.DateTimeField(auto_now_add=True)
