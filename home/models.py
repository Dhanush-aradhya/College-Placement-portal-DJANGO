# home/models.py
from django.db import models
from django.contrib.auth.models import User
import os
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator

# --- Helper functions for upload_to ---
# ... (keep get_student_photo_path, get_student_resume_path) ...
def get_student_photo_path(instance, filename):
    return f'student_photos/user_{instance.user.id}/{filename}'

def get_student_resume_path(instance, filename):
    return f'student_resumes/user_{instance.user.id}/{filename}'


# --- CHOICES definitions ---
# ... (keep DEPARTMENT_CHOICES, SEMESTER_CHOICES, YEAR_CHOICES, BATCH_CHOICES, PRE_UNIVERSITY_QUALIFICATION_CHOICES) ...
DEPARTMENT_CHOICES = [('cse', 'Computer Science & Engineering'), ('ise', 'Information Science & Engineering'), ('aiml', 'AI & Machine Learning'), ('ece', 'Electronics & Communication Engineering'), ('eee', 'Electrical & Electronics Engineering'), ('me', 'Mechanical Engineering'), ('ce', 'Civil Engineering')]
SEMESTER_CHOICES = [(str(i), f'{i}{"st" if i==1 else "nd" if i==2 else "rd" if i==3 else "th"} Semester') for i in range(1, 9)]
YEAR_CHOICES = [(str(i), f'{i}{"st" if i==1 else "nd" if i==2 else "rd" if i==3 else "th"} Year') for i in range(1, 5)]
BATCH_CHOICES = [(f"{year}-{year+4}", f"{year}-{year+4}") for year in range(2020, 2026)]
PRE_UNIVERSITY_QUALIFICATION_CHOICES = [('12th', '12th / PUC'), ('diploma', 'Diploma')]


# --- Existing Models ---
class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self): return self.name
    class Meta: ordering = ['name']

class Domain(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name
    class Meta: ordering = ['name']

# --- Updated StudentProfile Model ---
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    usn = models.CharField(max_length=20, unique=True, help_text="University Seat Number (matches username)")
    full_name = models.CharField(max_length=100)
    college_email = models.EmailField(max_length=255, unique=True, help_text="Official college email address")
    personal_email = models.EmailField(max_length=255, unique=True, help_text="Personal email address")
    phone_number = models.CharField(max_length=15, help_text="Contact phone number")

    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    current_semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    current_year = models.CharField(max_length=10, choices=YEAR_CHOICES)

    tenth_percentage = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], help_text="Percentage obtained in 10th standard (0-100)")
    pre_university_qualification_type = models.CharField(max_length=10, choices=PRE_UNIVERSITY_QUALIFICATION_CHOICES, null=True, blank=True, help_text="Qualification type: 12th/PUC or Diploma")
    pre_university_percentage = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], help_text="Percentage for 12th/PUC or Diploma (0-100)")

    cgpa = models.FloatField(help_text="Current Cumulative Grade Point Average")
    backlogs = models.IntegerField(default=0, help_text="Number of current backlogs")
    batch = models.CharField(max_length=9, choices=BATCH_CHOICES, help_text="e.g., 2021-2025")

    domains = models.ManyToManyField(Domain, blank=False, related_name='student_profiles', help_text="Select up to 4 domains of interest.")
    languages_known = models.ManyToManyField(Language, blank=True, help_text="Select languages you know.")

    # --- New Professional Links ---
    linkedin_url = models.URLField(max_length=255, blank=True, null=True, help_text="Link to your LinkedIn profile")
    github_url = models.URLField(max_length=255, blank=True, null=True, help_text="Link to your GitHub profile")
    leetcode_url = models.URLField(max_length=255, blank=True, null=True, help_text="Link to your LeetCode profile (optional)")
    hackerrank_url = models.URLField(max_length=255, blank=True, null=True, help_text="Link to your HackerRank profile (optional)")
    # --- End New Professional Links ---

    # --- New Certification/Achievements Fields ---
    certifications_list = models.TextField(
        blank=True, null=True,
        help_text="List your certifications or achievements, one per line (e.g., 'Google Cloud Certified - Associate Cloud Engineer', 'Winner of XYZ Hackathon')."
    )
    certifications_drive_link = models.URLField(
        max_length=500, # Drive links can be long
        blank=True, null=True,
        help_text="A single Google Drive/OneDrive/Dropbox link to a folder or PDF containing all your certificates/proof of achievements (optional)."
    )
    # --- End New Certification/Achievements Fields ---

    # REMOVED: certification_links (replaced by the two fields above)

    photo = models.ImageField(upload_to=get_student_photo_path, blank=True, null=True)
    resume = models.FileField(upload_to=get_student_resume_path, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.usn})"

    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"