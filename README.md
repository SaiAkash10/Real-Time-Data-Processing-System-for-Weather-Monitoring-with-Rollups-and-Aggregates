# Real-Time Weather Monitoring System

### Overview

This application is a **Real-Time Data Processing System for Weather Monitoring**, designed to continuously retrieve weather data from the OpenWeatherMap API and provide summarized insights using rollups and aggregates. The system focuses on delivering essential weather parameters, visualizations, and alerting functionalities.

### Features

- **Real-Time Data Retrieval**: Continuously fetches weather data for major metros in India (Delhi, Mumbai, Chennai, Bangalore, Kolkata, Hyderabad) every 5 minutes.
- **Data Processing**: Converts temperature values from Kelvin to Celsius (or Fahrenheit based on user preference) and calculates daily weather summaries.
- **Rollups and Aggregates**:
  - Daily aggregates: Average temperature, maximum temperature, minimum temperature, and dominant weather condition.
- **Alerting System**: User-configurable thresholds for temperature or specific weather conditions with alerts for breaches.
- **Visualizations**: Displays daily weather summaries, historical trends, and triggered alerts.

### Data Source

The system retrieves data from the [OpenWeatherMap API](https://openweathermap.org/). You need to sign up for a free API key to access the data. The API provides various weather parameters, including:

- **main**: Main weather condition (e.g., Rain, Snow, Clear)
- **temp**: Current temperature in Celsius
- **feels_like**: Perceived temperature in Celsius
- **dt**: Time of the data update (Unix timestamp)

### Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/weather-monitoring-system.git
   cd weather-monitoring-system
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   Ensure you have the necessary packages by running:
   ```bash
   pip install -r requirements.txt
   ```

   Dependencies may include:
   - Flask
   - Matplotlib
   - SQLite3 (built-in with Python)
   - Requests (for API calls)

4. **Environment Variables**:
   Set your OpenWeatherMap API key as an environment variable:
   ```bash
   export OPENWEATHER_API_KEY='your_api_key'  # On Windows use `set` instead of `export`
   ```

5. **Database Setup**:
   Ensure you have SQLite set up for storing daily weather summaries. The database file will be created automatically upon the first run.

6. **Run the Application**:
   Start the Flask server:
   ```bash
   python app.py
   ```

### Usage

- **Dashboard**: Access the main dashboard at `http://127.0.0.1:5000/` to view real-time weather data and summaries.
- **Alerts**: Configure alert thresholds at the `/alerts` route.
- **Visualizations**: Generate visualizations by selecting a city from the dropdown menu in the navigation bar.

### Testing

- Ensure the system connects to the OpenWeatherMap API with a valid API key.
- Test data retrieval at configurable intervals.
- Validate temperature conversions and daily summaries.
- Verify alert thresholds are triggering correctly based on simulated weather data.

### Bonus Features

- Extend support for additional weather parameters (e.g., humidity, wind speed) and incorporate them into rollups and aggregates.
- Implement functionalities for weather forecasts and summaries based on predicted conditions.

### Artifacts to be Submitted

- **Codebase**: Hosted on GitHub.
- **Comprehensive README**: Including build instructions, design choices, and any additional features.
- **Dependencies**: List of dependencies required for setting up and running the application (Docker or Podman containers can also be included).
