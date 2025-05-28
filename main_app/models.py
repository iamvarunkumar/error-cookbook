# main_app/models.py

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings # To get the User model correctly

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug: # Only generate slug if it's not already set or is being created
            original_slug = slugify(self.name)
            unique_slug = original_slug
            num = 1
            # Check if a Category with this slug already exists (excluding self if updating)
            while Category.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f'{original_slug}-{num}'
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main_app:errors_by_category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']


class ErrorEntry(models.Model):
    # Define status choices for moderation
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending Review'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    title = models.CharField(max_length=255)
    error_code = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='errors')
    cause_overview = models.TextField(blank=True, null=True, help_text="A general overview of common causes.")
    solution_overview = models.TextField(blank=True, null=True, help_text="A general overview of common solutions or steps.")
    slug = models.SlugField(max_length=280, unique=True, blank=True, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authored_errors'
    )
    # Moderation fields (These should be present)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES, # Ensure STATUS_CHOICES is defined in this model
        default=STATUS_PENDING, # Ensure STATUS_PENDING is defined in this model
        db_index=True
    )
    is_public = models.BooleanField(default=False, db_index=True, help_text="Visible to all users if checked.")
    moderator_notes = models.TextField(blank=True, null=True, help_text="Internal notes for moderators regarding this entry.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_bookmarked_by(self, user):
        if user.is_authenticated:
            return Bookmark.objects.filter(user=user, error_entry=self).exists()
        return False

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            while ErrorEntry.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f'{base_slug}-{num}'
                num += 1
            self.slug = unique_slug
        # Admin actions should explicitly set is_public on approval.
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main_app:error_detail', kwargs={'error_slug': self.slug})

    class Meta:
        verbose_name_plural = "Error Entries"
        ordering = ['-updated_at']


class Comment(models.Model):
    error_entry = models.ForeignKey(ErrorEntry, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments_authored')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.error_entry.title}'

    class Meta:
        ordering = ['created_at']


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks_made')
    error_entry = models.ForeignKey(ErrorEntry, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'error_entry')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} bookmarked "{self.error_entry.title}"'