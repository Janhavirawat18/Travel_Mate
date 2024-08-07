# Travel_Mate
A simple swipe featured travel tinder using Python. 

Welcome to Travel Mate! This Python web application helps users find their ideal travel destinations by using a swipe left and swipe right feature, similar to Tinder. Multiple users can use the app simultaneously to discover their next travel adventure.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Google Maps API Integration](#google-maps-api-integration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- Swipe left to skip a travel destination.
- Swipe right to save a travel destination.
- Simultaneous use by multiple users.
- Integration with Google Maps API to display destinations.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **APIs**: Google Maps API

## Getting Started

### Prerequisites
To run this project locally, you need to have the following installed:
- [Python](https://www.python.org/downloads/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/installation/)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/travel_mate.git
    cd travel_mate
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Google Maps API Integration

### Setting Up Google Maps API

1. **Create a Google Cloud Project:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Click on "Select a project" and then "New Project" to create a new project.

2. **Enable Google Maps APIs:**
   - In the Google Cloud Console, navigate to the "APIs & Services" dashboard.
   - Click on "Enable APIs and Services" and search for "Maps JavaScript API".
   - Click on "Maps JavaScript API" and then "Enable".

3. **Create API Key:**
   - In the "APIs & Services" dashboard, click on "Credentials" in the left-hand menu.
   - Click on "Create credentials" and select "API key".
   - Copy the API key provided.

4. **Restrict API Key (Optional but recommended):**
   - In the "Credentials" page, click on your API key to edit it.
   - Under "API restrictions", select "Maps JavaScript API".
   - Under "Application restrictions", select "HTTP referrers (web sites)" and add your website or localhost.

5. **Add API Key to Project:**
   - Replace the placeholder API key in your `config.py` file with your actual API key.
   ```python
   # config.py
   GOOGLE_MAPS_API_KEY = 'YOUR_API_KEY'
   ```

## Usage
1. **Run the Flask Application:**
    ```bash
    python app.py
    ```
    Open your browser and go to `http://localhost:5000` to see the application in action.

2. **Swipe Left or Right:**
   - Swipe left to skip a destination.
   - Swipe right to save a destination.

## Contributing
We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to reach out if you have any questions or need further assistance. Happy traveling!

---

Replace `"YOUR_API_KEY"` with your actual Google Maps API key in the `config.py` file.
