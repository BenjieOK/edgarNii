from django.db import models


class SiteSettings(models.Model):
    """Global site settings — only one instance should exist."""
    logo_text = models.CharField(max_length=100, default="Nii Kpakpo")
    footer_legal_text = models.CharField(
        max_length=200,
        default="Paid for by the Committee to Elect Edgar Nii Kpakpo",
    )
    footer_copyright_text = models.CharField(
        max_length=200,
        default="© 2025 Nii Kpakpo for Office. All Rights Reserved.",
    )
    twitter_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    donate_url = models.CharField(max_length=200, default="#")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HeroSection(models.Model):
    title = models.CharField(max_length=200, default="Progress, Unity, and Action")
    subtitle = models.CharField(
        max_length=300,
        default="Committed to building a stronger community for everyone.",
    )
    cta_text = models.CharField(max_length=100, default="Learn My Stance")
    cta_link = models.CharField(max_length=200, default="#issues")
    background_image = models.ImageField(
        upload_to="hero/", blank=True, null=True,
        help_text="Upload a hero background image. Leave blank to use the default.",
    )

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return "Hero Section"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class AboutSection(models.Model):
    candidate_name = models.CharField(max_length=100, default="Edgar Nii Kpakpo")
    bio_paragraph_1 = models.TextField(
        default=(
            "For over 15 years, Edgar Nii Kpakpo has been a dedicated public servant, "
            "community organizer, and advocate for working families. His career is built "
            "on a foundation of listening to his constituents and turning their concerns "
            "into effective policy."
        )
    )
    bio_paragraph_2 = models.TextField(
        default=(
            "Edgar believes in a future where our economy is strong, our schools are "
            "world-class, and our environment is protected for generations to come. He is "
            "running for office to bring common-sense solutions and a collaborative spirit "
            "to government."
        )
    )
    portrait_image = models.ImageField(
        upload_to="about/", blank=True, null=True,
        help_text="Professional portrait photo.",
    )
    cta_text = models.CharField(max_length=100, default="Get In Touch")
    cta_link = models.CharField(max_length=200, default="/contact/")

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self):
        return "About Section"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class IssueCard(models.Model):
    icon_class = models.CharField(
        max_length=100,
        default="work",
        help_text="Material Icons name, e.g. 'work', 'school', 'eco', 'health_and_safety'",
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Key Issue"
        verbose_name_plural = "Key Issues"

    def __str__(self):
        return self.title


class CTASection(models.Model):
    title = models.CharField(max_length=200, default="Join the Movement")
    subtitle = models.TextField(
        default=(
            "Your support is crucial. Volunteer your time, sign up for updates, "
            "or make a contribution to power our campaign forward."
        )
    )
    volunteer_text = models.CharField(max_length=100, default="Volunteer")
    volunteer_link = models.CharField(max_length=200, default="/contact/")
    subscribe_text = models.CharField(max_length=100, default="Subscribe")
    subscribe_link = models.CharField(max_length=200, default="/blog/#newsletter")

    class Meta:
        verbose_name = "CTA Section"
        verbose_name_plural = "CTA Section"

    def __str__(self):
        return "Call-to-Action Section"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ("Community", "Community"),
        ("Policy", "Policy"),
        ("Education", "Education"),
        ("Events", "Events"),
        ("Economy", "Economy"),
        ("Healthcare", "Healthcare"),
        ("Other", "Other"),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    published_date = models.DateField()
    excerpt = models.TextField()
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="blog/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-published_date"]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title


class Project(models.Model):
    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("ongoing", "Ongoing"),
        ("proposed", "Proposed"),
        ("in-progress", "In Progress"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ongoing")
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    detail_content = models.TextField(
        blank=True, help_text="Full detail shown in a modal or detail page."
    )
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title


class Event(models.Model):
    name = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["date_time"]
        verbose_name = "Event"
        verbose_name_plural = "Upcoming Events"

    def __str__(self):
        return self.name


class ContactInfo(models.Model):
    address = models.CharField(max_length=300, default="123 Main Street, Accra, Ghana")
    phone = models.CharField(max_length=50, default="+233 000 000 000")
    email = models.EmailField(default="contact@niikpakpo.com")

    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return "Contact Information"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.full_name} — {self.subject}"


class AcademicAchievement(models.Model):
    icon_class = models.CharField(
        max_length=100,
        default="school",
        help_text="Material Icons name, e.g. 'school', 'workspace_premium', 'science'",
    )
    degree_title = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    year = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Academic Achievement"
        verbose_name_plural = "Academic Achievements"

    def __str__(self):
        return f"{self.degree_title} — {self.institution}"


class SignatureProject(models.Model):
    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("ongoing", "Ongoing"),
        ("proposed", "Proposed"),
        ("in-progress", "In Progress"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="completed")
    image = models.ImageField(upload_to="portfolio/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Signature Project (Portfolio)"
        verbose_name_plural = "Signature Projects (Portfolio)"

    def __str__(self):
        return self.title


class AllowedIP(models.Model):
    """IP addresses permitted to reach the Django admin."""
    ip_address = models.GenericIPAddressField(unique=True)
    label = models.CharField(
        max_length=200, blank=True,
        help_text="Optional note, e.g. 'Office' or 'Edgar's home'.",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Allowed Admin IP"
        verbose_name_plural = "Allowed Admin IPs"

    def __str__(self):
        return f"{self.ip_address} ({self.label})" if self.label else self.ip_address


class AccessRequest(models.Model):
    """Submitted by a visitor whose IP isn't whitelisted when they try to reach the admin."""
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("denied", "Denied"),
    ]
    ip_address = models.GenericIPAddressField()
    name = models.CharField(max_length=200)
    email = models.EmailField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-requested_at"]
        verbose_name = "Admin Access Request"
        verbose_name_plural = "Admin Access Requests"

    def __str__(self):
        return f"{self.name} ({self.ip_address}) — {self.get_status_display()}"


class ConstituencyWork(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    testimonial_quote = models.TextField(blank=True)
    testimonial_author = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Constituency Work"
        verbose_name_plural = "Constituency Work"

    def __str__(self):
        return self.title
