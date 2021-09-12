# models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

User = get_user_model()


# creating model manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")


# post model
class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")

    image = models.ImageField(
        upload_to="featured_image/%Y/%m/%d/", blank=True, null=True
    )  # this

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    # body = models.TextField() # remove this
    body = RichTextUploadingField()  # add this

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])
