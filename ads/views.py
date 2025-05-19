from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from models.models import Advertisement, ExchangeProposal
from ads.forms import AdForm, ProposalForm
from django.urls import reverse_lazy


class AdListView(ListView):
    model = Advertisement
    template_name = 'ads/list.html'
    context_object_name = 'ads'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        category = self.request.GET.get('category')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        if category:
            queryset = queryset.filter(category=category)

        return queryset


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdForm
    template_name = 'ads/create.html'
    success_url = reverse_lazy('ads:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdDetailView(DetailView):
    model = Advertisement
    template_name = 'ads/detail.html'
    context_object_name = 'ad'


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Advertisement
    form_class = AdForm
    template_name = "ads/edit.html"
    success_url = reverse_lazy('ads:list')

    def test_func(self):
        return self.get_object().user == self.request.user


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Advertisement
    template_name = "ads/delete.html"
    success_url = reverse_lazy("ads:list")

    def test_func(self):
        return self.get_object().user == self.request.user

