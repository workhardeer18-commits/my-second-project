from django import forms
from .models import Ticket, Conversation, User # مطمئن شو User رو ایمپورت کردی

class UserRegistrationForm(forms.ModelForm):
    # اضافه کردن فیلد پسورد به صورت دستی برای امنیت بیشتر
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'text']

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['message']
