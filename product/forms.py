from django.forms import ModelForm, BooleanField, forms

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
        exclude = ('views', 'owner',)
    
    forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                       'радар']
    
    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        for forbidden_word in self.forbidden_words:
            if forbidden_word in cleaned_data.lower():
                raise forms.ValidationError(f'Название не должно содержать запрещенные слова: {forbidden_word}')
        return cleaned_data
    
    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        for forbidden_word in self.forbidden_words:
            if forbidden_word in cleaned_data.lower():
                raise forms.ValidationError(f'Описание не должно содержать запрещенные слова: {forbidden_word}')
        return cleaned_data


class ProductModeratorForm(StyleFormMixin, ModelForm):
    """Класс форма для модераторов изменение продуктов"""
    
    class Meta:
        model = Product
        fields = ('publication', 'description', 'category')


class VersionForm(StyleFormMixin, ModelForm):
    """Класс форма для версий"""
    
    class Meta:
        model = Version
        fields = '__all__'
    