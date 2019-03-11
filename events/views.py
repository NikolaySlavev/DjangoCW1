from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
from .models import Author, NewsStory
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
import json, datetime


@csrf_exempt
def handle_login(request):
	# handles the login functionality
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		data = "username=%s, password=%s" % (username, password)
		user = authenticate(request, username=username, password=password)
		# if the user doesn't exist or was not authenticated with the correct credentials we return an invalid login.
		# Otherwise, the login is successful
		if user is not None:
			if user.is_active:
				login(request, user)
				data = 'Hi ' + str(username) + '\nYou logged in with the following credentials: \n' + str(data)
				return HttpResponse(data, status = 200)
			else:
				return HttpResponse('Invalid login', status = 401)
		else:
			return HttpResponse('Invalid login', status = 401)
	else:
		# if the request wasn't post, an error message is returned
		return HttpResponse('Requires a POST request', status = 503)

@csrf_exempt
def handle_logout(request):
	# handles the logout
	if request.method == 'POST':
		if (request.user.is_authenticated):
			logout(request)
			return HttpResponse("Goodbye")
		else:
			# if the user is not logged in and we call the logout it will provide the appropriate mesasge.
			# The message will still return 200 because there weren't any errors
			return HttpResponse("User is not logged in")
	else:
		return HttpResponse("Requires a POST request", status = 503)

@csrf_exempt
def post_list(request):
	# handles the listing of the stories
	if request.method == 'GET':
		body_unicode = request.body.decode("utf-8")
		body_data = json.loads(body_unicode)
		
		# because the restriction in the models file would only apply if we were using templates
		# we need to add additional code in order to meet the coursework requirements
		# we first retrieve all stories
		posts = NewsStory.objects.all()
		# then check if any of the filter are present
		if 'story_cat' in body_data.keys() and body_data["category"] != "*":
			# if a filter is present, we check whether the filter has a valid value
			if body_data["category"] not in ["POL", "ART", "TECH", "TRIVIA"]:
				return HttpResponse("Invalid Category. Must be POL, ART, TECH or TRIVIA", status = 503)
			# if everything is valid, we filter the stories
			posts = posts.filter(category = body_data["category"])
		if 'story_region' in body_data.keys() and body_data["region"] != "*":
			if body_data["region"] not in ["UK", "EU", "W"]:
				return HttpResponse("Invalid Region. Must be UK, EU or W", status = 503)
			posts = posts.filter(region = body_data["region"])
		if 'story_date' in body_data.keys() and body_data["date"] != "*":
			# the date field has a strange format so we adjust it in order to meet the coursework specs
			if "/" not in body_data["date"] or len(body_data["date"].split("/")) !=3:
				return HttpResponse("Invalid date format. Must be day/month/year", status=503)
			date_array = body_data["date"].split("/")
			if not date_array[0].isdigit() or not date_array[1].isdigit() or not date_array[2].isdigit():
				return HttpResponse("Date inputs need to be integers", status=503)
			day = int(date_array[0])
			month = int(date_array[1])
			year = int(date_array[2])
			try:
				date = datetime.datetime(year, month, day)
			except Exception as e:
				return HttpResponse(e, status=503)
			posts = posts.filter(date__gte = date)
		
		# again in order to meet the coursework specifications we make a custome made json container and send it
		custom_data = []
		for story in posts:
			date = str(story.date.day) + "/" + str(story.date.month) + "/" + str(story.date.year)
			custom_data.append({"key": story.id, "headline": story.headline, "story_cat": story.category, "story_region": story.region, "author": story.author.name, "story_date": date, "story_details": story.details})
		return JsonResponse({"stories": custom_data}, safe=False)
	else:
		return HttpResponse("Requires a POST request", status = 503)
	
@csrf_exempt
def post_remove(request):
	# handles the removal of story
	if request.method == 'POST':
		if (request.user.is_authenticated):
			body_unicode = request.body.decode("utf-8")
			body_data = json.loads(body_unicode)
			# if the story key is not there, we return an error
			if 'story_key' not in body_data.keys():
				return HttpResponse("Story key required", status = 503)
			story_key = body_data["story_key"]
			post = NewsStory.objects.all()
			if not story_key.isdigit():
				return HttpResponse("Story key needs to be an integer", status = 503)
			post = post.filter(pk = story_key)
			if len(post) == 0:
				return HttpResponse("Story with story_key=" + str(story_key) + " does not exist", status = 503)
			post.delete()	
			return HttpResponse("Story removed successfully")
		else:
			return HttpResponse("User is not logged in", status = 503)
	else:
		return HttpResponse("Requires a POST request", status = 503)
		
@csrf_exempt
def post_new(request):
	# handles the posting of a new story
	if request.method == 'POST':
		body_unicode = request.body.decode("utf-8")
		body_data = json.loads(body_unicode)
		if request.user.is_authenticated:
			for argument in ["headline", "details", "category", "region"]:				
				if (argument not in body_data.keys()):
					return HttpResponse("Argument " + str(argument) + " is not specified.", status = 503)
			headline = body_data["headline"]
			details = body_data["details"]
			category = body_data["category"]
			region = body_data["region"]
			author = Author.objects.get(username=request.user)
			# we check if everything is valid as stated by the coursework specifications
			if len(headline) > 64:
				return HttpResponse("Exceeded Headline length of 64 characters", status = 503)
			if len(details) > 512:
				return HttpResponse("Exceeded Details length of 512 characters", status = 503)
			if region not in ["UK", "EU", "W"]:
				return HttpResponse("Invalid Region. Must be UK, EU or W", status = 503)
			if category not in ["POL", "ART", "TECH", "TRIVIA"]:
				return HttpResponse("Invalid Category. Must be POL, ART, TECH or TRIVIA", status = 503)
			
			new_post = NewsStory(author = author, headline = headline, category = category, region = region, details = details, date = timezone.now())
			new_post.save()
			return HttpResponse("Created Successfully", status = 201)
		else:
			# since the user was not logged in, we return an error message
			return HttpResponse("User not logged in", status = 503)
	else:
		return HttpResponse("Requires a POST request", status = 503)
