from django import forms
from django.contrib import admin
from .models import UserProfile
from TestAPI.validators import CustomPasswordValidator

# Register your models here.

# admin.site.register(UserProfile)

class UserProfileAdminForm(forms.ModelForm):
    
    # password = forms.CharField(
    #     label="Password",
    #     widget=forms.PasswordInput,
    #     help_text="Your password must be at least 8 characters long, contain at least one letter and one number.",
    # )

    class Meta:
        model = UserProfile
        fields = '__all__'
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            validator = CustomPasswordValidator()
            validator.validate(password)  # Validate the password
        return password
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileAdminForm
    # def get_readonly_fields(self, request, obj=None):
    #     return ['password']
    list_display = ('email', 'first_name', 'last_name', 'is_superuser')
    search_fields = ('email',)
admin.site.register(UserProfile, UserProfileAdmin)
