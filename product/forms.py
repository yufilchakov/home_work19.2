from django.forms import ModelForm, BooleanField, forms, BaseInlineFormSet

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


class VersionForm(StyleFormMixin, ModelForm):
    """Класс форма для версий"""
    
    class Meta:
        model = Version
        fields = '__all__'
        
        
class VersionFormset(StyleFormMixin, BaseInlineFormSet):
    def clean_count(self):
        super().clean()
        count = 0
        for form in self.forms:
            if form.instance.current_version_indicator:
                count += 1
        if count > 1:
            raise forms.ValidationError("Может быть только 1 активная версия")
        return count
    