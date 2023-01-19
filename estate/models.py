from django.db import models
from users.models import User
from django.utils.translation import ugettext_lazy as _


class Buy_Sell_Home(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name=_('Creator User'), null=True, related_name='buy_sell_home_creator'
    )
    area_code = models.CharField(max_length=10, verbose_name=_('Area Code'))
    owner_name = models.CharField(
        max_length=20, verbose_name=_('Owner Name'), null=True, blank=True)
    owner_phone = models.CharField(
        max_length=11, verbose_name=_('Owner Phone'), null=True, blank=True)
    street = models.CharField(
        max_length=50, verbose_name=_('Street'), null=True, blank=True)
    plaque = models.CharField(
        max_length=10, verbose_name=_('Plaque'), null=True, blank=True)
    floors = models.CharField(
        max_length=10, verbose_name=_('Floors'), null=True, blank=True)
    meterage = models.IntegerField(
        default=0, verbose_name=_('Meterage'), null=True, blank=True)
    price_per_meter = models.IntegerField(
        default=0, verbose_name=_('Price Per Meterage'), null=True, blank=True)
    total_price = models.IntegerField(
        default=0, verbose_name=_('Total Price'), null=True, blank=True)
    customer_name = models.CharField(
        max_length=20, verbose_name=_('Customer Name'), null=True, blank=True)
    style = models.CharField(
        max_length=20, verbose_name=_('Style'), null=True, blank=True)
    heating = models.CharField(
        max_length=20, verbose_name=_('Heating'), null=True, blank=True)
    bottom = models.CharField(
        max_length=20, verbose_name=_('Bottom'), null=True, blank=True)
    electricity = models.CharField(
        max_length=20, verbose_name=_('Electricity'), null=True, blank=True)
    kitchen = models.CharField(
        max_length=20, verbose_name=_('Kitchen'), null=True, blank=True)
    faucets = models.CharField(
        max_length=20, verbose_name=_('Faucets'), null=True, blank=True)
    bathtub = models.CharField(
        max_length=20, verbose_name=_('Bathtub'), null=True, blank=True)
    window = models.CharField(
        max_length=20, verbose_name=_('Window'), null=True, blank=True)
    description = models.TextField(
        verbose_name=_('Description'), null=True, blank=True)
    status = models.BooleanField(default=False, verbose_name=_('Status Home'))
    is_archived = models.BooleanField(
        default=False, verbose_name=_('Is Archived'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    checked_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name=_('Accepted By'), null=True, blank=True, related_name='buy_sell_home_accepted_by'
    )
    checked_date = models.DateTimeField(
        verbose_name=_('Accepted Date'), null=True, blank=True
    )

    def __str__(self) -> str:
        return self.creator.username


class Home_History(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name=_('User'), null=True, related_name='home_history_user'
    )
    home = models.ForeignKey(
        Buy_Sell_Home, on_delete=models.SET_NULL, verbose_name=_('Buy-Sell-Home'), null=True, related_name='home_history_home'
    )
    title = models.CharField(max_length=50, null=True, blank=True)
    descriptions = models.TextField(verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now=True)
