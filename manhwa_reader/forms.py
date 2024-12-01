from django import forms
from .models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "avatar"]

    # Add any custom validation if needed

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'chapter_number', 'pdf_file']  # Include fields as required
