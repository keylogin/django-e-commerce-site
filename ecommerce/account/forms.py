# account/forms.py

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
# Note: Ensure you have imported the User model if you reference it elsewhere,
# but for this specific form, only UserCreationForm and forms are necessary.

class CustomUserCreationForm(UserCreationForm):
    
    # 💡 FIX: Explicitly define password fields using string labels
    
    password1 = forms.CharField(
        # Removed the error-causing line UserCreationForm.base_fields['password'].label
        label='Password', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Password (minimum 8 characters)' 
        })
    )
    
    password2 = forms.CharField(
        # Removed the error-causing line UserCreationForm.base_fields['password'].label
        label='Password confirmation', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Confirm Password' 
        })
    )

    class Meta(UserCreationForm.Meta):
        
        model = UserCreationForm.Meta.model 
        fields = ('username', 'password1', 'password2') 
        
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Username (words, numbers, @/./+/-/_)' 
            }),
            # The widgets for password fields are now handled by the explicit definitions above.
        }
        
class UserLoginForm(AuthenticationForm):
    
    # Redefine username field to add placeholder and styling
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Username' 
        })
    )
    
    # Redefine password field to add placeholder and styling
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )