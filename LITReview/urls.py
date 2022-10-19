"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView

import authentication.views
import litr.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('signup', authentication.views.signup_page, name='signup'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('home/', litr.views.home, name='home'),
    path('posts/', litr.views.posts, name='posts'),
    path('subscriptions/', litr.views.subscriptions, name='subscriptions'),
    path('create/ticket/', litr.views.create_ticket, name='create_ticket'),
    path('create/review/', litr.views.create_review_and_ticket, name='create_review'),
    path('<int:ticket_id>/edit', litr.views.edit_ticket, name='modify_ticket'),
    path('<int:review_id>/edit', litr.views.edit_review, name='modify_review'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
