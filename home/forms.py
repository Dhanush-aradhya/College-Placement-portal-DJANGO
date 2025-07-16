# home/forms.py
from django import forms
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from .models import StudentProfile, Domain, Language

class StudentProfileForm(forms.ModelForm):
    domains = forms.ModelMultipleChoiceField(
        queryset=Domain.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2-target', 'style': 'width: 100%;'}),
        required=True,
        help_text="Select up to 4 domains of interest."
    )
    languages_known = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2-target', 'style': 'width: 100%;'}),
        required=False,
        help_text="Select languages you know (optional)."
    )

    class Meta:
        model = StudentProfile
        fields = [
            'full_name', 'usn',
            'college_email', 'personal_email', 'phone_number',
            'department', 'current_semester', 'current_year',
            'tenth_percentage',
            'pre_university_qualification_type',
            'pre_university_percentage',
            'cgpa', 'backlogs', 'batch',
            'domains',
            'languages_known',
            # New professional link fields
            'linkedin_url',
            'github_url',
            'leetcode_url',
            'hackerrank_url',
            # New certification fields
            'certifications_list',
            'certifications_drive_link',
            'photo', 'resume',
        ]
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'your-tailwind-classes-for-file-input'}),
            'resume': forms.FileInput(attrs={'class': 'your-tailwind-classes-for-file-input'}),
            'college_email': forms.EmailInput(attrs={'placeholder': 'yourusn@vvce.ac.in'}),
            'personal_email': forms.EmailInput(attrs={'placeholder': 'your.name@example.com'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'e.g., 9876543210'}),
            'tenth_percentage': forms.NumberInput(attrs={'step': "0.01", 'min': "0", 'max': "100", 'placeholder': 'e.g., 85.50'}),
            'pre_university_percentage': forms.NumberInput(attrs={'step': "0.01", 'min': "0", 'max': "100", 'placeholder': 'e.g., 75.25'}),
            'cgpa': forms.NumberInput(attrs={'step': "0.01", 'min': "0", 'max': "10", 'placeholder': 'e.g., 8.5'}),
            'backlogs': forms.NumberInput(attrs={'min': "0", 'placeholder': 'e.g., 0'}),
            
            # Widgets for new fields
            'linkedin_url': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/yourprofile'}),
            'github_url': forms.URLInput(attrs={'placeholder': 'https://github.com/yourusername'}),
            'leetcode_url': forms.URLInput(attrs={'placeholder': 'https://leetcode.com/yourusername'}),
            'hackerrank_url': forms.URLInput(attrs={'placeholder': 'https://hackerrank.com/yourusername'}),
            'certifications_list': forms.Textarea(attrs={'rows': 4, 'placeholder': "List your certifications and achievements, e.g.:\n- Google Certified Associate Cloud Engineer\n- Winner, XYZ Hackathon 2023\n- Published paper on ABC"}),
            'certifications_drive_link': forms.URLInput(attrs={'placeholder': 'Link to Google Drive/Dropbox folder with certificates'}),
        }
        help_texts = { # Example help texts
            'tenth_percentage': 'Enter percentage (0-100).',
            'pre_university_percentage': 'Enter percentage (0-100) for your 12th/Diploma.',
            'leetcode_url': 'Optional',
            'hackerrank_url': 'Optional',
            'certifications_list': 'Optional. List key achievements.',
            'certifications_drive_link': 'Optional. Share a link to a folder/PDF of your certificates.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pre_university_percentage'].required = False
        self.fields['tenth_percentage'].required = False
        # New fields are optional by model (blank=True), so form will reflect this
        if self.instance and self.instance.pk and 'usn' in self.fields:
            self.fields['usn'].disabled = True

    # --- Keep your existing clean_ methods ---
    # (clean_college_email, clean_personal_email, clean_domains, clean_tenth_percentage, clean_pre_university_percentage, clean_photo, clean_resume)
    # ... (ensure these are present and correct from previous versions)
    def clean_college_email(self):
        email = self.cleaned_data.get('college_email')
        # if email and not email.lower().endswith('@vvce.ac.in'):
        #     raise forms.ValidationError("College email must end with @vvce.ac.in")
        if self.instance and self.instance.pk and self.instance.college_email == email:
            return email
        if StudentProfile.objects.filter(college_email__iexact=email).exists():
            raise forms.ValidationError("This college email address is already in use.")
        return email

    def clean_personal_email(self):
        email = self.cleaned_data.get('personal_email')
        if self.instance and self.instance.pk and self.instance.personal_email == email:
            return email
        if StudentProfile.objects.filter(personal_email__iexact=email).exists():
            raise forms.ValidationError("This personal email address is already in use.")
        return email

    def clean_domains(self):
        selected_domains = self.cleaned_data.get('domains')
        if not selected_domains:
             raise forms.ValidationError("Please select at least one domain.")
        if len(selected_domains) > 4:
            raise forms.ValidationError("You can select a maximum of 4 domains.")
        return selected_domains

    def clean_tenth_percentage(self):
        percentage = self.cleaned_data.get('tenth_percentage')
        if percentage is not None and not (0 <= percentage <= 100):
            raise forms.ValidationError("10th Percentage must be between 0 and 100.")
        return percentage

    def clean_pre_university_percentage(self):
        percentage = self.cleaned_data.get('pre_university_percentage')
        qualification_type = self.cleaned_data.get('pre_university_qualification_type')
        if qualification_type and percentage is None: # If type selected, percentage becomes required
             raise forms.ValidationError("Please enter the percentage for your selected 12th/Diploma qualification.")
        if percentage is not None and not (0 <= percentage <= 100):
            raise forms.ValidationError("12th/Diploma Percentage must be between 0 and 100.")
        return percentage

    MAX_PHOTO_SIZE_KB = 400
    MAX_RESUME_SIZE_KB = 1000

    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        if photo:
            if hasattr(photo, 'size') and photo.size > self.MAX_PHOTO_SIZE_KB * 1024:
                raise forms.ValidationError(f"Photo file too large. Maximum size is {self.MAX_PHOTO_SIZE_KB}KB.")
        return photo

    def clean_resume(self):
        resume = self.cleaned_data.get('resume', False)
        if resume:
            if hasattr(resume, 'size') and resume.size > self.MAX_RESUME_SIZE_KB * 1024:
                raise forms.ValidationError(f"Resume file too large. Maximum size is {self.MAX_RESUME_SIZE_KB}KB.")
        return resume


class CustomPasswordChangeForm(DjangoPasswordChangeForm):
    pass