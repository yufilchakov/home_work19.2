from django.forms import inlineformset_factory
from django.utils.text import slugify
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from product.forms import ProductForm, VersionForm
from product.models import Product, Version


class ProductListView(ListView):
    """Класс-контроллер для вывода главной страницы"""
    model = Product
    

class ProductDetailView(DetailView):
    """Класс-контроллер для вывода информации об отдельном продукте"""
    model = Product
    
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class ProductCreateView(CreateView):
    """Класс-контроллер для создания нового продукта"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product:product_list')
    
    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.name)
            new_blog.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    """Класс-контроллер для редактирования продукта"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product:product_list')
    
    def get_success_url(self):
        return reverse('product:product_detail', args=[self.kwargs.get('pk')])
    
    def get_context_data(self, **kwargs):
        """Метод для вывода формы версии при редактировании продукта"""
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data
    
    def form_valid(self, form):
        """Метод для сохранения формы при редактировании"""
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductDeleteView(DeleteView):
    """Класс-контроллер для удаления продукта"""
    model = Product
    success_url = reverse_lazy('product:product_list')
