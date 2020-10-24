from django import forms
from .models import *
from django.contrib.auth.models import User



class BlogCreateForm(forms.ModelForm):
	
	class Meta:
		model = Post
		fields= ['title','image','phone','category','address','price','description']

class BlogUpdateForm(forms.ModelForm):
	
	class Meta:
		model = Post
		fields= ['title','image','phone','category','address','price','description']


class SignupForm(forms.Form):
	username=forms.CharField(widget=forms.TextInput())
	email=forms.CharField(widget=forms.TextInput())
	password=forms.CharField(widget=forms.PasswordInput())
	confirm_password=forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = Customer
		fields = ["username", "password", "email", "full_name", "address"]

		
		def clean_username(self):
			uname = self.cleaned_data.get("username")
			if User.objects.filter(username=uname).exists():
				raise forms.ValidationError(
                	"Customer with this username already exists.")
			return uname
		def clean_email(self):
			umail = self.cleaned_data.get("email")
			if User.objects.filter(email=umail).exists():
				raise forms.ValidationError(
                	"Customer with this email already exists.")
			return umail	

class SendMailForm(forms.Form):
	recepient=forms.EmailField(widget=forms.EmailInput())
	subject=forms.CharField(widget=forms.TextInput())
	message=forms.CharField(widget=forms.Textarea())
class LoginForm(forms.Form):
	username=forms.CharField(widget=forms.TextInput())
	password=forms.CharField(widget=forms.PasswordInput())
	