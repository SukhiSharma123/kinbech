from django.shortcuts import reverse ,redirect
from django.views.generic import * #TemplateView,ListView,DetailView,CreateView,UpdateView
from .models import Post, Comment
from .forms import *
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import update_session_auth_hash

class HomeView(TemplateView):
	template_name = 'home.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs) 
		posts = Post.objects.all()
		context['posts'] = posts
		print(posts)
		return context
class AllprView(TemplateView):
    template_name = "kux.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Post.objects.all().order_by("-id")
        paginator = Paginator(all_products, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context

class BlogCreateForm(CreateView):
	template_name = "blogcreate.html"
	model = Post
	form_class = BlogCreateForm

	def form_valid(self, form):
		# messages.success(self.request, 'form is valid')
		form.instance.author = self.request.user
		form.save()
		return redirect(self.get_success_url())

	def get_success_url(self):
		return reverse('sellapp:home')


class BloglistView(LoginRequiredMixin, ListView):
	template_name = 'bloglist.html'
	queryset = Post.objects.all().order_by('-id')
	context_object_name = 'postlist'

	def dispatch(self,request):
		if not request.user.is_authenticated:
			return redirect('sellapp:login')
		return super().dispatch(request)



class SignupFormView(FormView):
	template_name='signupform.html'
	form_class= SignupForm
	success_url=reverse_lazy('sellapp:login')

	def form_valid(self,form):
		u_name=form.cleaned_data['username']
		e_mail=form.cleaned_data['email']
		p_word=form.cleaned_data['password']
		cp_word=form.cleaned_data['confirm_password']
		if p_word==cp_word:
			if User.objects.filter(username=u_name):
				return render(self.request,self.template_name,{
				'form':form,
				'error':"Username is already taken"})
			else:
				User.objects.create_user(username=u_name,email=e_mail,password=p_word)
		else:
			return render(self.request,self.template_name,{
				'form':form,
				'error':"Password do not match"})
		messages.success(self.request, 'Successfully signed in')
		return super().form_valid(form)

#

class LoginFormView(FormView):
	template_name='login.html'
	form_class=LoginForm
	success_url=reverse_lazy('sellapp:home')

	def get(self,request):
		if request.user.is_authenticated:
			return redirect('sellapp:home')
		return super().get(request)

	def form_valid(self,form):
		u_name=form.cleaned_data['username']
		p_word=form.cleaned_data['password']
		user=authenticate(username=u_name,password=p_word)
		if user is not None:
			login(self.request,user)
		else:
			return render(self.request,self.template_name,{'form':form,'error':"Invalid Candential"})
		messages.success(self.request, 'Welcome')
		return super().form_valid(form)

	def get_success_url(self,**kwargs):
		self.next_url=self.request.POST.get('next')
		if self.next_url is not None:
			return self.next_url
		else:
			return self.success_url


# class LoginFormView(FormView):
#     template_name = "login.html"
#     form_class = LoginForm
#     success_url = reverse_lazy("sellapp:home")

#     # form_valid method is a type of post method and is available in createview formview and updateview
#     def form_valid(self, form):
#         uname = form.cleaned_data.get("username")
#         pword = form.cleaned_data["password"]
#         usr = authenticate(username=uname, password=pword)
#         if usr is not None and Customer.objects.filter(user=usr).exists():
#             login(self.request, usr)
#             messages.success(self.request, 'Welcome')
#         else:
#             messages.success(self.request, 'Invalid')
#             return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})

#         return super().form_valid(form)

#     def get_success_url(self):
#         if "next" in self.request.GET:
#             next_url = self.request.GET.get("next")
#             return next_url
#         else:
#             return self.success_url


class LogoutView(View):
	def get(self,request):
		logout(request)
		messages.success(self.request, 'You are Logged out')
		return redirect('sellapp:home')

class BlogDetailView(DetailView):
	template_name = 'blogdetail.html'
	model = Post
	context_object_name = 'postdetail'

class MobileViewed(TemplateView):
    template_name = "mobileviewed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = Post.objects.raw('SELECT * FROM sellapp_post WHERE category ="Mobile"')
        paginator = Paginator(results, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context

class BikeViewed(TemplateView):
    template_name = "bikeviewed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = Post.objects.raw('SELECT * FROM sellapp_post WHERE category ="Bike"')
        paginator = Paginator(results, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context

class CycleViewed(TemplateView):
    template_name = "cycleviewed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = Post.objects.raw('SELECT * FROM sellapp_post WHERE category ="Cycle"')
        paginator = Paginator(results, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context

class FridgeViewed(TemplateView):
    template_name = "fridgeviewed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = Post.objects.raw('SELECT * FROM sellapp_post WHERE category ="Fridge"')
        paginator = Paginator(results, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Post.objects.filter(Q(title__icontains=kw) | Q(description__icontains=kw) | Q(price__icontains=kw) | Q(address__icontains=kw) | Q(category__icontains=kw))
        context['results'] = results
        return context

def MinmaxPrice(request):
    if request.method=="POST":
        minprice = request.POST.get('minprice')
        maxprice = request.POST.get('maxprice')
        resultobj = Post.objects.raw('SELECT * From sellapp_post WHERE price between "'+minprice+'" and "'+maxprice+'"')
        return render(request, 'pricerange.html', {"data":resultobj})
    else:
        pricera = Post.objects.all()
        return render(request, 'pricerange.html', {"data":pricera})

class ProfileView(TemplateView):
	template_name = "profile.html"


def changepPass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            v = form.save()
            update_session_auth_hash(request, v)
            messages.success(request, 'Password Changed!!')
            return redirect('sellapp:home')
    else:
        form = PasswordChangeForm(request.user)
    params = {
        'form':form,
    }
    return render(request, 'changepass.html', params)

class MypostView(TemplateView):
	template_name = "mypost.html"

	def get(self,request,*args,**kwargs):
		context = super().get_context_data(**kwargs)
		current_user = request.user
		a_id = current_user.id
		context["results"] = Post.objects.filter(author_id=a_id)
		# return JsonResponse({'success':False, 'results':results})
		# return context
		return render(request, 'mypost.html', context)


class BlogUpdateView(UpdateView):
	template_name = 'blogupdate.html'
	model= Post
	form_class = BlogUpdateForm
	success_url= '/mypost/'


class BlogDeleteView(DeleteView):
	template_name = 'blogdelete.html'
	model= Post
	success_url= reverse_lazy("sellapp:mypost")


class LowToHigh(TemplateView):
    template_name = "lowtohigh.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = Post.objects.raw('SELECT * FROM sellapp_post ORDER BY price ASC')
        paginator = Paginator(results, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context


class HighToLow(TemplateView):
    template_name = "hightolow.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = Post.objects.raw('SELECT * FROM sellapp_post ORDER BY price DESC')
        paginator = Paginator(results, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context

# Create your views here.
