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

]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)