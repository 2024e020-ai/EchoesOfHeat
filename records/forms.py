from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Record

# サウナ記録用のフォーム
class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['sauna_name', 'sauna_time', 'water_time', 'rest_time', 'comment']
        labels = {
            'sauna_name': '施設名',
            'sauna_time': 'サウナ (分)',
            'water_time': '水風呂 (秒)',
            'rest_time': '休憩 (分)',
            'comment': '魂の独白 (コメント)',
        }
        widgets = {
            'sauna_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例：北投の湯'}),
            'sauna_time': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'water_time': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'rest_time': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '感想や整い具合をここに...'}),
        }

# ユーザー登録用のフォーム
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")
        labels = {
            'username': 'ユーザー名',
            'email': 'メールアドレス（任意）',
        }