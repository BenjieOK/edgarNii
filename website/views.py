from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

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
from .forms import ContactForm


def _site(request):
    """Return common site-wide context. nav_class defaults to is-scrolled (opaque)."""
    return {
        "site": SiteSettings.get(),
        "nav_class": "is-scrolled",
    }


def home(request):
    ctx = _site(request)
    ctx["nav_class"] = ""  # transparent nav — hero is dark
    ctx.update({
        "hero": HeroSection.get(),
        "about": AboutSection.get(),
        "issues": IssueCard.objects.all(),
        "cta": CTASection.get(),
        "recent_posts": BlogPost.objects.filter(is_published=True)[:3],
    })
    return render(request, "website/home.html", ctx)


def blog(request):
    ctx = _site(request)
    selected_category = request.GET.get("category", "")
    posts = BlogPost.objects.filter(is_published=True)
    if selected_category:
        posts = posts.filter(category=selected_category)

    featured = posts.filter(is_featured=True).first()
    # If nothing explicitly featured, use the latest (only when showing all)
    if featured is None and not selected_category:
        featured = posts.first()
    other_posts = posts.exclude(pk=featured.pk) if featured else posts

    ctx.update({
        "featured": featured,
        "posts": other_posts,
        "categories": BlogPost.CATEGORY_CHOICES,
        "selected_category": selected_category,
    })
    return render(request, "website/blog.html", ctx)


def blog_detail(request, pk):
    ctx = _site(request)
    post = get_object_or_404(BlogPost, pk=pk, is_published=True)
    related = BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)[:3]
    ctx.update({
        "post": post,
        "related": related,
    })
    return render(request, "website/blog_detail.html", ctx)


def projects(request):
    ctx = _site(request)
    ctx["projects"] = Project.objects.filter(is_visible=True)
    return render(request, "website/projects.html", ctx)


def portfolio(request):
    ctx = _site(request)
    ctx.update({
        "academics": AcademicAchievement.objects.all(),
        "sig_projects": SignatureProject.objects.all(),
        "constituency": ConstituencyWork.objects.all(),
    })
    return render(request, "website/portfolio.html", ctx)


def contact(request):
    ctx = _site(request)
    ctx.update({
        "contact_info": ContactInfo.get(),
        "events": Event.objects.all(),
    })
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent. Thank you!")
            return redirect("contact")
        else:
            ctx["form"] = form
    else:
        ctx["form"] = ContactForm()
    return render(request, "website/contact.html", ctx)
