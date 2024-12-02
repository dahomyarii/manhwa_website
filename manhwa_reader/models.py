from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Manhwa(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='cover_images/')
    genres = models.ManyToManyField(Genre, related_name='manhwas', blank=True)
    favorited_by = models.ManyToManyField(User, related_name='manhwa_favorites', blank=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    title = models.CharField(max_length=200)
    chapter_number = models.IntegerField()
    manhwa = models.ForeignKey(Manhwa, on_delete=models.CASCADE, related_name='chapters')
    pdf_file = models.FileField(upload_to='chapters/%Y/%m/%d/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chapters')  # Added user field

    def __str__(self):
        return f"Chapter {self.title} of {self.manhwa.title}"

class ChapterPage(models.Model):
    image = models.ImageField(upload_to='chapter_images/')

    def __str__(self):
        return f"Page {self.id}"

class ChapterImage(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='chapter_images')  # Unique related_name
    image = models.ImageField(upload_to='manhwa_images/')

class Image(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='images', on_delete=models.CASCADE)  # Unique related_name
    image = models.ImageField(upload_to='chapter_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.chapter.title}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manhwa = models.ForeignKey(Manhwa, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'manhwa')

    def __str__(self):
        return f'{self.user.username} - {self.manhwa.title}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    favorites = models.ManyToManyField('Manhwa', blank=True, related_name='is_favorited') 
    bio = models.TextField(blank=True, null=True)  # Optional bio
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.jpg")
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-generate a slug if not set
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class ReadingProgress(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    manhwa = models.ForeignKey('manhwa_reader.Manhwa', on_delete=models.CASCADE)
    last_read_chapter = models.ForeignKey('manhwa_reader.Chapter', on_delete=models.SET_NULL, null=True, blank=True)
    progress_percentage = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.user_profile.user.username} - {self.manhwa.title} Progress'

# Signal to auto-create UserProfile when a new User is created