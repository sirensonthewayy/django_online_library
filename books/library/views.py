from django.shortcuts import get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormMixin, CreateView
from django.views.generic import ListView
from django.core.mail import send_mail, BadHeaderError
from smtplib import SMTPException
from django.conf import settings
from django.contrib import messages

from .models import Book, Feedback, Review
from .forms import ReviewForm, OrderForm, FeedbackForm

@method_decorator(login_required, name='dispatch')
class BookView(FormMixin, DetailView):
    """Книга"""
    model = Book
    template_name = "book.html"
    context_object_name = "book"
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        context['order_form'] = OrderForm()
        context['reviews'] = Review.objects.filter(book=self.object).order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        review_form = ReviewForm()
        order_form = OrderForm()

        if 'submit_review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.book = self.object
                review.user = request.user
                review.save()
                messages.success(request, 'Отзыв успешно добавлен!')
                return redirect(reverse('book', kwargs={'pk': self.object.pk}))
            else:
                messages.error(request, 'Ошибка в форме отзыва.')

        elif 'submit_order' in request.POST:
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order = order_form.save(commit=False)
                order.book = self.object
                order.user = request.user
                order.save()
                messages.success(request, 'Книга успешно заказана!')
                email = order_form.cleaned_data['email']
                try:
                    send_mail(
                        subject="Заказ книги",
                        message=f"Вы заказали книгу '{self.object.title}'. Ссылка на книгу: {self.object.link}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                except (SMTPException, BadHeaderError) as e:
                    messages.error(request, "Ошибка отправки email. Проверьте корректность адреса.")
                return redirect(reverse('book', kwargs={'pk': self.object.pk}))
            else:
                messages.error(request, 'Ошибка в форме заказа.')

        context = self.get_context_data()
        context['review_form'] = review_form
        context['order_form'] = order_form
        return self.render_to_response(context)


class FeedbackView(CreateView):
    """Обратная связь"""
    model = Feedback
    template_name = "feedback.html"
    form_class = FeedbackForm
    success_url = reverse_lazy("feedback")

    def form_valid(self, form):
        response = super().form_valid(form)
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']

        full_message = f"Сообщение от: {name} <{email}>\n\n{message}"
        try:
            send_mail(
                subject=subject,
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.success(self.request, "Сообщение успешно отправлено.")
        except(SMTPException, BadHeaderError):
            messages.error(self.request, "Не удалось отправить сообщение. Попробуйте позже.")

        return super().form_valid(form)

class HomeView(ListView):
    model = Book
    template_name = "home.html"
    context_object_name = "books"