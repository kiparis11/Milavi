from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review

        fields = (
            'rating',
            'text',
        )

        labels = {
            'rating': 'Оценка',
            'text': 'Ваш отзыв',
        }

        widgets = {
            'rating': forms.Select(
                attrs={
                    'class': 'review-form__select'
                }
            ),

            'text': forms.Textarea(
                attrs={
                    'class': 'review-form__textarea',
                    'placeholder': 'Расскажите, что вам понравилось...',
                    'rows': 5,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['rating'].choices = [
            ('', 'Выберите оценку'),
            *Review.RATING_CHOICES,
        ]