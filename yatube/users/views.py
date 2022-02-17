from django.views.generic import CreateView
from django.shortcuts import render, redirect
# Функция reverse_lazy позволяет получить URL по параметрам функции path()
from django.urls import reverse_lazy
# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm, ContactForm
from .models import Contact


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


def user_contact(request):
    # Запрашиваем объект модели Contact
    contact = Contact.objects.get(pk=3)
    if request.method == 'POST':
        # Создаём объект формы класса ContactForm
        # и передаём в него полученные данные
        form = ContactForm(instance=contact)
        
        # Если все данные формы валидны - работаем с "очищенными данными" формы
        if form.is_valid():
            # Берём валидированные данные формы из словаря form.cleaned_data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['body']
            # При необходимости обрабатываем данные
            # ...
            # сохраняем объект в базу
            form.save()
            
            # Функция redirect перенаправляет пользователя
            # на другую страницу сайта, чтобы защититься
            # от повторного заполнения формы
            return redirect('/thank-you/')
        return render(request, 'users/contact.html', {'form': form})
    
    form = ContactForm()
    return render(request, 'users/contact.html', {'form': form})
