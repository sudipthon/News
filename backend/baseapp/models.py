# django imports
import datetime
import os
import re

# python imports
import nepali_datetime
from bs4 import \
    BeautifulSoup
# django third party imports
from ckeditor_uploader.fields import \
    RichTextUploadingField
from django.contrib.auth.models import \
    User
from django.core.cache import \
    cache
from django.db import \
    models
from django.utils import \
    timezone
from django.utils.functional import \
    cached_property
from django.utils.text import \
    slugify
from nepali_datetime import \
    date

# Create your models here.


def get_upload_path(instance, filename):
    """
    Function to return the upload path for the image and video field of Ad model.
    """
    if isinstance(instance, Post):
        sanitized_headline = re.sub("[^a-zA-Z]", "", instance.headline)
        return os.path.join("Posts", instance.author.username, sanitized_headline[:20], filename)

    return os.path.join("Ads", instance.party_name, instance.title, filename)


class Tags(models.Model):
    """
    Model representing a tag for a post.
    """

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Tags"
        verbose_name = "Tag"

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Model representing a category for a post.
    """

    name = models.CharField(max_length=100)
    url_name = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subcategories",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Override the save method to populate the slug field."""
        cache.delete("categories")
        self.url_name = slugify(self.url_name)
        super().save(*args, **kwargs)


class Post(models.Model):
    """
    Model representing a post.
    """

    options = (
        ("Published", "Published"),
        ("Draft", "Draft"),
        ("Deleted", "Deleted"),
    )

    headline = models.TextField()
    featured_image = models.ImageField(upload_to=get_upload_path, null=True, blank=True, default="None")
    first_paragraph = models.TextField(null=True, blank=True)
    content = RichTextUploadingField()
    posted_on = models.DateTimeField(blank=True, null=True)
    posted_on_bs = models.CharField(max_length=100, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="category_posts")
    tags = models.ManyToManyField("Tags", related_name="tag_posts")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    views_count = models.IntegerField(default=0)
    status = models.CharField(max_length=100, choices=options, default="Draft")

    class Meta:
        ordering = ["-posted_on"]

    def __str__(self):
        return self.headline

    def save(self, *args, **kwargs):
        if self.status == "Published" and self.pk is not None:
            old_post = Post.objects.get(pk=self.pk)
            if old_post.status != "Published":
                self.posted_on = timezone.now()
                self.posted_on_bs = nepali_datetime.date.from_datetime_date(self.posted_on.date()
                                                                            ).strftime('%D %N %K, %G')
        elif self.status != "Published":
            self.posted_on = None
            self.posted_on_bs = None

        soup = BeautifulSoup(self.content, "html.parser")
        first_p = soup.find_all("p")
        for p in first_p:
            if p.text.strip() != "":
                first_p = p.text
                break
        self.first_paragraph = first_p
        print(self.posted_on)
        cache.delete("categories")
        super().save(*args, **kwargs)


class Ad(models.Model):
    """
    Model representing an advertisement.
    """

    options = (
        ("side", "Side"),
        ("main", "Main"),
    )
    party_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    # video = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    section = models.CharField(max_length=100, choices=options, default="main")
    categories = models.ManyToManyField("Category", related_name="category_ads", blank=True)

    def __str__(self):
        return self.title

    def save(self):
        cache.delete("ads")
        super().save()


class Popup(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="popup/", null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
