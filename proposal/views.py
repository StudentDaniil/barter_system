from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from models.models import ExchangeProposal
from ads.forms import ProposalForm
from django.urls import reverse_lazy


class ProposalListView(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    template_name = 'proposals/list.html'
    context_object_name = 'proposals'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return ExchangeProposal.objects.filter(
            ad_sender__user=user
        ).distinct().order_by('-created_at')


class ProposalDetailView(LoginRequiredMixin, DetailView):
    model = ExchangeProposal
    template_name = 'proposals/detail.html'
    context_object_name = 'proposal'

    def get_queryset(self):
        user = self.request.user
        return ExchangeProposal.objects.filter(
            ad_sender__user=user
        ) | ExchangeProposal.objects.filter(
            ad_receiver__user=user
        )


class ProposalCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ProposalForm
    template_name = 'proposals/create.html'
    success_url = reverse_lazy('proposals:list')

    def form_valid(self, form):
        # проверяем, что текущий пользователь – владелец ad_sender
        if form.cleaned_data['ad_sender'].user != self.request.user:
            form.add_error('ad_sender', 'Вы не владелец этого объявления')
            return self.form_invalid(form)
        return super().form_valid(form)


class ProposalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ExchangeProposal
    form_class = ProposalForm
    template_name = 'proposals/edit.html'
    context_object_name = 'proposal'
    success_url = reverse_lazy('proposals:list')

    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        return user in (obj.ad_sender.user, obj.ad_receiver.user)

    def form_valid(self, form):
        if 'ad_sender' in form.changed_data or 'ad_receiver' in form.changed_data:
            form.add_error(None, 'Нельзя менять объявления в предложении')
            return self.form_invalid(form)
        return super().form_valid(form)


class ProposalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ExchangeProposal
    template_name = 'proposals/delete.html'
    success_url = reverse_lazy('proposals:list')

    def test_func(self):
        return self.get_object().ad_sender.user == self.request.user
