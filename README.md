# 📝 Student Blog Platform

A full-featured multi-user blogging platform built with **Python · Django · SQLite · Bootstrap 5**.

---

## ✨ Features

| Feature | Details |
|---|---|
| User Registration & Login | Secure sign-up, sign-in, session management |
| Create / Edit / Delete Posts | Rich form with title, body, tags, thumbnail, status |
| Draft vs Published | Drafts visible only to author |
| Post Detail Page | Full content, author info, tags, comments |
| Leave Comments | Logged-in users can comment on any published post |
| Tag Filtering | Click a tag to filter the home feed |
| Pagination | 6 posts per page with Previous/Next controls |
| User Profile | Avatar, bio, list of published posts |
| Thumbnail Upload | Optional cover image; placeholder shown if none |

---

## 🚀 Quick Start

### Option 1 — Automated (recommended)
```bash
bash setup.sh
```

### Option 2 — Manual
```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py makemigrations
python manage.py migrate

# 4. (Optional) Create admin user
python manage.py createsuperuser

# 5. Start the server
python manage.py runserver
```

Then open **http://127.0.0.1:8000** in your browser.

---

## 📁 Project Structure

```
DJANGO_BLOG_PROJECT/
├── blog/                  # Main app
│   ├── models.py          # UserProfile, Post, Comment, Tag
│   ├── views.py           # All view logic
│   ├── forms.py           # RegisterForm, PostForm, CommentForm
│   ├── urls.py            # App URL patterns
│   └── admin.py           # Admin registration
├── config/                # Django project config
│   ├── settings.py
│   └── urls.py
├── templates/             # All HTML templates
│   ├── base.html
│   ├── home.html
│   ├── post_detail.html
│   ├── post_form.html
│   ├── my_posts.html
│   ├── profile.html
│   ├── delete_post.html
│   ├── register.html
│   └── registration/
│       ├── login.html
│       └── logged_out.html
├── static/
│   └── css/style.css      # Custom styles
├── media/                 # Uploaded files
├── manage.py
├── requirements.txt
└── setup.sh
```

---

## 🔑 URL Routes

| URL | View | Description |
|---|---|---|
| `/` | `home` | Blog feed with tag filter & pagination |
| `/post/new/` | `create_post` | Create a new post (auth required) |
| `/post/<slug>/` | `post_detail` | View a post + comments |
| `/post/<slug>/edit/` | `edit_post` | Edit post (author only) |
| `/post/<slug>/delete/` | `delete_post` | Delete post (author only) |
| `/my-posts/` | `my_posts` | Author's own posts (with drafts) |
| `/profile/<username>/` | `profile` | Public profile page |
| `/tag/<slug>/` | `tag_filter` | Posts filtered by tag |
| `/register/` | `register` | Registration page |
| `/accounts/login/` | Django built-in | Login |
| `/accounts/logout/` | Django built-in | Logout |
| `/admin/` | Django admin | Admin panel |
