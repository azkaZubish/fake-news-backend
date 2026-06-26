# Backend for Fake News Detection [Live](https://fake-news-backend-dg3k.onrender.com/)
A Flask-based backend API for a Fake News Detection system. The application uses a trained Machine Learning model to classify news articles as Real News, Fake News, or Uncertain News. Prediction results are stored in MongoDB Atlas, allowing the frontend dashboard to display detection history and statistics.

## Features
-Machine Learning based news classification
-REST API for news prediction
-MongoDB Atlas integration for persistent storage
-Detection history API
-Confidence score for each prediction
-Ready for deployment on Render
-Supports React frontend integration

## Technologies Used
-Python
-Flask
-Scikit-learn
-MongoDB Atlas
-PyMongo
-Render
-python-dotenv

## Project Background
This project was originally based on a collaborative starter project and has since been significantly extended and maintained by me.

Major contributions include:
-MongoDB Atlas integration
-Persistent prediction history
-Detection History API
-Backend support for dashboard statistics
-Render deployment configuration
-Frontend-backend integration
-General maintenance and feature enhancements

## Backend Setup

### Clone the repository:
```bash
git clone <repository-url>
cd fake-news-detection-backend
```
### Install Dependencies:
```bash
pip install -r requirements.txt
```
### Create a .env file:
```bash
MONGO_URI=your_mongodb_connection_string
```
### Run Backend
```bash
python app.py
```
### Backend runs on:
```bash
http://localhost:5000
```
## API Endpoints
### Predict News
POST /predict
Analyzes a news article and stores the prediction in MongoDB.

### Get Detection History
GET /history
Returns previously analyzed news articles and their predictions.

### Future Improvements
-JWT authentication
-User-specific prediction history
-Pagination for history endpoint
-Docker support
-Automated testing
-CI/CD pipeline

## Related Project
Frontend Repository: [https://github.com/azkaZubish/fake-news-detection](https://github.com/azkaZubish/fake-news-detection)
