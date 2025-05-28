from django import forms
from .models import Comment, ErrorEntry, Category # Add ErrorEntry, Category

# ... (ErrorSearchForm and CommentForm remain the same as in Sprint 4) ...
class ErrorSearchForm(forms.Form):
    query = forms.CharField(
        label='Search Errors',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control me-2 glass-form-input',
            'type': 'search',
            'placeholder': 'Search by keyword...',
            'aria-label': 'Search'
        })
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control form-control-sm glass-form-input',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            }),
        }
        labels = {
            'body': ''
        }

# New ErrorEntryForm for Sprint 5
class ErrorEntryForm(forms.ModelForm):
    # Explicitly define category to use a ModelChoiceField with better widget if needed
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select glass-form-input'}),
        required=True # Make category selection mandatory
    )

    class Meta:
        model = ErrorEntry
        fields = ['title', 'error_code', 'category', 'description', 'cause_overview', 'solution_overview']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control glass-form-input', 'placeholder': 'e.g., Python TypeError: unsupported operand type(s)'}),
            'error_code': forms.TextInput(attrs={'class': 'form-control glass-form-input', 'placeholder': 'e.g., HTTP 404, ERR_CONNECTION_REFUSED'}),
            'description': forms.Textarea(attrs={'class': 'form-control glass-form-input', 'rows': 4, 'placeholder': 'Detailed description of when and how the error occurs.'}),
            'cause_overview': forms.Textarea(attrs={'class': 'form-control glass-form-input', 'rows': 3, 'placeholder': 'Common reasons why this error might happen.'}),
            'solution_overview': forms.Textarea(attrs={'class': 'form-control glass-form-input', 'rows': 5, 'placeholder': 'Step-by-step solutions or general approaches to fix it.'}),
        }
        labels = {
            'error_code': 'Error Code (Optional)',
            'cause_overview': 'Common Causes (Optional)',
            'solution_overview': 'Solutions / Fixes (Optional)',
        }
        help_texts = {
            'category': 'Select the most relevant category for this error.',
        }