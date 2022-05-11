from django import forms

from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            print('User Does Not Exist')
            raise forms.ValidationError("Not registered yet? It takes a few seconds, please do!")
        return username

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user is not None and not user.check_password(password):
            raise forms.ValidationError("Wrong password. Try again.")
        elif user is None:
            pass
        else:
            return password


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Your Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email']


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password2 and password1 and password2 != password1:
            raise forms.ValidationError("Passwords do not match")
        else:
            return password2


    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_with_same_emails_count = User.objects.filter(email=email).count()
        print('SAME EMAILS:', user_with_same_emails_count)
        if user_with_same_emails_count > 0:
            raise forms.ValidationError("This Email is alredy in use")
        return email


    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False) #???? ШО ЭТО БЛЯДЬ ТАКОЕ
        user.set_password(self.cleaned_data['password1'])          #LESSON 44
        if commit:                                                         #УСТАНАВЛИВАЕТ ПАРОЛЬ?
            user.save()
        return user