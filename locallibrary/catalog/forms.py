from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.

from catalog.models import Author, Book


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Введите дату между текущим моментом и через 8 недель (по умолчанию 3).", label="Обновлённая дата:")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Проверка того, что дата не выходит за "нижнюю" границу (не в прошлом).
        if data < datetime.date.today():
            raise ValidationError(_('Неверная дата - значение в прошлом'))

        #Проверка того, то дата не выходит за "верхнюю" границу (+8 недель).
        if data > datetime.date.today() + datetime.timedelta(weeks=8):
            raise ValidationError(_('Неверная дата - значение более чем через 8 недель.'))

        # Помните, что всегда надо возвращать "очищенные" данные.
        return data

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
        labels = {
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'date_of_birth': _('Дата рождения'),
            'date_of_death': _('Дата смерти'),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'summary', 'isbn', 'genre')
        labels = {
            'title': _('Название'),
            'author': _('Автор'),
            'summary': _('Краткое описание'),
            'isbn': _('ISBN'),
            'genre': _('Жанр'),
        }
        help_texts = {
            'summary': _('Введите краткое описание книги'),
            'isbn': _('<a href="https://www.isbn-international.org/content/what-isbn">Номер ISBN</a> из 13 символов'),
            'genre': _('Выберите жанр для книги'),
        }