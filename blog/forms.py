from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, UserProfile, Tag


def _bs(widget, extra=''):
    """Add Bootstrap class to a widget."""
    if isinstance(widget, (forms.Select, forms.SelectMultiple)):
        cls = 'form-select'
    elif isinstance(widget, forms.CheckboxInput):
        cls = 'form-check-input'
    else:
        cls = 'form-control'
    if extra:
        cls += ' ' + extra
    existing = widget.attrs.get('class', '')
    widget.attrs['class'] = (existing + ' ' + cls).strip()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            _bs(field.widget)
            field.widget.attrs.setdefault('autocomplete', 'off')
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a username'
        self.fields['email'].widget.attrs['placeholder'] = 'your@email.com'
        self.fields['password1'].widget.attrs['placeholder'] = 'Create a password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text='Comma-separated tags (e.g. python, django, web)',
        widget=forms.TextInput(attrs={
            'placeholder': 'python, django, web...',
            'class': 'form-control',
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'body', 'status', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a compelling title...'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 16, 'placeholder': 'Tell your story...'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags'].initial = ', '.join(
                [tag.name for tag in self.instance.tags.all()]
            )

    def save(self, commit=True):
        post = super().save(commit=commit)
        if commit:
            from django.utils.text import slugify
            tags_str = self.cleaned_data.get('tags', '')
            post.tags.clear()
            if tags_str:
                for name in [t.strip().lower() for t in tags_str.split(',') if t.strip()]:
                    tag, _ = Tag.objects.get_or_create(
                        slug=slugify(name),
                        defaults={'name': name}
                    )
                    post.tags.add(tag)
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your thoughts...',
            })
        }
        labels = {'body': ''}


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell the world about yourself...',
            }),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
