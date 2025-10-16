# IATL (Intelligent Speech Translation Assistant)

**Status: In Development**

An intelligent assistant designed for real-time speech recognition and translation. This project aims to break down language barriers using modern machine learning and mobile technologies.

## 📖 About The Project

IATL is a cross-platform mobile application that allows users to speak in their native language and receive an instant audio and text translation in another language. It is built with a powerful Django backend for processing audio and a lightweight Cordova frontend for a seamless mobile user experience.

## ✨ Key Features (Planned)

  * **Real-Time Translation:** Fast speech recognition and instant translation.
  * **Multi-Language Support:** A flexible architecture designed to easily add new language pairs.
  * **Voice Input & Output:** Users can speak to the app and listen to the translated audio.
  * **Translation History:** Saves recent translations for easy access.
  * **Cross-Platform:** Built with Apache Cordova to run on both Android and iOS from a single codebase.

## 🛠️ Tech Stack

| Component | Technology | Repository Folder |
| :--- | :--- | :--- |
| **Backend** | Django, Django REST Framework, Python | `voice_assistant` |
| **Frontend**| Apache Cordova, HTML, CSS, JavaScript | `voice-translator`|
| **Database** | PostgreSQL (Production) / SQLite (Development) | - |
| **Speech & Translation APIs** | (e.g., Google Cloud Speech-to-Text, DeepL API) | - |

## 📁 Project Structure

The project is organized into two main repositories for a clear separation of concerns:

```
/IATL
|-- /voice_assistant/  (Django Backend)
|-- /voice-translator/ (Cordova Frontend)
```

## 🚀 Getting Started

To get a local copy up and running, you will need to set up both the backend and frontend services.

### 1\. Backend (`voice_assistant`)

**Prerequisites:**

  * Python 3.8+
  * Pip
  * Git

**Installation & Setup:**

1.  Clone the repository:

    ```bash
    git clone https://github.com/Janspitoy/IATL.git
    cd IATL/voice_assistant
    ```

2.  Create and activate a virtual environment:

    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4.  Set up your environment variables. Create a `.env` file in the `voice_assistant` root directory from the `.env.example` template and add your configuration:

    ```ini
    SECRET_KEY='your_secret_key'
    DEBUG=True
    # Add database settings and API keys for translation services
    ```

5.  Apply database migrations:

    ```bash
    python manage.py migrate
    ```

6.  Run the development server:

    ```bash
    python manage.py runserver
    ```

    The backend API will be available at `http://127.0.0.1:8000`.

### 2\. Frontend (`voice-translator`)

**Prerequisites:**

  * Node.js and npm
  * Apache Cordova CLI (`npm install -g cordova`)
  * Git
  * Android Studio / Xcode for platform-specific builds

**Installation & Setup:**

1.  Navigate to the frontend directory:

    ```bash
    cd IATL/voice-translator
    ```

2.  Install npm dependencies:

    ```bash
    npm install
    ```

3.  Add your target platform (e.g., Android):

    ```bash
    cordova platform add android
    ```

4.  Configure the backend API endpoint. In your frontend code (e.g., in a `www/js/config.js` file), set the API URL:

    ```javascript
    const API_URL = 'http://127.0.0.1:8000/api/'; // Use your computer's network IP for testing on a real device
    ```

5.  Run the application on an emulator or a connected device:

    ```bash
    cordova run android
    ```

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request


Project Link: [https://github.com/Janspitoy/IATL](https://github.com/Janspitoy/IATL)
