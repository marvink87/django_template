from django.shortcuts import render
from django.apps import apps
from django.core.paginator import Paginator
from django.views import View
from django.http import Http404
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.db.models.fields.reverse_related import ManyToOneRel
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import get_default_form


class ModelAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Generic view that handles adding entries to models
    model_name must be specified in URL dispatcher
    """
    template_name = 'modelviewer/model_create.html'

    def dispatch(self, request, *args, **kwargs):
        self.app_name = self.request.resolver_match.app_name
        try:
            self.model = apps.get_model(self.app_name, self.kwargs['model_name'])
        except LookupError:
            raise Http404(f"Could not find table: {self.kwargs['model_name']}")
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        model_name = self.kwargs['model_name'].lower()
        return self.request.user.has_perm(f'{self.app_name}.add_{model_name}')

    def get_form_class(self):
        try:
            return get_default_form(self.model)
        except LookupError:
            raise Http404(f"Could not find model: {self.app_name}:{self.kwargs['model_name']}")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        model_name = self.kwargs['model_name']
        ctx['title'] = f'Add to {model_name}'
        return ctx

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            model_name = self.kwargs['model_name']
            return f'/{self.app_name}/list/{model_name}'


class ModelUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'modelviewer/model_update.html'

    def dispatch(self, request, *args, **kwargs):
        self.app_name = self.request.resolver_match.app_name
        try:
            self.model = apps.get_model(self.app_name, self.kwargs['model_name'])
        except LookupError:
            raise Http404(f"Could not find table: {self.kwargs['model_name']}")
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        model_name = self.kwargs['model_name'].lower()
        return self.request.user.has_perm(f'{self.app_name}.change_{model_name}')

    def get_queryset(self):
        return self.model.objects.filter(pk=self.kwargs['pk'])

    def get_form_class(self):
        try:
            return get_default_form(self.model)
        except LookupError:
            raise Http404(f"Could not find model: {self.app_name}:{self.kwargs['model_name']}")

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            model_name = self.kwargs['model_name']
            return f'/{self.app_name}/list/{model_name}'


class ModelDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'modelviewer/model_delete.html'

    def dispatch(self, request, *args, **kwargs):
        self.app_name = self.request.resolver_match.app_name
        try:
            self.model = apps.get_model(self.app_name, self.kwargs['model_name'])
        except LookupError:
            raise Http404(f"Could not find table: {self.kwargs['model_name']}")
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        model_name = self.kwargs['model_name'].lower()
        return self.request.user.has_perm(f'{self.app_name}.delete_{model_name}')

    def get_queryset(self):
        return self.model.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        model_name = self.kwargs['model_name']
        ctx['title'] = f'Delete {self.object} from {model_name}'
        return ctx

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            model_name = self.kwargs['model_name']
            return f'/{self.app_name}/list/{model_name}'


class ModelListView(LoginRequiredMixin, UserPassesTestMixin, View):

    def dispatch(self, request, *args, **kwargs):
        self.app_name = self.request.resolver_match.app_name
        try:
            self.model = apps.get_model(self.app_name, self.kwargs['model_name'])
        except LookupError:
            raise Http404(f"Could not find table: {self.kwargs['model_name']}")
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        model_name = self.kwargs['model_name'].lower()
        return self.request.user.has_perm(f'{self.app_name}.view_{model_name}')

    def get(self, request, model_name):
        model_objects = self.model.objects.all()

        # Paginate results
        paginator = Paginator(model_objects, 5)
        page = request.GET.get('page')
        model_page = paginator.get_page(page)

        # Get fields
        fields = [
            field
            for field in self.model._meta.fields
            if type(field) is not ManyToOneRel
        ]

        args = {
            'app_name': self.app_name,
            'model_name': model_name,
            'model': model_page,
            'fields': fields,
        }
        return render(request, 'modelviewer/model_list.html', args)
