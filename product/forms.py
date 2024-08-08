from django.forms import ModelForm, BooleanField, forms
from django.core.exceptions import ValidationError

from product.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'
                

class ProductForm(StyleFormMixin, ModelForm):
    """Класс форма для продуктов"""
    class Meta:
        model = Product
        exclude = ('views',)

        
class VersionForm(StyleFormMixin, ModelForm):
    """Класс форма для версий"""
    class Meta:
        model = Version
        fields = '__all__'
        
    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        forbidden_words = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар')
        if cleaned_data in forbidden_words:
            raise forms.ValidationError('Название не должно содержать запрещенные слова')
        return cleaned_data
    
    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        forbidden_words = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар')
        if cleaned_data in forbidden_words:
            raise forms.ValidationError('Описание не должно содержать запрещенные слова')
        return cleaned_data
        