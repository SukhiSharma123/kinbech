from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import reverse ,redirect
from django.views.generic import * #TemplateView,ListView,DetailView,CreateView,UpdateView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .utils import password_reset_token
from django.core.mail import send_mail
from django.conf import settings
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




class BloglistView(LoginRequiredMixin, ListView):
	template_name = 'bloglist.html'
	queryset = Post.objects.all().order_by('-id')
	context_object_name = 'postlist'

	def dispatch(self,request):
		if not request.user.is_authenticated:
			return redirect('sellapp:login')
		return super().dispatch(request)


class BlogCreateForm(CreateView):
    template_name = "blogcreate.html"
    form_class = BlogCreateForm
    success_url = reverse_lazy("sellapp:home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            PostImage.objects.create(product=p, images=i)
        return super().form_valid(form)

# class CommentCreateForm(CreateView):
#     template_name = "commentcreate.html"
#     form_class = CommentModelForm
#     success_url = reverse_lazy("sellapp:home")

#     def form_valid(self, form):
#         form.instance.commented_by = self.request.user

#         form.save()
#         return super().form_valid(form)
#         # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




class CustomerRegistrationView(CreateView):
    template_name = "customerregistration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("sellapp:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("sellapp:home")


class CustomerLoginView(FormView):
    template_name = "customerlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("sellapp:home")

    # form_valid method is a type of post method and is available in createview formview and updateview
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url





class PasswordForgotView(FormView):
    template_name = "forgotpassword.html"
    form_class = PasswordForgotForm
    success_url = "/forgot-password/?m=s"

    def form_valid(self, form):
        # get email from user
        email = form.cleaned_data.get("email")
        # get current host ip/domain
        url = self.request.META['HTTP_HOST']
        # get customer and then user
        customer = Customer.objects.get(user__email=email)
        user = customer.user
        # send mail to the user with email
        text_content = 'Please Click the link below to reset your password. '
        html_content = url + "/password-reset/" + email + \
            "/" + password_reset_token.make_token(user) + "/"
        send_mail(
            'Password Reset Link | Django Ecommerce',
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)

class PasswordResetView(FormView):
    template_name = "passwordreset.html"
    form_class = PasswordResetForm
    success_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse("sellapp:passworforgot") + "?m=e")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)


class BlogDetailView(CreateView):
    template_name = "blogdetail.html"
    form_class = CommentModelForm
    # success_url = reverse_lazy("sellapp:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_pk = self.kwargs['slug']
        post = Post.objects.get(slug=url_pk)
        comment=Comment.objects.filter(id=url_pk)
        context['post'] = post
        context['comment'] = comment
        return context

    def form_valid(self, form):
        post_id = self.request.POST.get('post_id')
        form.instance.commented_by = self.request.user
        form.instance.post = Post.objects.get(id=post_id)
        form.save()
        # return super().form_valid(form)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        return context

def changepPass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            v = form.save()
            update_session_auth_hash(request, v)
            # messages.success(request, 'Password Changed!!')
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
		context["results"] = Post.objects.filter(author_id=a_id).order_by("-id")
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
