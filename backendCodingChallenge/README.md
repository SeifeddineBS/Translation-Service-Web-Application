# # # Project Overview

# This project is a Django-based web application that provides translation services. 
# The application allows users to sign up, log in, and access a set of APIs to translate text 
# or HTML content into different languages using the Google Cloud Translation API. 
# The application is deployed at [Your Deployed Website Link].

# # # Features

# - **User Authentication**: Users can sign up, log in, and log out. Authentication is handled using session and token-based mechanisms.
# - **Translation Services**: Users can submit plain text or HTML content for translation into supported languages.
# - **Translation Management**: Users can view, list, and delete their translation requests.

# # # API Endpoints

# ### 1. **User Signup**
# - **URL**: `/signup/`
# - **Method**: `POST`
# - **Request Body**:
# ```json
# {
#     "username": "string",
#     "email": "string",
#     "password": "string"
# }
# ```
# - **Response**:
# - On success: `{ "token": "your_token", "user": { "username": "string", "email": "string" } }`
# - On failure: Validation errors.

# ### 2. **User Login**
# - **URL**: `/login/`
# - **Method**: `POST`
# - **Request Body**:
# ```json
# {
#     "username": "string",
#     "password": "string"
# }
# ```
# - **Response**:
# - On success: `{ "token": "your_token", "user": { "username": "string", "email": "string" } }`
# - On failure: `{"missing user"}`.

# ### 3. **User Logout**
# - **URL**: `/logout/`
# - **Method**: `GET`
# - **Response**: `{ "User logged out" }`

# ### 4. **List and Create Translations**
# - **URL**: `/translation/`
# - **Method**: `GET` or `POST`
# - **GET Parameters**:
# - `user` (optional): Filter translations by user ID.
# - **POST Request Body**:
# ```json
# {
#     "original_text": "string",
#     "target_language": "string",
#     "type": "HTML" or "PLAIN_TEXT"
# }
# ```
# - **Response**:
# - On GET: `{ "Translations": [ { ...translation_data... }, ... ] }`
# - On POST: Created translation object or validation errors.

# ### 5. **Translation Details and Deletion**
# - **URL**: `/translation/<id>/`
# - **Method**: `GET` or `DELETE`
# - **Response**:
# - On GET: Translation object.
# - On DELETE: Status 204 (No Content).

# ### 6. **Test Token**
# - **URL**: `/test-token/`
# - **Method**: `GET`
# - **Response**: `"passed!"`

# ### 7. **Public View**
# - **URL**: `/public-view/`
# - **Method**: `GET`
# - **Response**: `"This view does not require authentication."`

# # # Environment Setup

# ### Prerequisites
# - Python 3.x
# - Django
# - Django Rest Framework
# - Google Cloud Translate API

# ### Installation

# 1. **Clone the repository**:
# ```bash
# git clone https://github.com/your-repo-link.git
# cd your-repo-link
# ```

# 2. **Set up a virtual environment**:
# ```bash
# python3 -m venv venv
# source venv/bin/activate
# ```

# 3. **Install the required packages**:
# ```bash
# pip install -r requirements.txt
# ```

# 4. **Set up environment variables**:
# - Create a `.env` file in the project root directory with the following content:
# ```
# GOOGLE_APPLICATION_CREDENTIALS_B64=<Your Google Credentials in Base64>
# ```

# - **Note**: The `GOOGLE_APPLICATION_CREDENTIALS_B64` can be found at [Your Credential Link].

# 5. **Apply migrations**:
# ```bash
# python manage.py migrate
# ```

# 6. **Create a superuser** (optional):
# ```bash
# python manage.py createsuperuser
# ```

# 7. **Run the development server**:
# ```bash
# python manage.py runserver
# ```

# 8. **Access the application**:
# - Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to test the application locally.

# # # Deployment

# The application is deployed at [Your Deployed Website Link]. You can access the public APIs and test the application through this link.

# # # Testing the APIs

# You can test the APIs using tools like [Postman](https://www.postman.com/) or [cURL](https://curl.se/). Ensure that you provide the required authentication token in the headers for protected endpoints.

# # # Contact

# For any issues or questions, please contact [Your Name] at [Your Email Address].

# ---
# **Note**: Ensure to replace placeholders like `Your Deployed Website Link`, `your-repo-link`, `Your Google Credentials in Base64`, etc., with the actual values relevant to your project.
