import json
import datetime
from django.conf import settings
from django.shortcuts import redirect, render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product, OrderItem, Address, Payment, Order
from .utils import get_or_set_order_session
from django.shortcuts import get_object_or_404, reverse
from .forms import AddToCartForm, AddressForm
from django.contrib import messages
from django.http import JsonResponse
from .filters import ProductFilter


class ProductHomeView(generic.ListView):
    template_name = 'cart/home.html'
    queryset = Product.objects.all()
    context_object_name = 'products'
    ordering = ['-created']
    paginate_by = 12


def product_list(request):
    qs = Product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=qs)
    return render(request, 'cart/product-list.html', {'filter': product_filter})

'''
class ProductListView(generic.ListView):
    template_name = 'cart/product-list.html'
    model = Product
    filter_set = ProductFilter

    def get_queryset(self):
        qs = self.model.objects.all()
        product_filtered_list = ProductFilter(self.request.GET, qs)
        return product_filtered_list.qs
'''

class SoundkitListView(generic.ListView):
    template_name = 'cart/soundkit-list.html'
    queryset = Product.objects.all()


class SoundkitDetailView(generic.FormView):
    template_name = 'cart/soundkit-detail.html'
    form_class = AddToCartForm

    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse("cart:summary")

    def get_form_kwargs(self):
        kwargs = super(SoundkitDetailView, self).get_form_kwargs()
        kwargs['product_id'] = self.get_object().id
        return kwargs

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        product = self.get_object()

        item_filter = order.items.filter(
            product=product,
            licence_variation=form.cleaned_data['licence_variation'],
        )
        if item_filter.exists():
            item = item_filter.first()
            item.save()

        else:
            new_item = form.save(commit=False)
            new_item.product = product
            new_item.order = order
            new_item.save()

        return super(SoundkitDetailView, self).form_valid(form)


class ProductDetailView(generic.FormView):
    template_name = 'cart/product-detail.html'
    form_class = AddToCartForm

    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse("cart:summary")

    def get_form_kwargs(self):
        kwargs = super(ProductDetailView, self).get_form_kwargs()
        kwargs['product_id'] = self.get_object().id
        return kwargs

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        product = self.get_object()

        item_filter = order.items.filter(
            product=product,
            licence_variation=form.cleaned_data['licence_variation'],
        )
        if item_filter.exists():
            item = item_filter.first()
            item.save()

        else:
            new_item = form.save(commit=False)
            new_item.product = product
            new_item.order = order
            new_item.save()

        return super(ProductDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context


class CartView(generic.TemplateView):
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context["order"] = get_or_set_order_session(self.request)
        return context


class RemoveFromCartView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.delete()
        return redirect('cart:summary')


class CheckoutView(generic.FormView):
    template_name = 'cart/checkout.html'
    form_class = AddressForm

    def get_success_url(self):
        return reverse("cart:payment")

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        selected_shipping_address = form.cleaned_data.get(
            'selected_shipping_address')
        selected_billing_address = form.cleaned_data.get(
            'selected_billing_address')

        if selected_shipping_address:
            order.shipping_address = selected_shipping_address
        else:
            address = Address.objects.create(
                address_type='S',
                user=self.request.user,
                address_line_1=form.cleaned_data['shipping_address_line_1'],
                address_line_2=form.cleaned_data['shipping_address_line_2'],
                zip_code=form.cleaned_data['shipping_zip_code'],
                city=form.cleaned_data['shipping_city'],
            )
            order.shipping_address = address

        if selected_billing_address:
            order.billing_address = selected_billing_address
        else:
            address = Address.objects.create(
                address_type='B',
                user=self.request.user,
                address_line_1=form.cleaned_data['billing_address_line_1'],
                address_line_2=form.cleaned_data['billing_address_line_2'],
                zip_code=form.cleaned_data['billing_zip_code'],
                city=form.cleaned_data['billing_city'],
            )
            order.billing_address = address

        order.save()
        messages.info(
            self.request, "You have successfully added your addresses")
        return super(CheckoutView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context["order"] = get_or_set_order_session(self.request)
        return context


class PaymentView(generic.TemplateView):
    template_name = 'cart/payment.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context["PAYPAL_CLIENT_ID"] = settings.PAYPAL_CLIENT_ID
        context['order'] = get_or_set_order_session(self.request)
        context["CALLBACK_URL"] = reverse('cart:thank-you')
        return context


class ConfirmOrderView(generic.View):
    def post(self, request, *args, **kwargs):
        order = get_or_set_order_session(request)
        body = json.loads(request.body)
        payment = Payment.objects.create(
            order=order,
            successful=True,
            raw_response=json.dumps(body),
            amount=float(body["purchase_units"][0]["amount"]["value"]),
            payment_method='PayPal'
        )
        order.ordered = True
        order.ordered_date = datetime.date.today()
        order.save()
        return JsonResponse({"data": "success"})


class ThankYouView(generic.TemplateView):
    template_name = 'cart/thanks.html'


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'order.html'
    queryset = Order.objects.all()
    context_object_name = 'order'
