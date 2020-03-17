# from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


# class CustomSignupForm(SignupForm):
#     def signup(self, request, user):
#         user.save()
#         userprofile, created = self.get_or_create(user=user)
#         user.userprofile.save()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name']


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # magic
        self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        self.uf = UserForm(*args, **user_kwargs)
        # magic end

        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields.update(self.uf.fields)
        self.initial.update(self.uf.initial)

        self.fields['first_name'] = forms.CharField(
            required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter your first name...'})
        )
        self.fields['first_name'].widget.attrs.update({
            'id': 'profile_first_name',
            'maxlength': 15,
            'pattern': "^[A-Za-z.,\- ]{1,}$",
        })
        self.fields['last_name'] = forms.CharField(
            required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter your last name...'})
        )
        self.fields['last_name'].widget.attrs.update({
            'id': 'profile_last_name',
            'maxlength': 20,
            'pattern': "^[A-Za-z.,\- ]{1,}$"
        })
        self.fields['about'] = forms.CharField(
            required=False, max_length=250, widget=forms.Textarea(attrs={'rows': 2, 'cols': 2, 'placeholder': 'Enter more about you...'})
        )
        # Help Texts
        self.fields['first_name'].help_text = "Maximum length 15 and only these 'A-Za-z.,-' characters and spaces are allowed."
        self.fields['last_name'].help_text = "Maximum length 20 and only these 'A-Za-z.,-' characters and spaces are allowed."
        self.fields['gender'].help_text = 'Enter your Gender.'
        self.fields['blood_group'].help_text = 'Select your Blood Group.'
        self.fields['about'].help_text = 'Enter More About You.'

    class Meta:
        model = UserProfile
        fields = ['about', 'blood_group', 'gender']
        # fields = ['gender', 'blood_group', 'about']

    # def clean_first_name(self):
    #     first_name = self.cleaned_data.get("first_name")
    #     if first_name != "":
    #         allowed_char = re.match(r'^[A-Za-z-., ]+$', first_name)
    #         length = len(first_name)
    #         if length > 15:
    #             raise forms.ValidationError("Maximum 15 characters allowed !")
    #         if not allowed_char:
    #             raise forms.ValidationError(
    #                 "Only 'A-Za-z.,-' these characters and spaces are allowed.")
    #     return first_name

    # def clean_last_name(self):
    #     last_name = self.cleaned_data.get("last_name")
    #     if last_name != "":
    #         allowed_char = re.match(r'^[A-Za-z-., ]+$', last_name)
    #         length = len(last_name)
    #         if length > 20:
    #             raise forms.ValidationError("Maximum 20 characters allowed !")
    #         if not allowed_char:
    #             raise forms.ValidationError(
    #                 "Only 'A-Za-z.,-' these characters and spaces are allowed.")
    #     return last_name


    # def clean_about(self):
    #     about = self.cleaned_data.get('about')
    #     if not about == None:
    #         length = len(about)
    #         if length > 250:
    #             raise forms.ValidationError("Maximum 250 characters allowed !")
    #     return about

    def save(self, *args, **kwargs):
        self.uf.save(*args, **kwargs)
        return super(UserProfileForm, self).save(*args, **kwargs)



class BaseUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'blood_group', 'gender']



class BaseUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # magic
        self.uf = BaseUserProfileForm(*args, **kwargs)
        # magic end

        super(BaseUserForm, self).__init__(*args, **kwargs)

        self.fields.update(self.uf.fields)
        # self.initial.update(self.uf.initial)

        self.fields['first_name'] = forms.CharField(
            required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter your first name...'})
        )
        self.fields['first_name'].widget.attrs.update({
            'id': 'profile_first_name',
            'maxlength': 15,
            'pattern': "^[A-Za-z.,\- ]{1,}$",
        })
        self.fields['last_name'] = forms.CharField(
            required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter your last name...'})
        )
        self.fields['last_name'].widget.attrs.update({
            'id': 'profile_last_name',
            'maxlength': 20,
            'pattern': "^[A-Za-z.,\- ]{1,}$"
        })
        self.fields['email'] = forms.EmailField(
            required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your email...'})
        )
        self.fields['password'] = forms.CharField(
            required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password...'})
        )
        # Help Texts
        self.fields['first_name'].help_text = "Maximum length 15 and only these 'A-Za-z.,-' characters and spaces are allowed."
        self.fields['last_name'].help_text = "Maximum length 20 and only these 'A-Za-z.,-' characters and spaces are allowed."
        self.fields['gender'].help_text = 'Enter your Gender.'
        self.fields['blood_group'].help_text = 'Select your Blood Group.'


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class AdminUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role']