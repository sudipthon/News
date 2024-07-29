# django imports
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.core.cache import cache
from django.db.models import Prefetch
from django.db.models import F
from django.utils import timezone

# local imports
from .models import *
from .forms import PostForm, AdForm

# python imports
import nepali_datetime


def get_ads(request, categoryad=None):
    ads = cache.get("ads")
    if not ads:
        ad_category = Category.objects.prefetch_related(Prefetch("category_ads"))

        ads = {
            category.url_name: [ad for ad in category.category_ads.all()]
            for category in ad_category
            if category.category_ads.all()
        }

        cache.set("ads", ads, 60 * 60 * 24)  # cache for 24 hours
    adreturned = []
    for key, value in ads.items():
        if key == categoryad:
            adreturned = value

    return adreturned


def get_categories(request):
    categories_list = cache.get("categories")
    if not categories_list:
        categories = (
            Category.objects.prefetch_related(
                Prefetch(
                    "category_posts",
                    queryset=Post.objects.only(
                        "headline", "featured_image", "first_paragraph", "posted_on_bs"
                    ).filter(status="Published")[:15],
                    to_attr="latest_posts",
                ),
                "subcategories",
            )
            .exclude(name="home")
            .filter(parent=None)
        )
        categories_list = [
            {
                "name": category.name,
                "url_name": category.url_name,
                "category_posts": category.latest_posts,
                "subcategories": (
                    [
                        {
                            "name": subcategory.name,
                            "url_name": subcategory.url_name,
                        }
                        for subcategory in category.subcategories.all()
                    ]
                    if category.subcategories.exists()
                    else []
                ),
            }
            for category in categories
        ]

        cache.set("categories", categories_list, 60 * 60 * 24)  # cache for 24 hours
    return categories_list


def index(request):
    """
    View function for home page and handling the seach bar requests. Returns normal posts querry if no search is made, else returns the posts related to the search query.

    Args:
    - request (HttpRequest): The incoming HTTP request object.

    Input Data (from form):
    - parameter1 (str): search query, fetched from the form.

    Returns:
    - HttpResponse: An HTTP response object containing the posts and ads to be displayed on the home page.

    """
    popup = Popup.objects.all().first()
    date = nepali_datetime.date.today().strftime("%D %N %K, %G")
    search = request.POST.get("search")
    post = (
        Post.objects.all()
        .only("headline", "featured_image", "first_paragraph", "posted_on_bs")
        .filter(status="Published")
        .order_by("-posted_on")[:30]
    )
    if search:
        post = (
            Post.objects.filter(
                Q(headline__icontains=search)
                | Q(categories__name__icontains=search)
                | Q(categories__url_name__icontains=search)
                | Q(tags__name__icontains=search)
            )
            .filter(status="Published")
            .distinct()
            .only("headline", "featured_image", "first_paragraph", "posted_on_bs")[:30]
        )

    ads_cache = get_ads(request, "home")
    ads = {"main": [], "side": []}
    for a in ads_cache:
        if a.section == "main":
            ads["main"].append(a)
        else:
            ads["side"].append(a)

    context = {
        "categories": get_categories(request),
        "post": post,
        "ads": ads,
        "date": date,
        "popup": popup,
    }

    return render(request, "index.html", context)


# news realted views start


def news_by_category(request, urlName: str):
    """
    view function for listing all the related posts in a category

    Args:
    - request (HttpRequest): The incoming HTTP request object and the category slug.

    Returns:
    - HttpResponse: An HTTP response object containing the posts related to the category.

    """
    ads_cache = get_ads(request, urlName)
    ads = {"main": [], "side": []}
    if len(ads_cache) > 1:
        for a in ads_cache:
            if a.section == "main":
                ads["main"].append(a)
            else:
                ads["side"].append(a)

    categories = get_categories(request)
    category_post = [
        post
        for category in categories
        if category["url_name"] == urlName
        for post in category["category_posts"]
    ]

    category_post = Post.objects.filter(
        Q(categories__url_name=urlName) & Q(status="published")
    )

    post = (
        Post.objects.all()
        .exclude(categories__url_name=urlName)[:3]
        .only("headline", "featured_image", "posted_on_bs")
    )
    time_24_hours_ago = timezone.now() - timezone.timedelta(hours=24)

    context = {
        "ads": ads,  # for ads
        "categories": categories,
        "category_post": category_post,
        "post": post,
        "time_24_hours_ago": time_24_hours_ago,
    }
    return render(request, "category-home.html", context)


def create_news(request):
    """
    View function for adding a new post.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.

    """
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
        return redirect("index")
    context = {"form": form}
    return render(request, "quill.html", context)


def single_news(request, id):
    """
    View function for displaying the details of a post.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the post to display.

    Returns:
        HttpResponse: The rendered HTML response containing the details of the post.
    """

    categories = get_categories(request)
    single_post = Post.objects.get(id=id)
    Post.objects.filter(id=id).update(views_count=F("views_count") + 1)

    ads_cache = get_ads(request, single_post.categories.all()[0].url_name)
    ads = {"main": [], "side": []}
    for a in ads_cache:
        if a.section == "main":
            ads["main"].append(a)
        else:
            ads["side"].append(a)

    category_post = []
    single_post_url_name = single_post.categories.all()[0].url_name
    for category in categories:
        if category["url_name"] == single_post_url_name:
            category_post = category["category_posts"]
            break

    time_24_hours_ago = timezone.now() - timezone.timedelta(hours=24)
    latest_posts = Post.objects.all().order_by("-posted_on")[:8]
    context = {
        "ads": ads,
        "categories": categories,  # for navbar
        "single_news": single_post,
        "category_posts": category_post,
        "latest_posts": latest_posts,
        "time_24_hours_ago": time_24_hours_ago,
    }
    return render(request, "news_single.html", context)


def edit_news(request, id):
    """
    View function for editing an existing post.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the post to be edited.

    Returns:
        HttpResponse: The HTTP response object.

    """
    # return HttpResponse("Hello")

    post = Post.objects.get(id=id)
    form = PostForm(instance=post)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
        return redirect("index")
    context = {"form": form}
    return render(request, "quill.html", context)


def delete_news(request, id):
    """
    View function for deleting a post.

    Args:
    - request: The HTTP request object.
    - id: The ID of the post to be deleted.

    Returns:
    - A redirect response to the index page.

    Raises:
    - Post.DoesNotExist: If the post with the given ID does not exist.
    """
    try:
        post = Post.objects.get(id=id)
        post.delete()
    except Post.DoesNotExist:
        return HttpResponse("Post does not exist")

    return redirect("index")


# news realted views end


# ad realted views start
def list_ads(request):
    """
    View function for listing all the ads.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: The rendered HTML response.
    :rtype: HttpResponse
    """
    ads = Ad.objects.all()
    context = {"ads": ads}
    return render(request, "ads.html", context)


def create_ad(request):
    """
    View function for creating a new ad.

    Args:
        - request (HttpRequest): The incoming HTTP request object.
    Input Data (from form):
        - parameter2 (str): image file encoded in base64, fetched from the form.
    Returns:
        - HttpResponse: An HTTP response object containing the image link returned by imgur.
    """
    form = AdForm()
    if request.method == "POST":
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("index")
    context = {"form": form}
    return render(request, "create_ad.html", context)


def edit_ad(request, id):
    """
    View function for editing an existing ad.

    Args:
        -request (HttpRequest): The HTTP request object.
        -id (int): The ID of the ad to be edited.
    Returns:
        HttpResponse: The HTTP response object.
    """
    if request.method == "POST":
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
        return redirect("index")
    ad = Ad.objects.get(id=id)
    form = AdForm(instance=ad)
    context = {"form": form}
    return render(request, "create_ad.html", context)


def delete_ad(request, id):
    """
    View function for deleting an ad.

    Args:
      - request: The HTTP request object.
      - id: The ID of the ad to be deleted.

    Returns:
         - A redirect response to the index page.

    Raises:
         - Ad.DoesNotExist: If the ad with the given ID does not exist.
    """
    try:
        ad = Ad.objects.get(id=id)
        ad.delete()
    except Ad.DoesNotExist:
        return HttpResponse("Ad does not exist")
    return redirect("index")


# def maintenance(request):
#     return render(request, "503.html")
