from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    SiteSettings,
    HeroSection,
    AboutSection,
    IssueCard,
    CTASection,
    BlogPost,
    Project,
    Event,
    ContactInfo,
    ContactMessage,
    AcademicAchievement,
    SignatureProject,
    ConstituencyWork,
)


# ─── Display helpers ───────────────────────────────────────────────────────

def _thumb(image_field, size=44):
    """Small square thumbnail for changelist columns."""
    if not image_field:
        return mark_safe('<span class="no-thumb">—</span>')
    return format_html(
        '<img src="{}" class="admin-thumb" style="width:{}px;height:{}px;" />',
        image_field.url, size, size,
    )


def _image_preview(image_field):
    """Larger preview for the change form, shown above the upload field."""
    if not image_field:
        return mark_safe('<span class="no-thumb">No image uploaded yet.</span>')
    return format_html(
        '<img src="{}" class="admin-image-preview" />', image_field.url,
    )


STATUS_COLORS = {
    "completed":   ("#2d7664", "#f1fbde"),
    "ongoing":     ("#8c6f14", "#fbf3d9"),
    "proposed":    ("#5a5a6e", "#eceef2"),
    "in-progress": ("#265e50", "#eef2e6"),
}


def _status_badge(status, display):
    fg, bg = STATUS_COLORS.get(status, ("#5a5a6e", "#eceef2"))
    return format_html(
        '<span class="status-badge" style="color:{};background:{};">{}</span>',
        fg, bg, display,
    )


def _bool_badge(value, true_label, false_label):
    if value:
        return format_html('<span class="status-badge status-badge--on">{}</span>', true_label)
    return format_html('<span class="status-badge status-badge--off">{}</span>', false_label)


# ─── Singleton admin mixin ────────────────────────────────────────────────────

class SingletonModelAdmin(admin.ModelAdmin):
    """Admin class for models that should only ever have one row."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Redirect straight to the single object's change page.
        obj, _ = self.model.objects.get_or_create(pk=1)
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        app = self.model._meta.app_label
        model = self.model._meta.model_name
        return HttpResponseRedirect(reverse(f"admin:{app}_{model}_change", args=[obj.pk]))


# ─── Site-wide singletons ─────────────────────────────────────────────────────

@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):
    fieldsets = (
        ("Navigation & Branding", {"fields": ("logo_text", "donate_url")}),
        (
            "Footer",
            {"fields": ("footer_legal_text", "footer_copyright_text")},
        ),
        (
            "Social Media Links",
            {"fields": ("twitter_url", "facebook_url", "instagram_url")},
        ),
    )


# ─── Home page sections ───────────────────────────────────────────────────────

@admin.register(HeroSection)
class HeroSectionAdmin(SingletonModelAdmin):
    readonly_fields = ("background_preview",)
    fieldsets = (
        ("Hero Text", {"fields": ("title", "subtitle")}),
        ("Call-to-Action Button", {"fields": ("cta_text", "cta_link")}),
        ("Background Image", {"fields": ("background_preview", "background_image")}),
    )

    @admin.display(description="Current Background")
    def background_preview(self, obj):
        return _image_preview(obj.background_image)


@admin.register(AboutSection)
class AboutSectionAdmin(SingletonModelAdmin):
    readonly_fields = ("portrait_preview",)
    fieldsets = (
        ("Candidate", {"fields": ("candidate_name", "portrait_preview", "portrait_image")}),
        ("Biography", {"fields": ("bio_paragraph_1", "bio_paragraph_2")}),
        ("Button", {"fields": ("cta_text", "cta_link")}),
    )

    @admin.display(description="Current Portrait")
    def portrait_preview(self, obj):
        return _image_preview(obj.portrait_image)


@admin.register(IssueCard)
class IssueCardAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "icon_class")
    list_editable = ("order", "title", "icon_class")
    list_display_links = None
    ordering = ("order",)
    fieldsets = (
        (None, {"fields": ("order", "icon_class", "title", "description")}),
    )


@admin.register(CTASection)
class CTASectionAdmin(SingletonModelAdmin):
    fieldsets = (
        ("Text", {"fields": ("title", "subtitle")}),
        (
            "Buttons",
            {
                "fields": (
                    "volunteer_text",
                    "volunteer_link",
                    "subscribe_text",
                    "subscribe_link",
                )
            },
        ),
    )


# ─── Blog ─────────────────────────────────────────────────────────────────────

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title", "category", "published_date", "is_featured", "is_published")
    list_display_links = ("title",)
    list_editable = ("category", "is_featured", "is_published")
    list_filter = ("category", "is_featured", "is_published")
    search_fields = ("title", "excerpt", "content")
    date_hierarchy = "published_date"
    readonly_fields = ("image_preview",)
    fieldsets = (
        (None, {"fields": ("title", "category", "published_date", "image_preview", "image")}),
        ("Content", {"fields": ("excerpt", "content")}),
        ("Options", {"fields": ("is_featured", "is_published")}),
    )

    @admin.display(description="")
    def thumb(self, obj):
        return _thumb(obj.image)

    @admin.display(description="Current Image")
    def image_preview(self, obj):
        return _image_preview(obj.image)


# ─── Projects page ────────────────────────────────────────────────────────────

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("thumb", "order", "title", "status_display", "is_visible")
    list_editable = ("order", "is_visible")
    list_display_links = ("title",)
    ordering = ("order",)
    readonly_fields = ("image_preview",)
    fieldsets = (
        (None, {"fields": ("order", "title", "status", "image_preview", "image", "is_visible")}),
        ("Content", {"fields": ("description", "detail_content")}),
    )

    @admin.display(description="")
    def thumb(self, obj):
        return _thumb(obj.image)

    @admin.display(description="Current Image")
    def image_preview(self, obj):
        return _image_preview(obj.image)

    @admin.display(description="Status", ordering="status")
    def status_display(self, obj):
        return _status_badge(obj.status, obj.get_status_display())


# ─── Contact page ─────────────────────────────────────────────────────────────

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("order", "name", "date_time", "location")
    list_editable = ("order",)
    list_display_links = ("name",)
    ordering = ("date_time",)


@admin.register(ContactInfo)
class ContactInfoAdmin(SingletonModelAdmin):
    fieldsets = (
        (None, {"fields": ("address", "phone", "email")}),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("read_badge", "full_name", "email", "subject", "submitted_at", "is_read")
    list_display_links = ("full_name",)
    list_editable = ("is_read",)
    list_filter = ("is_read",)
    search_fields = ("full_name", "email", "subject", "message")
    readonly_fields = ("full_name", "email", "subject", "message", "submitted_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    @admin.display(description="")
    def read_badge(self, obj):
        return _bool_badge(not obj.is_read, "New", "Read")

    def change_view(self, request, object_id, form_url="", extra_context=None):
        # Opening a message is how staff "read" it — mirrors an inbox, no extra click needed.
        ContactMessage.objects.filter(pk=object_id, is_read=False).update(is_read=True)
        return super().change_view(request, object_id, form_url, extra_context)


# ─── Portfolio page ───────────────────────────────────────────────────────────

@admin.register(AcademicAchievement)
class AcademicAchievementAdmin(admin.ModelAdmin):
    list_display = ("order", "degree_title", "institution", "year")
    list_editable = ("order",)
    list_display_links = ("degree_title",)
    ordering = ("order",)


@admin.register(SignatureProject)
class SignatureProjectAdmin(admin.ModelAdmin):
    list_display = ("thumb", "order", "title", "status_display")
    list_editable = ("order",)
    list_display_links = ("title",)
    ordering = ("order",)
    readonly_fields = ("image_preview",)
    fieldsets = (
        (None, {"fields": ("order", "title", "status", "image_preview", "image")}),
        ("Content", {"fields": ("description",)}),
    )

    @admin.display(description="")
    def thumb(self, obj):
        return _thumb(obj.image)

    @admin.display(description="Current Image")
    def image_preview(self, obj):
        return _image_preview(obj.image)

    @admin.display(description="Status", ordering="status")
    def status_display(self, obj):
        return _status_badge(obj.status, obj.get_status_display())


@admin.register(ConstituencyWork)
class ConstituencyWorkAdmin(admin.ModelAdmin):
    list_display = ("order", "title")
    list_editable = ("order",)
    list_display_links = ("title",)
    ordering = ("order",)
    fieldsets = (
        (None, {"fields": ("order", "title", "description")}),
        (
            "Testimonial (optional)",
            {"fields": ("testimonial_quote", "testimonial_author")},
        ),
    )
