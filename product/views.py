from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from product.forms import ProductForm, VersionForm, ProductModeratorForm
from product.models import Product, Version


class ProductListView(ListView):
    """Класс-контроллер для вывода главной страницы"""
    model = Product
    
    def get_context_data(self, **kwargs):
        """Метод для вывода названия версии если она активна"""
        context_data = super().get_context_data(**kwargs)
        version_data = {}
        for product in Product.objects.all():
            for version in Version.objects.all():
                if version.current_version_indicator:
                    if version.product_id == int(product.pk):
                        version_data[version.product_id] = version.version_name
        context_data['version'] = version_data
        return context_data


class ProductDetailView(DetailView, LoginRequiredMixin):
    """Класс-контроллер для вывода информации об отдельном продукте"""
    model = Product
    
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.views += 1
            self.object.save()
            return self.object
        raise PermissionDenied


class ProductCreateView(CreateView, LoginRequiredMixin):
    """Класс-контроллер для создания нового продукта"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product:product_list')
    
    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
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
    
    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm('product.can_cancel_publication_product') and user.has_perm(
                'product.can_change_description_product') and user.has_perm('product.can_change_category_product'):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(DeleteView):
    """Класс-контроллер для удаления продукта"""
    model = Product
    success_url = reverse_lazy('product:product_list')
