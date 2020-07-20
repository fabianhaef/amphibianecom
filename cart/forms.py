from django import forms
from .models import OrderItem, LicenceVariations, Product


class AddToCartForm(forms.ModelForm):
    licence_variation = forms.ModelChoiceField(queryset=LicenceVariations.objects.none())

    class Meta:
        model = OrderItem
        fields = ['licence_variation']

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id')
        product = Product.objects.get(id=product_id)
        super().__init__(*args, **kwargs)

        self.fields['licence_variation'].queryset = product.licence_variation.all()
