
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .models import Code
import openai
import os


# Function to get response from openAI
def openAI_response(code, lang, task):

	# Get API Key
	api_key = os.getenv('API_KEY')

	# If API Key is "None"
	if not api_key:
		print("API_KEY is not set or is empty")
		response = "# OpenAI function is currently not available. First add an API key."
		return response
    	
	# argument 'task' must be 'fix' or 'suggest'
	if task == "fix":
		AI_prompt = f"Respond only with code. Fix this {lang} code: (code)"
	elif task == "suggest":
		AI_prompt = f"Respond only with code. {code}"

	# Set OpenAI Key
	openai.api_key = api_key

	# Create OpenAI instance to print the different models
	try:
		models = openai.Model.list()
		print(models)
	except Exception as e:
		print(f"Error fetching models: {e}")

	# Make an OpenAI request
	try:
		# Response is a python dict and must be parsed
		response = openai.Completion.create(
			model = 'text-ada-001', # 'text-davinci-003' is more expensive
			prompt = AI_prompt,
			temperature = 0, # High value means more creativity
			max_tokens = 100, # Amount of (sub)words - keep low to stay cheap
			top_p=1.0, # nucleas sampling, probability measure to select output
			frequency_penalty =0.0, # High value means less repeatings
			presence_penalty=0.0, # High value means a reduction of words which are used in the prompt
			)

		# Parse response
		response = (response["choices"][0]["text"]).strip()

	# if request failed
	except Exception as e:
		response = e	

	return response


# Function to fix code using openAI
def home(request):

	# API = place_here_your_API_KEY
	lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'csv', 'dart', 'django', 'docker', 'git', 'go', 'html', 'java', 'javascript', 'json', 'jsx', 'latex', 'markup', 'markup-templating', 'matlab', 'mongodb', 'objectivec', 'perl', 'php', 'powershell', 'python', 'r', 'regex', 'ruby', 'rust', 'sass', 'sql', 'swift', 'typescript', 'typoscript', 'xml-doc', 'yaml']
	
	if request.method == "POST":
		code = request.POST['code']
		lang = request.POST['lang']

		# Check if user choose a language
		if lang == "Select Programming Language":
			messages.success(request,"Hey! You forgot to pick a programming language...")
			return render(request, 'home.html', {'lang_list':lang_list, 'code':code, 'lang':lang})	
		else:
			response = openAI_response(code, lang, "fix") # change "no_task" to "fix" for openai

			# Save to database ()
			record = Code(question=code, code_answer=response, language=lang, user=request.user)
			record.save()

			return render(request, 'home.html', {'lang_list':lang_list, 'response':response, 'lang':lang})

	# If method is not POST
	return render(request, 'home.html', {'lang_list':lang_list})


# Function to get suggestion from openAI
def suggest(request):
	lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'csv', 'dart', 'django', 'docker', 'git', 'go', 'html', 'java', 'javascript', 'json', 'jsx', 'latex', 'markup', 'markup-templating', 'matlab', 'mongodb', 'objectivec', 'perl', 'php', 'powershell', 'python', 'r', 'regex', 'ruby', 'rust', 'sass', 'sql', 'swift', 'typescript', 'typoscript', 'xml-doc', 'yaml']
	
	if request.method == "POST":
		code = request.POST['code']
		lang = request.POST['lang']

		# Check if user chose a language
		if lang == "Select Programming Language":
			messages.success(request,"Hey! You forgot to pick a programming language...")
			return render(request, 'suggest.html', {'lang_list':lang_list, 'code':code, 'lang':lang})	
		else:
			response = openAI_response(code, lang, "suggest") # change "no_task" to "suggest" for openai
			
			# Save to database ()
			record = Code(question=code, code_answer=response, language=lang, user=request.user)
			record.save()

			return render(request, 'suggest.html', {'lang_list':lang_list, 'response':response, 'lang':lang})

	# If method is not POST
	return render(request, 'suggest.html', {'lang_list':lang_list})


# Login
def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You have been logged in !")
			return redirect('home')
		else:
			messages.success(request, "Error logging in. Please try again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {})


# Logout
def logout_user(request):
	logout(request)
	messages.success(request, "You have been logged out successfully !")
	return redirect('home')


# Register
def register_user(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request,'You have registered successfully !')
			return redirect('home')
	else:
		form = SignUpForm()
	return render(request, 'register.html', {"form":form})


# History page
def hist(request):
	if request.user.is_authenticated:
		code = Code.objects.filter(user_id=request.user.id)
		return render(request, 'hist.html', {"code":code})
	else:
		messages.success(request, "You must be logged in to see this page.")
		return redirect('home')


# Delete history
def delete_hist(request, hist_id):
	hist = Code.objects.get(pk=hist_id)
	hist.delete()
	messages.success(request, "Deleted successfully !")
	return redirect('hist')


