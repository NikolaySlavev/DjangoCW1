from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
from .models import Author, NewsStory
from .forms import PostForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
import json
import datetime


@csrf_exempt
def handle_login(request):
	if request.method == 'POST':
		print(1)
		print(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		data = 'username = ' + username + ', password = ' + password
		user = authenticate(request, username=username, password=password)
	if user is not None:
		print(2)
		if user.is_active:
			print(3)
			login(request, user)
			if (user.is_authenticated):
				print(4)
				print(user.username + ' is logged in')
			return HttpResponse(data)
		else:
			print(5)
			return HttpResponse('disabled account')
	else:
		print(6)
		return HttpResponse('invalid login ' + data)

@csrf_exempt
def handle_logout(request):
	if request.method == 'POST':
		if (request.user.is_authenticated):
			logout(request)
			return HttpResponse("Goodbye")
		else:
			return HttpResponse("User is not logged in")
	else:
		return HttpResponse("Requires a POST request")

		
#def post_list(request):
#	posts = NewsStory.objects.filter(date__lte=timezone.now()).order_by('date')
#	return render(request, 'blog/post_list.html', {'posts':posts})

@csrf_exempt
def post_list(request):
	if request.method == 'GET':
		body_unicode = request.body.decode("utf-8")
		body_data = json.loads(body_unicode)
		
		if 'category' not in body_data:
			category = '*'
		else:
			category = body_data["category"]
			
		if 'region' not in body_data:
			region = '*'
		else:
			region = body_data["region"]
			
		if 'date' not in body_data:
			date = '*'
		else:
			date_string = body_data["date"]
			date_array = date_string.split("/")
			day = int(date_array[0])
			month = int(date_array[1])
			year = int(date_array[2])
			date = datetime.datetime(year, month, day)
				
		posts = NewsStory.objects.all()
		
		if category is not '*':
			posts = posts.filter(category = category)
		
		if region is not '*':
			posts = posts.filter(region = region)
		
		if date is not '*':
			posts = posts.filter(date__gte = date)
		
		data = list(posts.values())
		return JsonResponse(data, safe=False)
	else:
		return HttpResponse("Requires a POST request")

	
@csrf_exempt
def post_remove(request):
	print(99999999999999999999)
	print(request.POST)
	
	
	if request.method == 'POST':
		if (request.user.is_authenticated):
			body_unicode = request.body.decode("utf-8")
			body_data = json.loads(body_unicode)
			
			if 'story_key' not in body_data:
				return HttpResponse("Story key required")
			else:
				story_key = body_data["story_key"]
			print(story_key)
			post = NewsStory.objects.all()
			post = post.filter(pk = story_key)
			print(post)
			post.delete()	
			return HttpResponse("OK")
		else:
			return HttpResponse("User is not logged in")
	else:
		return HttpResponse("Requires a POST request")
	
		
@csrf_exempt
def post_new(request):
	print(123)
	if request.method == 'POST':
		#form = PostForm(request.POST)
		body_unicode = request.body.decode("utf-8")
		body_data = json.loads(body_unicode)
		if (request.user.is_authenticated):
		
			headline = body_data["headline"]
			details = body_data["details"]
			category = body_data["category"]
			region = body_data["region"]
			#if form.is_valid():
			#post = form.save(commit=False)
			author = Author.objects.get(username=request.user)
			
			new_post = NewsStory(author = author, headline = headline, category = category, region = region, details = details, date = timezone.now())
			new_post.save()
			#post.author = author
			#post.date = timezone.now()
			#post.save()
			return HttpResponse("Created")
			#else:
				#return HttpResponse("Form is invalid")
		else:
			return HttpResponse("User not logged in")
	else:
		return HttpResponse("Requires a POST request")

		
		
		
"""
Server
post_new -> 
		return 201 and 503 response codes
		content type needs to be json
		
		response = HttpResponse()
		response.write("<p>Here's the text of the Web page.</p>")
		
login and logout ->
		ensure that the response is text/plain
		
		
	2018-02-02 10:10:10
	YYYY-MM-DD HH:MM
	
Client
post_new ->
		add restrictions to inputs
login ->
		splitting problem (if you put only one word)
list_stories ->
		add a way to get all stories if id = *
"""		
		
		
		#login http://127.0.0.1:8000
		#news -id="test" -cat="tech" -reg="uk" -date="14/02/2019"
