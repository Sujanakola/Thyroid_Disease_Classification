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

### Deployment on Render

1. Create a new account on [Render](https://render.com)
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Fill in the following details:
   - Name: thyroid-classification
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`
5. Click "Create Web Service"

## Environment Variables

- `SECRET_KEY`: Session encryption key (optional)
- `PORT`: Application port (default: 5000)

## Model Information

The application uses a trained machine learning model to classify thyroid conditions into four categories:
- Hyperthyroid
- Hypothyroid
- Negative (Normal)
- Sick

## License

MIT License

