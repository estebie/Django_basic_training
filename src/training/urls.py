from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from django.contrib.auth.views import LoginView, LogoutView

from menus.views import HomeView
from profiles.views import ProfileFollowToggle, RegisterView, activate_user_view, ProfileSearchDetailview

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view, name='activate'),
    url(r'^search/$', ProfileSearchDetailview.as_view(), name='search'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^restaurants/', include('restaurants.urls', namespace='restaurants')),
    url(r'^follow/$', ProfileFollowToggle.as_view(), name='follow'),
    url(r'^u/', include('profiles.urls', namespace='profiles')),
    url(r'^items/', include('menus.urls', namespace='menus')),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
