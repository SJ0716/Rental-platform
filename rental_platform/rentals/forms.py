from django import forms
from .models import Item, RentalRequest

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'image', 'is_available', 'deposit', 'daily_cost', 'weekly_cost']
        labels = {
            'title': '상품명',
            'description': '상품 설명',
            'image': '상품 이미지',
            'is_available': '대여 가능 여부',
            'deposit': '보증금',
            'daily_cost': '일 단위 비용',
            'weekly_cost': '주 단위 비용',
        }
        widgets = {
            'deposit': forms.NumberInput(attrs={'placeholder': '보증금 (원)'}),
            'daily_cost': forms.NumberInput(attrs={'placeholder': '일 단위 비용 (원)'}),
            'weekly_cost': forms.NumberInput(attrs={'placeholder': '주 단위 비용 (원)'}),
        }


class RentalRequestForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # HTML5 날짜 선택 위젯
        input_formats=['%Y-%m-%d']  # 허용되는 날짜 형식
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = RentalRequest
        fields = ['start_date', 'end_date']
        labels = {
            'start_date': '대여 시작일',
            'end_date': '대여 종료일',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
