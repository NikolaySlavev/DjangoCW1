from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
	name = models.CharField('Author Name', max_length=120)
	username = models.ForeignKey(User, on_delete = models.CASCADE)
	passowrd = models.CharField('Password', max_length=120) #secret

	def __str__(self):
		return self.username.username
		

STORY_CATEGORY_CHOICES = (
    ('POL', 'Politics'),
    ('ART', 'Art'),
    ('TECH', 'Technology'),
    ('TRIVIA', 'Trivial')
)

STORY_REGION_CHOICES = (
    ('UK', 'United Kingdom News'),
    ('EU', 'European News'),
    ('W', 'World News')
)
		
class NewsStory(models.Model):
	headline = models.CharField('Headline', max_length=64)
	category = models.CharField('Category', choices = STORY_CATEGORY_CHOICES, max_length = 6)
	region = models.CharField('Region', choices = STORY_REGION_CHOICES, max_length = 2)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	date = models.DateTimeField('Date')
	details = models.CharField('Details', max_length=512)
	
	def __str__(self):
		return self.headline + ' on ' + self.date.strftime('%m/%d/%Y') + ' region = ' + self.region + ' category = ' + self.category
		
	def publish(self):
		self.date = timezone.now()
		self.save()
