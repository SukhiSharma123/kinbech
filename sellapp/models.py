from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.template.defaultfilters import slugify


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    def __unicode__(self):
    	return str(self.id)

CATEGORY = (
    ("Mobile", "Mobile"),
    ("Bike", "Bike"),
    ("Cycle", "Cycle"),
    ("Electronics", "Electronics"),
    ("Furnitures", "Furnitures"),
)

class Post(models.Model):
	title=models.CharField(max_length=200)
	image=models.ImageField(upload_to='Post')
	phone=models.PositiveIntegerField()
	category = models.CharField(max_length=20, choices=CATEGORY)
	address= models.CharField(max_length=20)
	description=models.TextField()
	slug = models.SlugField(max_length=150, unique=True)
	price = models.DecimalField(decimal_places=2, max_digits=10)
	date=models.DateTimeField(auto_now_add=True)
	author=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="post")

	def __unicode__(self):
		return str(self.id)

	def save(self, *args, **kwargs):
		super(Post, self).save(*args, **kwargs)
		if not self.slug:
			self.slug = slugify(self.id)
			self.save()

class PostImage(models.Model):
    product = models.ForeignKey(Post, on_delete=models.CASCADE)
    images = models.FileField(upload_to="posts/images/", blank=True, null=True)

    def __str__(self):
        return self.product.title

class Comment(models.Model):
	comment=models.TextField()
	post=models.ForeignKey(Post,on_delete=models.CASCADE, verbose_name="commentpost")      #or cascade ko sata ma DO_NOTHING lekhna sakxa or SET_NULL pani rakhna sakxau
	date=models.DateTimeField(auto_now_add=True)
	commented_by=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="comment")

	def __str__(self):
		return str(self.pk)

	
