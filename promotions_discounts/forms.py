from django import forms
from .models import Shop

class FavoriteShopForm(forms.Form):
    favorite_shops = forms.ModelMultipleChoiceField(
        queryset=Shop.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,  # Tidak wajib karena pengguna bisa memilih atau tidak
        label="Filter by Shops"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the label for each choice to the shop name
        self.fields['favorite_shops'].label_from_instance = lambda obj: obj.name
