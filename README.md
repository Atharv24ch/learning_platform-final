# AI Learning Platform 🎓

A personalized learning platform powered by AI that generates custom roadmaps, curates YouTube videos, and creates interactive quizzes to help users master any subject.

![Next.js](https://img.shields.io/badge/Next.js-16.0-black?logo=next.js)
![Django](https://img.shields.io/badge/Django-5.2-green?logo=django)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?logo=typescript)
![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)

## ✨ Features

### 🗺️ AI-Powered Roadmaps
- Generate personalized learning paths based on your goals and skill level
- Structured curriculum with lessons, topics, and milestones
- Track your progress through each roadmap

### 📚 Smart Lessons
- AI-curated content for each lesson
- YouTube video integration for visual learning
- Organized by difficulty and topic

### 🎯 Interactive Quizzes
- AI-generated quizzes to test your knowledge
- Instant feedback and scoring
- Track your quiz performance over time

### 👤 User Dashboard
- Beautiful, modern dashboard with learning stats
- View completed lessons and quiz scores
- Quick actions for creating roadmaps and taking quizzes
- Recent activity timeline

### 🔐 Authentication & Profile
- Secure user registration and login (JWT-based)
- Profile dropdown with settings and help
- Persistent authentication state

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **HTTP Client**: Axios

### Backend
- **Framework**: Django 5.2
- **API**: Django REST Framework
- **Authentication**: JWT (Simple JWT)
- **Database**: PostgreSQL (Neon)
- **AI Integration**: OpenAI API
- **Video Search**: YouTube Data API

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.13+
- PostgreSQL database (or Neon account)
- OpenAI API key
- YouTube Data API key

### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/Atharv24ch/learning_platform-final.git
cd learning_platform-final
```

#### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env file (or update existing one)
# Add your environment variables:
# - DATABASE_URL
# - OPENAI_API_KEY
# - YOUTUBE_API_KEY

# Run migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Start the Django development server
python manage.py runserver
```

The backend will run at `http://localhost:8000`

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local

# Start the Next.js development server
npm run dev
```

The frontend will run at `http://localhost:3000`

## 📁 Project Structure

```
learning_platform/
├── backend/
│   ├── learning_platform/      # Django project settings
│   ├── users/                  # User authentication & profiles
│   ├── courses/                # Roadmaps, lessons, AI generation
│   ├── quizzes/                # Quiz generation & submission
│   └── manage.py
│
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── components/     # Reusable components (Navbar, etc.)
│   │       ├── context/        # Auth context
│   │       ├── dashboard/      # Dashboard page
│   │       ├── login/          # Login page
│   │       ├── register/       # Registration page
│   │       ├── roadmap/        # Roadmap generation & display
│   │       ├── lessons/        # Lessons page
│   │       └── quiz/           # Quiz pages
│   ├── lib/                    # API utilities
│   └── public/                 # Static assets
│
└── README.md
```

## 🔑 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@host:port/database
OPENAI_API_KEY=your_openai_api_key
YOUTUBE_API_KEY=your_youtube_api_key
SECRET_KEY=your_django_secret_key
DEBUG=True
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## 📝 API Endpoints

### Authentication
- `POST /api/users/register/` - Register a new user
- `POST /api/users/login/` - Login and get JWT tokens

### Roadmaps
- `POST /api/courses/generate/` - Generate AI roadmap
- `GET /api/courses/roadmaps/` - List user's roadmaps
- `GET /api/courses/roadmaps/{id}/` - Get roadmap details

### Lessons
- `GET /api/courses/lessons/` - List lessons
- `GET /api/courses/lessons/{id}/` - Get lesson details

### Quizzes
- `POST /api/quizzes/generate/` - Generate quiz for a lesson
- `POST /api/quizzes/submit/` - Submit quiz answers
- `GET /api/quizzes/{id}/` - Get quiz details

## 🎨 Design Features

- Modern gradient backgrounds
- Smooth animations and transitions
- Responsive design for all devices
- Card-based layouts
- Interactive dropdowns and modals
- Professional color scheme (blue, purple, green accents)

## 🔒 Security

- JWT-based authentication
- CORS configuration for frontend-backend communication
- Password hashing with Django's built-in authentication
- Secure HTTP-only token storage

## 🚧 Development

### Running Tests
```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests (if configured)
cd frontend
npm test
```

### Database Migrations
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Atharv Choudhary**
- GitHub: [@Atharv24ch](https://github.com/Atharv24ch)
- Email: atharvchoudhary44@gmail.com

## 🙏 Acknowledgments

- OpenAI for GPT API
- YouTube Data API
- Next.js and Django communities
- All contributors and supporters

---

Built with ❤️ using Next.js, Django, and AI
