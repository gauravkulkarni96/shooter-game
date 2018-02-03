from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import details, scores
from django.views.decorators.csrf import csrf_exempt
import json
MAX_TRIES = 10
# Create your views here.

def home(request):
	# print request.session['user'].email
	if 'email' not in request.session and 'name' not in request.session:
		return render(request, 'home.html')
	
	user = details.objects.get(id = request.session['id'])
	tries = scores.objects.filter(user = user)

	top = scores.objects.all().order_by('-score')[:50]
	context = {
		'topten':top,
	}
	context['tries'] = MAX_TRIES-len(tries)
	if len(tries) >= MAX_TRIES:
		context['tries'] = "0"
	
	return render(request, 'index.html', context)

def submit(request):
	name = request.POST.get('name')
	email = request.POST.get('email')
	phone = request.POST.get('phone')
	searchobj = details.objects.filter(name = name, email = email, phone = phone)
	if len(searchobj) == 0:
		detailobj = details(name = name, email = email, phone = phone)
		detailobj.save()
		searchobj = details.objects.filter(name = name, email = email, phone = phone)
	searchobj = searchobj[0]
	request.session['id'] = searchobj.id
	request.session['email'] = email
	request.session['name'] = name
	return HttpResponseRedirect('/')

def delsession(request):
	if 'email' in request.session:
		del request.session['email']
	if 'name' in request.session:
		del request.session['name']
	if 'id' in request.session:
		del request.session['id']
	if 'tries' in request.session:
		del request.session['tries']
	return HttpResponseRedirect('/')

@csrf_exempt
def savescore(request):
	score = request.POST.get('score')
	win = request.POST.get('win')
	user = details.objects.get(id = request.session['id'])

	tries = scores.objects.filter(user = user)
	tries = MAX_TRIES - len(tries)
	if tries<=0:
		tries = "Tries left: 0"
		context_list = {
		'tries': tries
		}
		return HttpResponse(json.dumps(context_list),content_type="application/json")

	if win == 'true':
		win = True
	else:
		win = False
	scoreobj = scores(user = user, score = score, win = win)
	scoreobj.save()
	tries -= 1
	if tries <= 0:
		tries = "Tries left: 0"
	else:
		tries = "Tries left: "+str(tries)
	context_list = {
	'tries': tries
	}
	return HttpResponse(json.dumps(context_list),content_type="application/json")

def gettop(request):
	top = scores.objects.order_by('-score', '-win', 'date')[:50]
	
	context = {
		'topten':top,
	}
	return render(request, 'table.html', context)

def tnc(request):
	return render(request, 'tnc.html')