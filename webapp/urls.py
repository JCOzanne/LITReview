from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('home/', blog.views.home, name='home'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('create_review/<int:ticket_id>/', blog.views.create_review, name='create_review'),
    path('create_review/', blog.views.create_review_and_ticket, name='create_review_and_ticket'),
    path('create_ticket/', blog.views.create_ticket, name='create_ticket'),
    path('follow/', blog.views.follow_users, name='follow_users'),
    path('unfollow/<str:username>/', blog.views.unfollow_user, name='unfollow_user'),
    path('block/<str:username>/', blog.views.block_user, name='block_user'),
    path('unblock/<str:username>/', blog.views.unblock_user, name='unblock_user'),
    path('ticket/<int:ticket_id>/edit/', blog.views.edit_ticket, name='edit_ticket'),
    path('ticket/<int:ticket_id>/delete/', blog.views.delete_ticket, name='delete_ticket'),
    path('review/<int:review_id>/edit/', blog.views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', blog.views.delete_review, name='delete_review'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)