from .models import *
from .forms import *
from .serializers import ManhwaSerializer, ChapterSerializer
from .utils import convert_pdf_to_images
from django.core.management import call_command
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
import logging

logger = logging.getLogger(__name__)

def create_superuser_view(request):
    try:
        call_command('createsuperuser', interactive=False, username='admin', email='admin@example.com', password='yourpassword')
        return HttpResponse("Superuser created successfully!")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    

# User UserProfile view
def user_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    logger.debug(f"User: {user.username}")

    # Ensure the Profile exists, and create it if necessary
    profile, created = UserProfile.objects.get_or_create(user=user)
    logger.debug(f"Profile: {profile} Created: {created}")

    # Fetch the user's favorite manhwas (or any other details you want to show)
    favorites = user.manhwa_favorites.all()  # Using the `related_name` in the Manhwa model
    logger.debug(f"Favorites: {favorites}")

    return render(request, 'manhwa_reader/profile.html', {
        'user': user,
        'profile': profile,
        'favorites': favorites,
    })


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  # Redirect to the profile page
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'manhwa_reader/user_profile.html', {
        'profile': profile,
        'form': form,
    })
# Edit or view the logged-in user's profile
@login_required
def user_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  # Redirect to the profile page
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'manhwa_reader/user_profile.html', {
        'profile': profile,
        'form': form,
    })

# Toggle favorite for a specific Manhwa
@login_required
def toggle_favorite(request, manhwa_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'unauthenticated'}, status=403)

    # Fetch the Manhwa object
    manhwa = get_object_or_404(Manhwa, id=manhwa_id)
    
    # Check if the manhwa is already in the user's favorites
    user_profile = request.user.userprofile  # Assuming `userprofile` is a one-to-one relationship
    if manhwa in user_profile.favorites.all():
        user_profile.favorites.remove(manhwa)  # Remove from favorites
        return JsonResponse({'status': 'removed'})
    else:
        user_profile.favorites.add(manhwa)  # Add to favorites
        return JsonResponse({'status': 'added'})



# List favorite Manhwas for the logged-in user
@login_required
def favorite_manhwas(request):
    # Fetch the favorite manhwas directly using `favorited_by`
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    manhwas = user_profile.favorites.all()  # Get all the manhwas the user has favorited

    return render(request, 'manhwa_reader/favorites.html', {'manhwas': manhwas})


# Remove a specific Manhwa from favorites
@login_required
def remove_favorite(request, manhwa_id):
    manhwa = get_object_or_404(Manhwa, id=manhwa_id)
    
    # Ensure the UserProfile exists for the logged-in user
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Remove the manhwa from favorites if it exists
    if manhwa in user_profile.favorites.all():
        user_profile.favorites.remove(manhwa)
    
    return redirect('favorites')

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('manhwa_list')
    else:
        form = UserCreationForm()
    return render(request, 'manhwa_reader/register.html', {'form': form})

# User login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('manhwa_list')
    else:
        form = AuthenticationForm()
    return render(request, 'manhwa_reader/login.html', {'form': form})

# User logout view
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('manhwa_list')

# List all genres
def genre_list(request):
    genres = Genre.objects.all()  # Retrieve all genres from the database
    return render(request, 'manhwa_reader/genre_list.html', {'genres': genres})

# Genre details and associated Manhwas
def genre_detail(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    manhwas = genre.manhwas.all()
    return render(request, 'manhwa_reader/genre_detail.html', {'genre': genre, 'manhwas': manhwas})

# Upload a chapter for a specific Manhwa
@login_required
def upload_chapter(request, manhwa_id):
    manhwa = get_object_or_404(Manhwa, id=manhwa_id)

    if request.method == 'POST':
        form = ChapterForm(request.POST, request.FILES)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.manhwa = manhwa
            chapter.user = request.user  # Assign the logged-in user to the chapter
            chapter.save()

            # Convert the uploaded PDF to images (optional)
            if chapter.pdf_file:  # Ensure the PDF file exists
                pdf_path = chapter.pdf_file.path  # File path of the uploaded PDF
                image_paths = convert_pdf_to_images(pdf_path, chapter)  # Pass chapter as an argument

                # Save each image path to the database
                save_images(chapter, image_paths)

            return redirect('manhwa_detail', manhwa_id=manhwa_id)
    else:
        form = ChapterForm()

    return render(request, 'manhwa_reader/upload_chapter.html', {
        'form': form,
        'manhwa': manhwa
    })

# List all Manhwas
def manhwa_list(request):
    query = request.GET.get('query')
    if query:
        manhwas = Manhwa.objects.filter(title__icontains=query)
    else:
        manhwas = Manhwa.objects.all()
    
    paginator = Paginator(manhwas, 10)  # Paginate with 10 manhwas per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'manhwa_reader/manhwa_list.html', {
        'manhwas': page_obj,  # Paginated objects
        'page': 'home'
    })

# Favorite manhwas view (user profile favorites)
@login_required
def favorite_manhwas(request):
    # Access the user profile directly
    user_profile = request.user.userprofile
    manhwas = user_profile.favorites.all()  # Fetch the favorite manhwas using the related_name

    return render(request, 'manhwa_reader/favorites.html', {'manhwas': manhwas})

# Detail view for a specific Manhwa
def manhwa_detail(request, manhwa_id):
    # Fetch the Manhwa object
    manhwa = get_object_or_404(Manhwa, id=manhwa_id)
    
    # Check if the user is logged in and if the Manhwa is in their favorites
    is_favorite = False
    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile  # Access the user's profile
            is_favorite = manhwa in user_profile.favorites.all()
        except AttributeError:
            is_favorite = False

    # Get all related chapters
    chapters = manhwa.chapters.all()  # Assuming a related_name 'chapters' on a ForeignKey or ManyToManyField

    # Fetch all genres related to the Manhwa (if applicable)
    genres = manhwa.genres.all()  # Assuming genres is a ManyToManyField in the Manhwa model

    return render(request, 'manhwa_reader/manhwa_detail.html', {
        'manhwa': manhwa,
        'is_favorite': is_favorite,
        'chapters': chapters,
        'genres': genres,  # Pass genres to the template
    })

# Detail view for a specific Chapter

def chapter_detail(request, manhwa_id, chapter_id):
    try:
        # Get the manhwa object
        manhwa = get_object_or_404(Manhwa, id=manhwa_id)
        
        # Get the current chapter object
        chapter = get_object_or_404(Chapter, id=chapter_id, manhwa=manhwa)
        
        # Retrieve images associated with this chapter
        images = chapter.images.all()
        
        # Get the previous chapter
        previous_chapter = Chapter.objects.filter(manhwa=manhwa, id__lt=chapter.id).order_by('-id').first()
        
        # Get the next chapter
        next_chapter = Chapter.objects.filter(manhwa=manhwa, id__gt=chapter.id).order_by('id').first()
        
        # Pass the context to the template
        return render(request, 'manhwa_reader/chapter_detail.html', {
            'manhwa': manhwa,
            'images': images,
            'chapter': chapter,
            'previous_chapter': previous_chapter,
            'next_chapter': next_chapter
        })
    
    except Exception as e:
        # You can log the error or return a custom error page if necessary
        print(f"Error: {e}")
        # Returning a 404 page or a custom error page
        return render(request, 'manhwa_reader/error.html', {'error_message': str(e)})


def love(request):
    return render(request, "manhwa_reader/her.html")

def love2(request):
    return render(request, "manhwa_reader/readmore.html")

# API Viewsets for Manhwa and Chapter
class ManhwaViewSet(viewsets.ModelViewSet):
    queryset = Manhwa.objects.all()
    serializer_class = ManhwaSerializer

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

# Function to save images related to a chapter
@login_required
def save_images(chapter, image_paths):
    for image_path in image_paths:
        Image.objects.create(chapter=chapter, image=image_path)
