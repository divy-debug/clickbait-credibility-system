# 📰 HEADLINE LAB
### Clickbait & Credibility Scoring System

<p align="center">
  <strong>Does it pass the label test?</strong><br>
  An intelligent news analysis application that helps users examine clickbait headlines and assess news credibility.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--learn-F7931E?logo=scikitlearn&logoColor=white" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Environment-uv-6C3FC5" alt="uv">
</p>

---

## 💡 About the Project

**Headline Lab** is a machine-learning-powered application designed to help users analyze potentially misleading headlines and evaluate the credibility of news articles.

Inspired by the concept of nutritional labels on food packaging, Headline Lab generates a **credibility label** for submitted news content.

Users provide an article headline and its corresponding text. The application processes the input through two machine-learning models and presents the results in an intuitive, visual dashboard.

Instead of providing only a binary fake-or-real classification, Headline Lab combines prediction scores with additional content indicators to give users a more informative view of the submitted news.

> **Our idea:** Read the label before you share.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🎯 Clickbait Detection | Identifies potentially clickbait-style headlines. |
| 📰 News Credibility Prediction | Estimates whether an article is likely to be fake or real. |
| 📊 Overall Credibility Score | Displays a consolidated credibility score out of 100. |
| 🔍 Clickbait Wording | Highlights the presence of clickbait-related language. |
| 📝 Headline-Article Consistency | Provides an indicator of how well the article supports its headline. |
| 📚 Source Indicators | Checks for named sources in the submitted content. |
| 🎭 Tone Analysis | Provides an indicator of calm or neutral language. |
| 📄 Report-Style Analysis | Checks whether the writing resembles a news report. |
| 🎨 Visual Results | Presents verdicts, metrics, progress bars, and color-coded indicators. |
| ⚡ API Integration | Connects the frontend to the machine-learning backend through FastAPI. |

---

## 🧠 Machine Learning Methodology

The project uses two independent machine-learning pipelines for text classification.

### 1. Clickbait Detection Model

**Dataset:** Webis Clickbait-17

The clickbait detection model analyzes headline language and linguistic patterns to distinguish clickbait headlines from non-clickbait headlines.

**Methodology:**

- Text cleaning and preprocessing.
- TF-IDF vectorization using unigram and bigram features.
- Handcrafted linguistic feature extraction.
- Feature scaling using `StandardScaler`.
- Classification using class-balanced Logistic Regression.

**Handcrafted features include:**

- Exclamation and question mark counts.
- Pronoun usage.
- Uppercase character ratio.
- Headline word and character counts.
- Curiosity-inducing phrases.
- Superlative indicators.

### 2. News Credibility Model

**Dataset:** ISOT Fake News Dataset

The credibility model analyzes headline and article text to estimate whether the submitted news content belongs to the fake or real news category.

**Methodology:**

- Text preprocessing and cleaning.
- TF-IDF-based text representation.
- Logistic Regression classification.
- Prediction probabilities for fake and real news.

### 3. Additional Content Indicators

Alongside the machine-learning predictions, the application performs additional quick checks to provide more context about the submitted article.

These include:

- Whether the article supports its headline.
- Whether named sources are present.
- Whether the language is calm and neutral.
- Whether the writing resembles a report.

These indicators complement the model predictions; they should not be interpreted as independent factual verification.

---

## 🏗️ System Architecture

```text
                   USER
                     |
                     v
             STREAMLIT FRONTEND
                (Headline Lab)
                     |
                     v
              FASTAPI BACKEND
                     |
                     v
              ANALYSIS PIPELINE
                     |
             +-------+-------+
             |               |
             v               v
       CLICKBAIT MODEL   CREDIBILITY MODEL
             |               |
             v               v
       CLICKBAIT SCORE   CREDIBILITY SCORE
             |               |
             +-------+-------+
                     |
                     v
              ADDITIONAL CHECKS
                     |
                     v
               RESULTS PANEL
                     |
                     v
             VISUAL CREDIBILITY
                   LABEL
```

---

## 🖥️ Application Interface

The Headline Lab interface is designed around a simple two-panel layout.

### Input Panel

Users can enter:

- Article headline.
- Full article text.

### Credibility Facts Panel

The results panel displays:

- Overall credibility score.
- Clickbait wording indicator.
- Article-headline support indicator.
- Named-source indicator.
- Calm and neutral tone indicator.
- Report-style writing indicator.

The interface uses visual scores, progress bars, and color-coded verdicts to make the results easier to understand.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python 3.12 |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Text Representation | TF-IDF |
| Feature Scaling | StandardScaler |
| Model Serialization | Joblib |
| Backend Framework | FastAPI |
| Frontend Framework | Streamlit |
| API Server | Uvicorn |
| Testing | Pytest |
| Environment & Dependency Management | uv |
| Development Tools | VS Code, Jupyter Notebook |

---

## 📂 Project Structure

```text
clickbait-credibility-system/
│
├── api/
│   ├── main.py
│   └── __pycache__/
│
├── data/
│   ├── processed/
│   │   ├── clickbait.csv
│   │   ├── credibility_clean.csv
│   │   └── isot.csv
│   │
│   └── raw/
│
├── models/
│   ├── clickbait_model.joblib
│   ├── clickbait_scaler.joblib
│   ├── clickbait_tfidf.joblib
│   ├── credibility_model.joblib
│   └── credibility_tfidf.joblib
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_clickbait_model.ipynb
│   └── 03__credibility_model.ipynb
│
├── pages/
│   ├── 1_How_it_works.py
│   └── 2_History.py
│
├── src/
│   ├── clickbait_predictor.py
│   ├── credibility_predictor.py
│   ├── pipeline.py
│   └── prepare_clickbait.py
│
├── tests/
│   ├── test_api.py
│   ├── test_clickbait_predictor.py
│   └── test_pipeline.py
│
├── .gitignore
├── .python-version
├── app.py
├── components.py
├── demo.py
├── main.py
├── pyproject.toml
├── README.md
└── uv.lock
```

---

## ⚙️ Installation & Setup

### Prerequisites

Make sure you have the following installed:

- Python 3.12
- uv
- Git

### 1. Clone the repository

```bash
git clone https://github.com/divy-debug/clickbait-credibility-system.git
```

Navigate into the project directory:

```bash
cd clickbait-credibility-system
```

### 2. Install dependencies

Install the project dependencies using uv:

```bash
uv sync
```

### 3. Start the FastAPI Backend

Open a terminal in the project root and run:

```bash
uv run uvicorn api.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### 4. Start the Streamlit Frontend

Open a **second terminal** in the project root and run:

```bash
uv run streamlit run app.py
```

The frontend will usually be available at:

```text
http://localhost:8501
```

**Important:** Keep both terminals running while using the application. The Streamlit frontend communicates with the FastAPI backend to obtain the machine-learning predictions.

---

## 🔌 API Endpoints

The FastAPI backend provides the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Checks whether the backend is running. |
| `POST` | `/predict` | Analyzes a submitted headline and article text. |

### Example Prediction Request

```json
{
  "headline": "Example news headline",
  "article_text": "Example article content goes here."
}
```

---

## 🧪 Testing

The project includes automated tests for the API, clickbait predictor, and analysis pipeline.

Run the test suite from the project root:

```bash
uv run pytest
```

---

## 👥 Team Members & Contributions

| Team Member | Roll Number | Role & Contribution |
|---|---|---|
| **Divyanka Agrawal** | 25156085 | **Primary Author & Team Leader** — Developed both machine-learning models, including dataset selection, data cleaning, preprocessing, exploratory data analysis, feature engineering, model training, evaluation, and artifact serialization. |
| **Tuhin Das** | 25051596 | **Backend Developer** — Implemented the FastAPI backend, configured CORS using CORSMiddleware, and worked on `/health` and `/predict` endpoint tests. |
| **Jigyansa Rout** | 26155453 | **Frontend Developer** — Designed and developed the Streamlit interface, including headline and article input and visual presentation of prediction results. |
| **Manya Thaker** | 2605948 | **Results & Visualization** — Implemented result displays, Streamlit metrics, progress bars, color-coded verdict alerts, and explanations behind predictions. |

---

## 📚 Datasets & Acknowledgements

This project uses the following datasets for machine-learning experimentation:

- **Webis Clickbait-17** — Used for clickbait headline classification.
- **ISOT Fake News Dataset** — Used for fake and real news classification.

The datasets are used for academic and educational purposes. Please refer to their original sources for licensing and usage conditions.

---

## ⚠️ Limitations & Disclaimer

- Predictions are based on patterns learned from the training datasets.
- A high credibility score does not guarantee that an article is factually correct.
- A low credibility score does not independently prove that an article is fake.
- Model performance may vary across news sources, topics, and writing styles.
- The additional content indicators are preliminary checks, not comprehensive fact-checking mechanisms.
- The application is intended as an assistive analysis tool, not a replacement for professional fact-checking.

Users should independently verify important claims using reliable sources.

---

## 🎯 Project Objective

The objective of Headline Lab is to demonstrate how machine learning and natural language processing can be applied to identify potentially misleading headlines and estimate news credibility through an integrated, interactive, and user-friendly application.

---

<p align="center">
  <strong>HEADLINE LAB</strong>
  <br>
  <i>Read the label before you share.</i>
  <br><br>
  Built with Python, Machine Learning & NLP.
</p>