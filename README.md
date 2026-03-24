# Health Prediction & Care Management System

A full-stack application for predictive health risk analysis, insurance recommendations, and preventive care management.

## Project Structure

```
├── backend/          # Flask API (Deploy to Render)
│   ├── app.py
│   ├── requirements.txt
│   ├── render.yaml
│   └── .env.example
├── src/             # React Frontend (Deploy to Vercel)
│   ├── App.tsx
│   ├── config.ts
│   └── ...
├── package.json
├── vercel.json
└── .env.example
```

## Deployment

### Backend (Render)

1. Push code to GitHub
2. Create new Web Service on [Render](https://dashboard.render.com/)
3. Set root directory to `backend`
4. Use build command: `pip install -r requirements.txt`
5. Use start command: `gunicorn app:app`
6. Add environment variable `CORS_ORIGINS` with your Vercel URL

### Frontend (Vercel)

1. Push code to GitHub
2. Import project on [Vercel](https://vercel.com)
3. Framework preset: Vite
4. Add environment variable:
   - `VITE_API_BASE_URL`: Your Render backend URL (e.g., `https://your-app.onrender.com`)
5. Deploy

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
python app.py
```

### Frontend
```bash
npm install
cp .env.example .env
npm run dev
```

## Environment Variables

### Backend (.env)
```
PORT=5000
FLASK_ENV=development
CORS_ORIGINS=http://localhost:5173
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:5000
```

## Tech Stack

- Frontend: React + TypeScript + Vite + TailwindCSS
- Backend: Flask + scikit-learn
- Deployment: Vercel (Frontend) + Render (Backend)
