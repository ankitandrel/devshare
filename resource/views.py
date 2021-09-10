from resource import context_processor
from django.db.models.deletion import CASCADE
from django.shortcuts import redirect, render, get_object_or_404
from . models import Article, Category, Resource, Like_Unlike
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def resource_by_category(request, category_name_slug = None):
    if category_name_slug != None:
        category_name = get_object_or_404(Category,  category_name_slug = category_name_slug) 
        resources = Resource.objects.all().filter(resource_category = category_name)
    else:
        resources = Resource.objects.all()

    context = {
        'resources':resources,
    }

    return render(request,'resource/resource.html', context)

@login_required(login_url='login')
def resource_like(request, id):
    if request.method == "POST":
        like_button = request.POST['like']
        resource = get_object_or_404(Resource, pk = id)
        if resource.liked.filter(id=request.user.id).exists():
            resource.liked.remove(request.user)
        else:
            resource.liked.add(request.user)

        like, created = Like_Unlike.objects.get_or_create(user=request.user, resource_id=id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

            resource.save()
            like.save()



    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
   
@login_required(login_url='login')
def delete_resource(request,id):
    resource = Resource.objects.get(id = id)
    if request.method == "POST":
        resource.delete()
        return redirect('profile')
    
    context = {
        'resource':resource
    }

    return render(request, 'users/profile.html', context)

@login_required(login_url='login')
def delete_article(request,id):
    article = Article.objects.get(id = id)
    if request.method == "POST":
        article.delete()
        return redirect('profile')
    
    context = {
        'article':article
    }

    return render(request, 'users/profile.html', context)