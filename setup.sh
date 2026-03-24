#!/bin/bash
# ============================================================
# Student Blog Platform — One-Click Setup Script
# Run: bash setup.sh
# ============================================================

echo ""
echo "🚀 Setting up Student Blog Platform..."
echo ""

# 1. Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet

# 3. Run migrations
echo "🗃️  Running migrations..."
python manage.py makemigrations
python manage.py migrate

# 4. Create superuser (optional)
echo ""
echo "👤 Create a superuser for admin access? (y/n)"
read -r CREATE_SU
if [ "$CREATE_SU" = "y" ] || [ "$CREATE_SU" = "Y" ]; then
  python manage.py createsuperuser
fi

# 5. Done
echo ""
echo "✅ Setup complete!"
echo ""
echo "▶  Start the server with:"
echo "   source .venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "🌐 Then open: http://127.0.0.1:8000"
echo ""
