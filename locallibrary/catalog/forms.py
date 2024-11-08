from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.

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