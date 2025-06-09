# Thyroid Disease Classification Web App

A web-based application that uses machine learning to classify thyroid conditions based on laboratory test results and patient information.

## Features

- Analysis of thyroid hormone levels (TSH, T3, T4, etc.)
- Patient history consideration
- Detailed result explanation
- Mobile-responsive design
- Dark/light mode support

## Technical Stack

- Flask (Python web framework)
- scikit-learn (Machine learning)
- HTML/CSS/JavaScript (Frontend)
- Gunicorn (WSGI HTTP Server)

## Deployment Instructions

### Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

## Model Information

The application uses a trained machine learning model to classify thyroid conditions into four categories:
- Hyperthyroid
- Hypothyroid
- Negative (Normal)
- Sick
