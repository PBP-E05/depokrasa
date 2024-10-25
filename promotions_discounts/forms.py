from django import forms
from .models import Shop, UserFavoriteShop

class FavoriteShopForm(forms.Form):
    favorite_shops = forms.ModelMultipleChoiceField(
        queryset=Shop.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Your Favorite Shops"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the label for each choice to the shop name
        self.fields['favorite_shops'].label_from_instance = lambda obj: obj.name

    def save(self, user):
        # Clear previous favorites
        UserFavoriteShop.objects.filter(user=user).delete()

        # Save each selected favorite shop
        for shop in self.cleaned_data['favorite_shops']:
            UserFavoriteShop.objects.create(user=user, shop=shop)
