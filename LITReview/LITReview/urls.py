"""
URL configuration for LITReview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView

import authentication.views
import book_reviews.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", LoginView.as_view(template_name="authentication/login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", authentication.views.logout_user, name="logout"),
    path("home/", book_reviews.views.display_ticket_review_flux, name="home"),
    path("posts/", book_reviews.views.display_ticket_review_posts, name="posts"),
    path("manage-users/", book_reviews.views.search_user, name="manage_users"),
    path("follow-action/", book_reviews.views.follow_action, name="follow_action"),
    path("signup/", authentication.views.signup_page, name="signup"),
    path("create-ticket/", book_reviews.views.create_ticket , name="create_ticket"),
    path("update-ticket/<int:ticket_id>/", book_reviews.views.update_ticket, name="update_ticket"),
    path("delete-ticket/<int:ticket_id>/", book_reviews.views.delete_ticket, name="delete_ticket"),
    path("create-review/<int:ticket_id>/", book_reviews.views.create_review , name="create_review"),
    path("update-review/<int:review_id>/", book_reviews.views.update_review, name="update_review"),
    path("delete-review/<int:review_id>/", book_reviews.views.delete_review, name="delete_review"),
    path("create_ticket_and_review/", book_reviews.views.create_ticket_and_review, name="create_ticket_and_review"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
