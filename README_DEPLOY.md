# msa-mefa

Aplikacja web do Measurement System Analysis (MSA) – **Gage R&R**:
- Metody: **ANOVA** oraz **Average & Range**
- Ręczne wprowadzanie danych (10 próbek × 3 serie × 3 operatorów)
- Zapis badań do bazy
- Generowanie **PDF** raportu
- Frontend serwowany przez FastAPI (jeden adres URL)

## Uruchomienie lokalne

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./run.sh  # Windows: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm i
npm run build  # skompiluje do dist/, ale w Dockerze i tak zbuduje się automatycznie
```

## Deploy – Render.com (Docker)
1. Załóż konto i podepnij repo (GitHub).
2. Utwórz **PostgreSQL** na Render i skopiuj `DATABASE_URL`.
3. **New → Web Service** → wybierz repo → **Environment: Docker**.
4. Ustaw zmienne środowiskowe:
   - `DATABASE_URL=postgresql://...` (z kroku 2)
   - `PYTHONUNBUFFERED=1`
5. Zbuduje się i udostępni URL, np. `https://msa-mefa.onrender.com`.

## Deploy – Azure App Service (Docker)
1. Zbuduj obraz lokalnie:
   ```bash
   docker build -t msa-mefa:latest .
   ```
2. Zaloguj się do Azure i utwórz **Azure Container Registry (ACR)**, wypchnij obraz:
   ```bash
   az acr login --name <ACR_NAME>
   docker tag msa-mefa:latest <ACR_NAME>.azurecr.io/msa-mefa:latest
   docker push <ACR_NAME>.azurecr.io/msa-mefa:latest
   ```
3. Utwórz **Azure Database for PostgreSQL** (Flexible Server) i pobierz connection string (`DATABASE_URL`).
4. Utwórz **Web App for Containers** w Azure App Service:
   - **Image Source:** ACR → `msa-mefa:latest`
   - **App Settings:** dodaj `DATABASE_URL=postgresql://...`
   - Port kontenera: `8000`
5. Po uruchomieniu aplikacja będzie dostępna pod adresem Twojego Web App.

## Użycie
- Wejdź pod adres aplikacji → formularz wypełnij danymi → „Zapisz i analizuj”
- Przełącznik **ANOVA / Average & Range** wybiera metodę obliczeń
- Po analizie: przycisk **Pobierz PDF** wygeneruje raport
