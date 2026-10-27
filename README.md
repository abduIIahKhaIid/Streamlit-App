# Diabetes Risk Predictor

A full-stack machine-learning demo that estimates diabetes risk from eight patient measurements. A FastAPI service loads a trained K-Nearest Neighbours (KNN) pipeline, while a responsive Streamlit interface collects inputs and presents the prediction in a clear, user-friendly format.

> [!IMPORTANT]
> This project is for education and demonstration only. It is not a medical device, diagnosis, or validated clinical risk score. Always consult a qualified healthcare professional for medical advice.

## Highlights

- Polished, responsive Streamlit interface with guided inputs and helpful descriptions
- FastAPI backend with health and prediction endpoints
- Scikit-learn pipeline combining feature scaling with a five-neighbour KNN classifier
- Input validation through Pydantic request models
- Clear success, risk, loading, and connection-error states
- Ready-to-use Render configuration for backend deployment
- Separate frontend and API architecture suitable for cloud deployment

## Architecture

```text
Patient input
     │
     ▼
Streamlit UI (streamlit_app.py)
     │  POST /predict
     ▼
FastAPI service (main.py)
     │
     ▼
Saved scikit-learn pipeline (model.pkl)
     │
     ▼
Prediction label + neighbour-vote confidence
```

The Streamlit application does not load the model directly. It sends a JSON request to FastAPI, and FastAPI performs the prediction using `model.pkl`.

## Project Structure

| File | Purpose |
| --- | --- |
| `streamlit_app.py` | Responsive web interface and API client |
| `main.py` | FastAPI application exposing health and prediction routes |
| `train_model.py` | Trains and saves the KNN classification pipeline |
| `model.pkl` | Pretrained scikit-learn pipeline used by the API |
| `diabetes.csv` | Pima Indians Diabetes dataset used for training |
| `requirements.txt` | Python dependencies for the frontend, API, and model |
| `render.yaml` | Render Blueprint configuration for the FastAPI service |
| `.python-version` | Python version selection for compatible deployments |

## Model Inputs

The model expects these eight values in the same order used during training:

| Feature | Description |
| --- | --- |
| `Pregnancies` | Number of previous pregnancies |
| `Glucose` | Plasma glucose concentration |
| `BloodPressure` | Diastolic blood pressure in mm Hg |
| `SkinThickness` | Triceps skin-fold thickness in mm |
| `Insulin` | Two-hour serum insulin measurement |
| `BMI` | Body mass index |
| `DiabetesPedigreeFunction` | Dataset score representing family history of diabetes |
| `Age` | Age in years |

The training pipeline applies `StandardScaler` before `KNeighborsClassifier(n_neighbors=5)`. The displayed confidence is the fraction of the five nearest neighbours that voted for the predicted class; it is not a calibrated medical probability.

## Local Setup

### 1. Create a virtual environment

From the project directory in Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell prevents activation, allow scripts for the current terminal session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 2. Prepare the model

A pretrained `model.pkl` is included. To retrain it from `diabetes.csv`, run:

```powershell
python train_model.py
```

Run the command from the project root so the script can locate the dataset and save the model in the expected location.

### 3. Start the FastAPI backend

In the first terminal:

```powershell
python -m uvicorn main:app --reload
```

The API is available at:

- Health check: `http://127.0.0.1:8000/`
- Interactive API docs: `http://127.0.0.1:8000/docs`
- Prediction endpoint: `http://127.0.0.1:8000/predict`

### 4. Start the Streamlit frontend

Open a second terminal, activate the same virtual environment, and run:

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run streamlit_app.py
```

Streamlit normally opens `http://localhost:8501`. Keep the FastAPI terminal running while using the interface.

## API Reference

### `GET /`

Returns the API status and indicates whether the model is loaded.

Example response:

```json
{
  "status": "running",
  "model_loaded": true
}
```

### `POST /predict`

Example request body:

```json
{
  "Pregnancies": 2,
  "Glucose": 120,
  "BloodPressure": 70,
  "SkinThickness": 20,
  "Insulin": 79,
  "BMI": 25.0,
  "DiabetesPedigreeFunction": 0.5,
  "Age": 30
}
```

Example response shape:

```json
{
  "prediction": 0,
  "result_label": "Not Diabetic",
  "confidence": 0.8
}
```

`prediction` is `1` for **Diabetic** and `0` for **Not Diabetic**.

## Configuration

The Streamlit frontend reads the backend base URL from the `API_URL` environment variable. When the variable is not set, it defaults to `http://127.0.0.1:8000` for local development.

PowerShell example:

```powershell
$env:API_URL = "https://your-api-service.onrender.com"
python -m streamlit run streamlit_app.py
```

Use the base URL only—do not add `/predict`, because the application adds that route automatically.

## Deployment

### Backend on Render

Connect the repository to Render and create a Web Service with these settings:

| Setting | Value |
| --- | --- |
| Runtime | Python 3 |
| Build command | `pip install -r requirements.txt` |
| Start command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Health check path | `/` |

The included `render.yaml` provides the same service configuration for a Blueprint deployment. After deployment, open the service root and `/docs` to confirm that the API is available.

### Frontend on Streamlit Community Cloud

Create an app from the repository with `streamlit_app.py` as the main file. In the app's **Secrets** settings, add the deployed FastAPI base URL as a root-level value named `API_URL`. Streamlit exposes root-level secrets as environment variables, which the application reads automatically.

```text
API_URL = "https://your-api-service.onrender.com"
```

The API must use a public HTTPS URL in cloud deployments. A local address such as `127.0.0.1` points to the Streamlit host itself and cannot reach your computer.

## Troubleshooting

| Problem | Resolution |
| --- | --- |
| `py` is not recognized | Install Python 3.11 or create the environment with `python -m venv .venv` |
| PowerShell blocks activation | Use the process-scoped execution policy command shown in Local Setup |
| `model.pkl` is missing | Run `python train_model.py` from the project root |
| Streamlit shows the service-unavailable warning | Start FastAPI and verify that `API_URL` contains the correct base URL |
| Cloud frontend cannot connect | Use the deployed HTTPS API URL instead of `localhost` or `127.0.0.1` |
| First cloud prediction is slow | Free hosting services may pause inactive applications and need time to wake up |
| Model fails to load after dependency changes | Recreate `model.pkl` using the installed scikit-learn version |

## Technology Stack

- **Frontend:** Streamlit
- **API:** FastAPI and Uvicorn
- **Validation:** Pydantic
- **Machine learning:** scikit-learn, NumPy, pandas, and joblib
- **Deployment:** Render and Streamlit Community Cloud

## Responsible Use

This model is trained on a small historical dataset and does not account for the full clinical context required to assess diabetes. Zero values in some dataset fields may also represent missing measurements. Do not use its output to begin, stop, or change medical treatment.
