from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("blog/", views.blog, name="blog"),
    path("blog/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("projects/", views.projects, name="projects"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("contact/", views.contact, name="contact"),
]
