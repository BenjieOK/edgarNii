from django.test import TestCase
from django.urls import reverse

from .models import (
    SiteSettings,
    HeroSection,
    IssueCard,
    BlogPost,
    Project,
    ContactMessage,
)


class SingletonModelTests(TestCase):
    """SiteSettings/HeroSection/etc. must always resolve to the same row."""

    def test_get_creates_and_reuses_single_row(self):
        first = SiteSettings.get()
        second = SiteSettings.get()
        self.assertEqual(first.pk, 1)
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(SiteSettings.objects.count(), 1)

    def test_save_always_pins_to_pk_one(self):
        hero = HeroSection.get()
        hero.title = "Updated Title"
        hero.save()
        self.assertEqual(hero.pk, 1)
        self.assertEqual(HeroSection.objects.count(), 1)
        self.assertEqual(HeroSection.get().title, "Updated Title")


class PageViewTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_blog_page_loads(self):
        response = self.client.get(reverse("blog"))
        self.assertEqual(response.status_code, 200)

    def test_blog_category_filter(self):
        BlogPost.objects.create(
            title="Community Post", category="Community",
            published_date="2025-01-01", excerpt="...",
        )
        BlogPost.objects.create(
            title="Policy Post", category="Policy",
            published_date="2025-01-02", excerpt="...",
        )
        response = self.client.get(reverse("blog"), {"category": "Policy"})
        self.assertEqual(response.status_code, 200)
        titles = [p.title for p in response.context["posts"]]
        self.assertNotIn("Community Post", titles)

    def test_projects_page_loads(self):
        response = self.client.get(reverse("projects"))
        self.assertEqual(response.status_code, 200)

    def test_projects_hides_invisible_projects(self):
        Project.objects.create(title="Hidden", description="...", is_visible=False)
        response = self.client.get(reverse("projects"))
        titles = [p.title for p in response.context["projects"]]
        self.assertNotIn("Hidden", titles)

    def test_portfolio_page_loads(self):
        response = self.client.get(reverse("portfolio"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_loads(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)


class ContactFormSubmissionTests(TestCase):
    def test_valid_submission_creates_message_and_redirects(self):
        response = self.client.post(reverse("contact"), {
            "full_name": "Jane Voter",
            "email": "jane@example.com",
            "subject": "Question about policy",
            "message": "I'd like to know more.",
        })
        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(ContactMessage.objects.count(), 1)
        saved = ContactMessage.objects.first()
        self.assertEqual(saved.full_name, "Jane Voter")
        self.assertFalse(saved.is_read)

    def test_invalid_submission_does_not_create_message(self):
        response = self.client.post(reverse("contact"), {
            "full_name": "",
            "email": "not-an-email",
            "subject": "",
            "message": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)


class IssueCardOrderingTests(TestCase):
    def test_issue_cards_ordered_by_order_field(self):
        IssueCard.objects.create(title="Third", description="...", order=2, icon_class="eco")
        IssueCard.objects.create(title="First", description="...", order=0, icon_class="work")
        IssueCard.objects.create(title="Second", description="...", order=1, icon_class="school")
        titles = list(IssueCard.objects.values_list("title", flat=True))
        self.assertEqual(titles, ["First", "Second", "Third"])
