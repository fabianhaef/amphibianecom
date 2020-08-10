from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views
from cart.views import ProductHomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', ProductHomeView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('shop/', include('cart.urls', namespace='cart')),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('staff/', include('staff.urls', namespace='staff')),
    path('about/', views.AboutView.as_view(), name='about'),
    path('licences/', views.LicenceView.as_view(), name='licence'),
    path('terms-and-conditions/', views.TermsAndConditionsView.as_view(), name='terms-and-condition'),
    path('cookie-policy/', views.CookiePolicyView.as_view(), name='cookie-policy'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('impressum/', views.ImpressumView.as_view(), name='impressum'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
