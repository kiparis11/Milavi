from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order

        fields = (
            'full_name',
            'phone',
            'address',
            'comment',
            'payment_method',
        )

        labels = {
            'full_name': 'Имя получателя',
            'phone': 'Номер телефона',
            'address': 'Адрес доставки',
            'comment': 'Комментарий к заказу',
        }

        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Как к вам обращаться?'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'placeholder': '+998 XX XXX XX XX'
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'placeholder': 'Улица, дом, квартира',
                    'rows': 3,
                }
            ),

            'comment': forms.Textarea(
                attrs={
                    'placeholder': 'Пожелания к заказу (необязательно)',
                    'rows': 3,
                }
            ),

            'payment_method': forms.RadioSelect(),
        }