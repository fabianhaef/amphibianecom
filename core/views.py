from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views import generic
from django.contrib import messages

from django.conf import settings

from cart.utils import get_or_set_order_session
from .forms import ContactForm
from django.core.mail import send_mail
from cart.models import Order, OrderItem


class AboutView(generic.TemplateView):
    template_name = 'about.html'


class LicenceView(generic.TemplateView):
    template_name = 'licence.html'


class TermsAndConditionsView(generic.TemplateView):
    template_name = 'terms-and-condition.html'


class CookiePolicyView(generic.TemplateView):
    template_name = 'cookie-policy.html'


class PrivacyPolicyView(generic.TemplateView):
    template_name = 'privacy-policy.html'


class ImpressumView(generic.TemplateView):
    template_name = 'impressum.html'


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            "orders": Order.objects.filter(user=self.request.user, ordered=True),
            'order_items': OrderItem.objects.all().order_by('order')
        })
        return context


class ContactView(generic.FormView):
    form_class = ContactForm
    template_name = 'contact.html'

    def get_success_url(self):
        return reverse("contact")

    def form_valid(self, form):
        messages.info(self.request, "Thanks for getting in touch. We have received your message.")
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')

        full_message = f"""
            Received message below from {name}, {email}
            ____________________________________


            {message}
            """
        send_mail(
            subject="Received contact form submission",
            message = full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list = [settings.NOTIFY_EMAIL],
        )
        return super(ContactView, self).form_valid(form)
