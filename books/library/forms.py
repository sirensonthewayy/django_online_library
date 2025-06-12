from django import forms
from .models import Order, Feedback, Review

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email']
        labels = {'email': 'Электронная почта'}
        widgets = {
            'email': forms.EmailInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                'title': 'Введите корректный email'
            })
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'
        labels = {
            'name': 'Имя',
            'email': 'Электронная почта',
            'subject': 'Тема',
            'message': 'Сообщение',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                'title': 'Введите корректный email'
            }),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        labels = {
            'text': 'Отзыв',
            'rating': 'Оценка (от 1 до 5)',
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }