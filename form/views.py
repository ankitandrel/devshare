from django.db import reset_queries
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from . models import Submit_Resource, Contact
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def submit_resource(request):

    if request.method == "POST":
        resource_name = request.POST['resource_name']
        resource_category = request.POST['resource_category']
        resource_link = request.POST['resource_link']
        resource_info = request.POST['resource_info']
        
        resource = Submit_Resource.objects.create(
            resource_name = resource_name,
            resource_category = resource_category,
            resource_link = resource_link,
            resource_info = resource_info,
            resource_submited_by = request.user
        )
        
        resource.save()
        messages.success(request, "Thanks of Improving the  Community")
        return redirect('submit_resource')

    return render(request, 'form/submit_resource.html')

def contact_form(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        social_handle = request.POST['social']
        subject = request.POST['subject']
        description = request.POST['description']

        save_form = Contact.objects.create(
            name = name,
            email = email,
            social_media_handle = social_handle,
            subject = subject,
            description= description,
        )

        save_form.save()
        messages.success(request, "Thanks for contacting us, we will react you soon.")
        return redirect('contact_form')
    return render(request, 'form/contact_form.html')