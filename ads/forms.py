from django import forms
from models.models import Advertisement, ExchangeProposal


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class AdForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
        }


class ProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment', 'status']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'status': forms.Select(),
        }
