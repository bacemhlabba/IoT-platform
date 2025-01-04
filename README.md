# IoT Project

This repository contains a Flask project that serves web pages to display sensor data from Firebase and a local database. The project also includes functionality to update the LED state in the local database.

## Setup Instructions

### 1. Set up and run the Flask project

1. Clone the repository:
    ```bash
    git clonehttps://github.com/bacemhlabba/IoT-platform.git
    cd IoT-platform
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask app:
    ```bash
    ./run.sh
    ```

### 2. Create and configure the Firebase project

1. Go to the [Firebase Console](https://console.firebase.google.com/) and create a new project.

2. Add a new web app to the project and follow the instructions to register the app.

3. Download the  file from the Firebase Console and place it in the root directory of the project.

4. Update the  file with the Firebase configuration details.

### 3. Set up the local database

1. Create a new SQLite database file:
    ```bash
    sqlite3 local_database.db
    ```

2. Create the `sensor_data` table with the following fields:
    ```sql
    CREATE TABLE sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature TEXT,
        humidity TEXT,
        gas TEXT,
        led TEXT
    );
    ```

3. Insert some initial data into the `sensor_data` table:
    ```sql
    INSERT INTO sensor_data (temperature, humidity, gas, led) VALUES ('25', '60', 'Normal', 'OFF');
    ```

4. Close the SQLite database:
    ```bash
    .exit
    ```

## Running the App

1. Make sure the virtual environment is activated and the required dependencies are installed.

2. Run the Flask app:
    ```bash
    ./run.sh
    ```

3. Open a web browser and go to `http://127.0.0.1:5000/` to access the index page.

4. Use the navigation links to go to Page 1 and Page 2 to view the sensor data and update the LED state.
