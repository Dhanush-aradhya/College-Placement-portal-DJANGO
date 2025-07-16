import csv # For reading student USNs from a CSV file (optional)
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
# from home.models import StudentProfile # We'll create profiles later, not in this command yet

# --- Configuration for User Creation ---
# For students, USN will be the username.
# You can prepare a CSV file with a list of USNs.
# Format of student_usns.csv (one USN per line in a column named 'USN'):
# USN
# 1VV21CS001
# 1VV21CS002
# ...
STUDENT_USN_CSV_PATH = 'student_usns.csv' # Place this CSV in your project's root directory
DEFAULT_STUDENT_PASSWORD = 'password' # Students MUST change this on first login

FACULTY_ACCOUNTS = [
    {'username': 'ravikumar', 'email': 'ravikumarv@vvce.ac.in', 'password': 'vvce@001', 'first_name': 'Ravi', 'last_name': 'Kumar'},
    {'username': 'nithin', 'email': 'nithingowda021@vvce.ac.in', 'password': 'vvce@002', 'first_name': 'Nithin', 'last_name': 'Kumar'},
    {'username': 'dhanush', 'email': 'vvce22cse0162@vvce.ac.in', 'password': 'vvce@003', 'first_name': 'Dhanush', 'last_name': 'Aradhya'},
    {'username': 'placement', 'email': '', 'password': 'vvce@placement', 'first_name': 'placement', 'last_name': 'placement'},
    # Add more faculty as needed
]
# --- End Configuration ---


class Command(BaseCommand):
    help = 'Creates initial student and faculty users for the placement portal.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting user creation process...'))

        # --- Create Student Users ---
        created_students_count = 0
        skipped_students_count = 0
        try:
            with open(STUDENT_USN_CSV_PATH, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                if 'USN' not in reader.fieldnames:
                    raise CommandError(f"CSV file '{STUDENT_USN_CSV_PATH}' must contain a 'USN' column.")

                for row in reader:
                    usn = row['USN'].strip()
                    if not usn:
                        self.stdout.write(self.style.WARNING(f"Skipping empty USN in CSV."))
                        continue

                    if User.objects.filter(username=usn).exists():
                        self.stdout.write(self.style.WARNING(f"Student user with USN '{usn}' already exists. Skipping."))
                        skipped_students_count += 1
                        continue
                    try:
                        User.objects.create_user(username=usn, password=DEFAULT_STUDENT_PASSWORD)
                        # Note: We are not creating StudentProfile here yet. That happens when student first uploads details.
                        # Or, you could create a basic StudentProfile here if needed:
                        # user_instance = User.objects.get(username=usn)
                        # StudentProfile.objects.create(user=user_instance, usn=usn, full_name="To Be Updated") # etc.
                        self.stdout.write(self.style.SUCCESS(f"Successfully created student user: {usn}"))
                        created_students_count += 1
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f"Error creating student user {usn}: {e}"))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Student USN file not found: '{STUDENT_USN_CSV_PATH}'. Please create it."))
            self.stdout.write(self.style.WARNING("Skipping student user creation due to missing CSV file."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred while processing student CSV: {e}"))

        self.stdout.write(f"\n--- Student User Creation Summary ---")
        self.stdout.write(self.style.SUCCESS(f"Created: {created_students_count}"))
        self.stdout.write(self.style.WARNING(f"Skipped (already exist): {skipped_students_count}\n"))


        # --- Create Faculty Users ---
        created_faculty_count = 0
        skipped_faculty_count = 0
        self.stdout.write("--- Creating Faculty Users ---")
        for acc in FACULTY_ACCOUNTS:
            username = acc['username']
            email = acc.get('email', f'{username}@example.com') # Default email if not provided
            password = acc['password']
            first_name = acc.get('first_name', '')
            last_name = acc.get('last_name', '')

            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f"Faculty user '{username}' already exists. Skipping."))
                skipped_faculty_count += 1
                continue
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_staff = True # Crucial for admin portal access
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Successfully created faculty user: {username} (staff status set)"))
                created_faculty_count += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error creating faculty user {username}: {e}"))

        self.stdout.write(f"\n--- Faculty User Creation Summary ---")
        self.stdout.write(self.style.SUCCESS(f"Created: {created_faculty_count}"))
        self.stdout.write(self.style.WARNING(f"Skipped (already exist): {skipped_faculty_count}\n"))

        self.stdout.write(self.style.SUCCESS('User creation process finished.'))