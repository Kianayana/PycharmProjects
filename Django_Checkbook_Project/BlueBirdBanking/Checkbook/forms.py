from django.forms import ModelForm
from .models import Account, Transaction

#Create Accunt Form based on Account Model
class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = '__all__'

#Creates Transaction Form based on Transaction Model
class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'