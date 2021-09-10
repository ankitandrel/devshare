from django.db.models.query import RawQuerySet
from django.shortcuts import redirect, render, get_object_or_404
from resource.models import Category, Resource,Article, Like_Unlike
from taggit.models import Tag
from . forms import ArticleForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def home(request):
    all_category = Category.objects.all()
    featured_reasource = Resource.objects.all().filter(is_featured = True)
    featured_article = Article.objects.all().filter(is_featured = True)
    
    context = {
        'all_category':all_category,
        'featured_reasource':featured_reasource,
        'featured_article': featured_article,
    }
    return render(request,'home.html',context)

def view_all_category(request):
    category = Category.objects.all()
    articles = Article.objects.all()
    context = {
        'category':category,
        'articles':articles,
    }

    return render(request, 'resource/all_category.html', context)

def article(request):
    articles = Article.objects.order_by('-article_posted_on')
    common_tags = Article.objects.order_by('-article_posted_on')[:2]
    context = {
        'articles':articles,
        'common_tags':common_tags
    }
    return render(request,'resource/articles.html', context)

@login_required(login_url='login')
def post_article(request):
    
    common_tags = Article.objects.order_by('-article_posted_on')
    
    form = ArticleForm(request.POST)
    
    if form.is_valid():
        newArticle = form.save(commit=False)
        newArticle.article_posted_by = request.user
        newArticle.save()
        form.save()
    context = {
        'common_tags':common_tags,
        'form':form,
    }

    return redirect('article')
    # return render(request,'resource/articles.html',context)

@login_required(login_url='login')
def article_like(request, id):
    if request.method == "POST":
        like_button = request.POST['like']
        article = get_object_or_404(Article, pk = id)
        if article.liked.filter(id=request.user.id).exists():
            article.liked.remove(request.user)
        else:
            article.liked.add(request.user)

        like, created = Like_Unlike.objects.get_or_create(user=request.user, article_id=id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

            article.save()
            like.save()



    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def article_by_tag(request, slug):
    
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name  
    articles = Article.objects.filter(article_tag=tag)
    context = {
        'tag':tag,
        'articles':articles,
    }
    return render(request, 'resource/articles.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            resources= Resource.objects.order_by('-posted_date').filter(Q(resource_name__icontains=keyword) | Q(resource_info__icontains=keyword))
            articles= Article.objects.order_by('-article_posted_on').filter(Q(article_title__icontains=keyword) | Q(article_info__icontains=keyword))
            resources_count = resources.count()
            articles_count = articles.count()
    
            total_search_reasult = resources_count + articles_count
    context = {
        'resources': resources,
        'resources_count': resources_count,
        'articles':articles,
        'articles_count':articles_count,
        'total_search_reasult':total_search_reasult
    }
    return render(request, 'resource/search.html', context)


def about(request):
    return render(request, 'about.html')
