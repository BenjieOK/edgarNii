"""
Run with: venv/bin/python seed_data.py
Seeds the database with the original static-site content.
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from website.models import (
    SiteSettings, HeroSection, AboutSection, IssueCard, CTASection,
    BlogPost, Project, Event, ContactInfo,
    AcademicAchievement, SignatureProject, ConstituencyWork,
)
from datetime import date, datetime
from django.utils import timezone


# Site settings
s = SiteSettings.get()
s.logo_text = "Nii Kpakpo"
s.footer_legal_text = "Paid for by the Committee to Elect Edgar Nii Kpakpo"
s.footer_copyright_text = "© 2025 Nii Kpakpo for Office. All Rights Reserved."
s.save()
print("✓ SiteSettings")

# Hero
h = HeroSection.get()
h.title = "Progress, Unity, and Action"
h.subtitle = "Committed to building a stronger community for everyone."
h.cta_text = "Learn My Stance"
h.cta_link = "#issues"
h.save()
print("✓ HeroSection")

# About
a = AboutSection.get()
a.candidate_name = "Edgar Nii Kpakpo Addo"
a.bio_paragraph_1 = (
    "Edgar Nii Kpakpo Addo is a distinguished Maritime Education Practitioner, "
    "Certified Engineer, and Entrepreneur. Deeply committed to his faith and family, "
    "his mission is anchored in leveraging technical education to drive Ghana's "
    "industrialization."
)
a.bio_paragraph_2 = (
    "He bridges the gap between the classroom and the rig. His work involves "
    "designing, fabricating, and maintaining engineering structures for global giants "
    "like SMTC Global and Rig World Ghana. He believes that true economic liberation "
    "for the youth lies in competency-based skill acquisition."
)
a.save()
print("✓ AboutSection")

# Issues
issues = [
    ("work", "Economic Growth",
     "Fostering small business innovation and creating well-paying jobs to ensure a prosperous future for all."),
    ("school", "Education Reform",
     "Investing in our public schools, supporting our teachers, and ensuring every child has access to quality education."),
    ("eco", "Environmental Protection",
     "Championing clean energy initiatives and protecting our natural resources for a sustainable tomorrow."),
]
IssueCard.objects.all().delete()
for i, (icon, title, desc) in enumerate(issues):
    IssueCard.objects.create(icon_class=icon, title=title, description=desc, order=i)
print("✓ IssueCards")

# CTA
cta = CTASection.get()
cta.title = "Join the Movement"
cta.subtitle = (
    "Your support is crucial. Volunteer your time, sign up for updates, "
    "or make a contribution to power our campaign forward."
)
cta.save()
print("✓ CTASection")

# Blog posts
BlogPost.objects.all().delete()
BlogPost.objects.create(
    title="A New Plan for Local Infrastructure",
    category="Community",
    published_date=date(2025, 9, 16),
    excerpt=(
        "Today, Edgar Nii Kpakpo unveiled a comprehensive plan to revitalize our roads, "
        "bridges, and public transit systems. This initiative aims to create jobs and "
        "improve daily life for all residents..."
    ),
    is_featured=True,
)
BlogPost.objects.create(
    title="Expanding Access to Quality Healthcare",
    category="Healthcare",
    published_date=date(2025, 9, 12),
    excerpt=(
        "Edgar speaks about his commitment to ensuring every family has affordable "
        "and reliable healthcare options..."
    ),
)
BlogPost.objects.create(
    title="Town Hall with Local Educators",
    category="Education",
    published_date=date(2025, 9, 8),
    excerpt=(
        "A recap of the productive discussion with teachers and parents about the "
        "future of our school district..."
    ),
)
print("✓ BlogPosts")

# Projects
Project.objects.all().delete()
Project.objects.create(
    title="Downtown Revitalization Act",
    description=(
        "Secured funding to restore historic downtown storefronts, improve public parks, "
        "and support local businesses, leading to a 15% increase in local commerce."
    ),
    status="completed",
    order=0,
)
Project.objects.create(
    title="Community Health Initiative",
    description=(
        "Partnered with local clinics to provide free health screenings and wellness "
        "programs, aiming to improve access to healthcare for underserved populations."
    ),
    status="ongoing",
    order=1,
)
print("✓ Projects")

# Events
Event.objects.all().delete()
Event.objects.create(
    name="Community Town Hall",
    date_time=timezone.make_aware(datetime(2025, 10, 5, 19, 0)),
    location="Anytown Community Center",
    order=0,
)
Event.objects.create(
    name="Meet & Greet Fundraiser",
    date_time=timezone.make_aware(datetime(2025, 10, 12, 18, 0)),
    location="The Grand Ballroom",
    order=1,
)
Event.objects.create(
    name="Volunteer Canvassing Day",
    date_time=timezone.make_aware(datetime(2025, 10, 18, 10, 0)),
    location="Campaign HQ",
    order=2,
)
print("✓ Events")

# Contact info
ci = ContactInfo.get()
ci.address = "123 Main Street, Suite 45, Accra, Ghana"
ci.phone = "+233 000 000 000"
ci.email = "contact@niikpakpo.com"
ci.save()
print("✓ ContactInfo")

# Academic achievements
AcademicAchievement.objects.all().delete()
AcademicAchievement.objects.create(
    icon_class="science",
    degree_title="PhD Candidate, Material Science and Engineering",
    institution="University of Ghana",
    year="In Progress",
    description="Concurrently established as a leading expert and lecturer at the Regional Maritime University.",
    order=0,
)
AcademicAchievement.objects.create(
    icon_class="school",
    degree_title="MSc, Mechanical Engineering Technology",
    institution="University of Education, Winneba",
    year="—",
    order=1,
)
AcademicAchievement.objects.create(
    icon_class="school",
    degree_title="BSc, Instrumentation and Control Engineering",
    institution="—",
    year="—",
    order=2,
)
AcademicAchievement.objects.create(
    icon_class="workspace_premium",
    degree_title="Professional Engineering Certification (PE 02583)",
    institution="Council of Engineers",
    year="—",
    description="Corporate member of the Council of Engineers and a certified TVET Facilitator.",
    order=3,
)
print("✓ AcademicAchievements")

# Signature projects (portfolio)
SignatureProject.objects.all().delete()
SignatureProject.objects.create(
    title="Downtown Revitalization Act",
    description=(
        "Secured funding to restore historic downtown storefronts, improve public parks, "
        "and support local businesses, leading to a 15% increase in local commerce."
    ),
    status="completed",
    order=0,
)
SignatureProject.objects.create(
    title="Tech in Schools Program",
    description=(
        "A successful program that equipped over 5,000 students with laptops and provided "
        "enhanced technology training for educators across the district."
    ),
    status="completed",
    order=1,
)
print("✓ SignatureProjects")

# Constituency work
ConstituencyWork.objects.all().delete()
ConstituencyWork.objects.create(
    title="Weekly Town Halls",
    description=(
        "Established and maintained a commitment to hosting weekly open-door town halls. "
        "Since 2018, over 300 sessions have been held, addressing thousands of constituent "
        "concerns directly."
    ),
    testimonial_quote=(
        "Edgar's weekly meetings are a game-changer. I raised an issue about road safety in "
        "our neighborhood, and within a month, speed bumps were installed. He listens and he acts."
    ),
    testimonial_author="Adoley Mensah, Madina Resident",
    order=0,
)
ConstituencyWork.objects.create(
    title="Youth Mentorship Program",
    description=(
        "Launched a mentorship program connecting young adults with local business leaders in Accra. "
        "The program has successfully placed over 150 mentees in internships and apprenticeships."
    ),
    order=1,
)
print("✓ ConstituencyWork")

print("\nAll seed data loaded successfully!")
