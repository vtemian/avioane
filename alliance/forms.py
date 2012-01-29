from django import forms
from django.forms.models import ModelForm
from alliance.models import Alliance, AllianceNews

class ClanCreate(forms.Form):
    name = forms.CharField(max_length=50)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Alliance.objects.filter(name=name).exists():
            raise forms.ValidationError('Try a different name!')
        return name

class UploadAvatar(ModelForm):
    class Meta:
        model = Alliance
        fields = ('avatar',)

class NewsCreate(ModelForm):
    class Meta:
        model = AllianceNews
        fields = ('text', 'title')

class ClanChangeName(ModelForm):
    class Meta:
        model = Alliance
        fields = ('name',)