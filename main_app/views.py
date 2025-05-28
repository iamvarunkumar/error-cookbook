from django.shortcuts import render, get_object_or_404, redirect
from .models import ErrorEntry, Category, Comment, Bookmark
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.contrib import messages
from .forms import ErrorSearchForm, CommentForm, ErrorEntryForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404 # Add Http404

# ... (get_common_context and RegisterView remain the same) ...
def get_common_context(request):
    return {
        'categories': Category.objects.all(),
        'search_form': ErrorSearchForm(request.GET if request.method == 'GET' else None)
    }

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful! You can now log in.')
        return response

# MODIFIED Views to filter by is_public=True and status=APPROVED
def index(request):
    common_context = get_common_context(request)
    # Only show approved and public errors
    recent_errors = ErrorEntry.objects.filter(is_public=True, status=ErrorEntry.STATUS_APPROVED).order_by('-updated_at')[:5]
    context = {**common_context, 'recent_errors': recent_errors}
    return render(request, 'main_app/index.html', context)

def error_list(request):
    common_context = get_common_context(request)
    error_entries = ErrorEntry.objects.filter(is_public=True, status=ErrorEntry.STATUS_APPROVED).order_by('-updated_at')
    context = {**common_context, 'error_entries': error_entries, 'list_title': 'All Errors'}
    return render(request, 'main_app/error_list.html', context)

def errors_by_category(request, category_slug):
    common_context = get_common_context(request)
    category = get_object_or_404(Category, slug=category_slug)
    error_entries = ErrorEntry.objects.filter(category=category, is_public=True, status=ErrorEntry.STATUS_APPROVED).order_by('-updated_at')
    context = {**common_context, 'error_entries': error_entries, 'current_category': category, 'list_title': f'Errors in {category.name}'}
    return render(request, 'main_app/error_list.html', context)

def category_list(request): # No change needed for filtering here, just lists categories
    common_context = get_common_context(request)
    return render(request, 'main_app/category_list.html', common_context)

def search_results(request):
    common_context = get_common_context(request)
    query = request.GET.get('query')
    results = ErrorEntry.objects.none()
    if query:
        # Base query for public and approved errors
        base_query = ErrorEntry.objects.filter(is_public=True, status=ErrorEntry.STATUS_APPROVED)
        results = base_query.filter(
            Q(title__icontains=query) | Q(description__icontains=query) |
            Q(error_code__icontains=query) | Q(category__name__icontains=query)
        ).distinct().order_by('-updated_at')
    context = {**common_context, 'query': query, 'results': results, 'list_title': f'Search Results for "{query}"' if query else 'Search Results'}
    return render(request, 'main_app/search_results.html', context)


# Error Detail View - MODIFIED for moderation status
def error_detail(request, error_slug):
    common_context = get_common_context(request)
    error_entry = get_object_or_404(ErrorEntry, slug=error_slug)

    # Check if the error can be viewed
    can_view = error_entry.is_public and error_entry.status == ErrorEntry.STATUS_APPROVED
    if not can_view and request.user.is_authenticated:
        # Allow author or staff/superuser to view non-public entries
        if error_entry.author == request.user or request.user.is_staff:
            can_view = True
    
    if not can_view:
        raise Http404("Error entry not found or not approved.")

    comments = error_entry.comments.all().order_by('-created_at')
    comment_form = CommentForm()
    is_bookmarked = error_entry.is_bookmarked_by(request.user)

    if request.method == 'POST': # Handles comment submission
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to post a comment.")
        else:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.error_entry = error_entry
                new_comment.author = request.user
                new_comment.save()
                messages.success(request, "Your comment has been added successfully!")
                return redirect(error_entry.get_absolute_url())
            else:
                messages.error(request, "There was an error with your comment. Please check the form.")

    related_errors = []
    if error_entry.category and error_entry.is_public and error_entry.status == ErrorEntry.STATUS_APPROVED: # Only show related if current is public
        related_errors = ErrorEntry.objects.filter(
            category=error_entry.category,
            is_public=True,
            status=ErrorEntry.STATUS_APPROVED
        ).exclude(pk=error_entry.pk).order_by('?')[:3]

    context = {
        **common_context,
        'error_entry': error_entry,
        'comments': comments,
        'comment_form': comment_form,
        'related_errors': related_errors,
        'is_bookmarked': is_bookmarked,
        'can_view_fully': error_entry.is_public and error_entry.status == ErrorEntry.STATUS_APPROVED, # To adjust display based on status
    }
    return render(request, 'main_app/error_detail.html', context)

# Submit Error View - MODIFIED for default status
@login_required
def submit_error(request):
    common_context = get_common_context(request)
    if request.method == 'POST':
        form = ErrorEntryForm(request.POST)
        if form.is_valid():
            new_error = form.save(commit=False)
            new_error.author = request.user
            new_error.status = ErrorEntry.STATUS_PENDING # Default to pending
            new_error.is_public = False # Default to not public
            new_error.save() # Slug will be generated here
            messages.success(request, f'Thank you! Your error "{new_error.title}" has been submitted and is pending review.')
            # Redirect to their "My Submissions" page or the new error's detail page (which might show pending status)
            return redirect(reverse('main_app:my_submissions'))
        else:
            messages.error(request, "There were errors in your submission. Please correct them.")
    else:
        form = ErrorEntryForm()

    context = {**common_context, 'form': form, 'form_title': 'Submit a New Error Entry'}
    return render(request, 'main_app/submit_error.html', context)

# My Bookmarks View - No change needed other than ensuring it uses common_context
@login_required
def my_bookmarks(request):
    common_context = get_common_context(request)
    user_bookmarks = Bookmark.objects.filter(user=request.user).select_related('error_entry')
    # Only show bookmarked errors that are currently public and approved
    bookmarked_errors = [
        bookmark.error_entry for bookmark in user_bookmarks 
        if bookmark.error_entry.is_public and bookmark.error_entry.status == ErrorEntry.STATUS_APPROVED
    ]
    # Alternative: If you want to show all bookmarked errors regardless of status (user might have bookmarked before it was un-published)
    # bookmarked_errors = [bookmark.error_entry for bookmark in user_bookmarks]

    context = {**common_context, 'bookmarked_errors': bookmarked_errors, 'list_title': 'My Bookmarked Errors'}
    return render(request, 'main_app/my_bookmarks.html', context)


# Add/Remove Bookmark Views - No change needed from Sprint 4
@login_required
def add_bookmark(request, error_slug):
    error_entry = get_object_or_404(ErrorEntry, slug=error_slug)
    # Allow bookmarking even if not public, user might be author or admin
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, error_entry=error_entry)
    if created: messages.success(request, f'"{error_entry.title}" has been added to your bookmarks.')
    else: messages.info(request, f'"{error_entry.title}" is already in your bookmarks.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', error_entry.get_absolute_url()))

@login_required
def remove_bookmark(request, error_slug):
    error_entry = get_object_or_404(ErrorEntry, slug=error_slug)
    bookmark = Bookmark.objects.filter(user=request.user, error_entry=error_entry)
    if bookmark.exists():
        bookmark.delete()
        messages.success(request, f'"{error_entry.title}" has been removed from your bookmarks.')
    else: messages.info(request, f'"{error_entry.title}" was not in your bookmarks.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', error_entry.get_absolute_url()))


# --- New View for Sprint 6: My Submissions ---
@login_required
def my_submissions(request):
    common_context = get_common_context(request)
    user_submissions = ErrorEntry.objects.filter(author=request.user).order_by('-updated_at')
    context = {
        **common_context,
        'user_submissions': user_submissions,
        'list_title': 'My Submitted Errors'
    }
    return render(request, 'main_app/my_submissions.html', context)

def user_profile_detail(request, username): # <<< THIS IS THE VIEW
    common_context = get_common_context(request)
    profile_user = get_object_or_404(User, username=username)

    authored_errors_query = ErrorEntry.objects.filter(author=profile_user).order_by('-updated_at')
    if request.user != profile_user:
        authored_errors = authored_errors_query.filter(is_public=True, status=ErrorEntry.STATUS_APPROVED)
    else:
        authored_errors = authored_errors_query

    user_comments = Comment.objects.filter(
        author=profile_user,
        error_entry__is_public=True,
        error_entry__status=ErrorEntry.STATUS_APPROVED
    ).select_related('error_entry', 'error_entry__category').order_by('-created_at')

    context = {
        **common_context,
        'profile_user': profile_user,
        'authored_errors': authored_errors,
        'user_comments': user_comments,
    }
    return render(request, 'main_app/user_profile_detail.html', context)