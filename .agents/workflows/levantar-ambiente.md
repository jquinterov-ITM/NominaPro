---
description: levantar ambiente de desarrollo de NominaPro (Vue + FastAPI)
---

# Levantar ambiente de desarrollo

## Pasos

1. Terminal 1 (Backend):
   `ash
   cd backend
   ..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
   `
2. Terminal 2 (Frontend):
   `ash
   cd frontend
   npm run dev
   `
3. Verificar en navegador (localhost:5173).
