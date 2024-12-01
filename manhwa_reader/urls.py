# manhwa_reader/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register(r'manhwas', ManhwaViewSet)
router.register(r'chapters', ChapterViewSet)

urlpatterns = [
    # List of Manhwas
    path('', views.manhwa_list, name='manhwa_list'),
    
    # Manhwa detail page
    path('manhwa/<int:manhwa_id>/', views.manhwa_detail, name='manhwa_detail'),
    
    # Chapter detail page with both manhwa_id and chapter_id
    path('manhwa/<int:manhwa_id>/chapter/<int:chapter_id>/', views.chapter_detail, name='chapter_detail'),
    
    # Upload chapter for a Manhwa
    path('manhwa/<int:manhwa_id>/upload_chapter/', views.upload_chapter, name='upload_chapter'),
    
    # List of genres
    path('genres/', views.genre_list, name='genre_list'),
    
    # Genre detail page
    path('genres/<int:genre_id>/', views.genre_detail, name='genre_detail'),
    
    # User registration, login, logout
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # User favorites
    path('favorites/', views.favorite_manhwas, name='favorites'),
    path('remove_favorite/<int:manhwa_id>/', views.remove_favorite, name='remove_favorite'),
    path('toggle_favorite/<int:manhwa_id>/', views.toggle_favorite, name='toggle_favorite'),
    
    # User profile
    path("profile/<str:username>/", views.user_profile_view, name="profile_view"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]


# Add this to serve media files during development (only in DEBUG mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
