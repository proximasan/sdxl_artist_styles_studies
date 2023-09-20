#!/bin/bash

# Function to terminate the Flask process when the script exits
cleanup() {
  kill -9 $APP_PID 2>/dev/null
}

# Attach the cleanup function to the EXIT signal
trap cleanup EXIT

# ASCII Art
echo "              ██████████                                            "
echo "            ██░░░░░░░░░░████                                        "
echo "          ██░░░░░░░░░░░░░░░░██                                      "
echo "        ██░░░░░░░░░░░░░░░░░░░██                                    "
echo "      ██░░░░░░██░░░░░░░░░░░░████                                    "
echo "    ██░░░░░░░░██░░████████░░██░░██                                  "
echo "    ██░░░░░░░░░░░░██░░░░░░██░░░░██                                  "
echo "  ████░░░░░░░░░░░░██░░░░░░██░░░░░░██                                "
echo "  ██░░░░░░░░░░░░░░██░░░░░░██░░░░░░░░██                              "
echo "██░░░░░░░░░░░░░░░░██░░░░████░░░░░░░░██                              "
echo "██░░░░░░░░░░░░░░░░░░██░░██░░░░░░░░░░██                              "
echo "██░░░░░░░░░░░░░░░░░░██░░██░░░░░░░░░░██                              "
echo "  ██░░░░░░░░░░░░░░░░░░██░░░░░░░░░░░░██                              "
echo "    ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                            "
echo "    ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████                        "
echo "    ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                      "
echo "    ██░░██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                    "
echo "    ██░░░░░░░░██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                  "
echo "    ████████████████████████████████████████████████                  "

# Check if Python 3 is installed
command -v python3 >/dev/null 2>&1 || {
    echo >&2 "Python 3 is required but it's not installed. Please install Python 3 and then run this script again.";
    exit 1;
}

# Function to detect the operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "mac"
    elif [[ "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Create a Python virtual environment only if it doesn't exist
if [ ! -d "venv" ]; then
  python3 -m venv venv
  source venv/bin/activate
  pip install Flask
else
  source venv/bin/activate
fi

# Run the app in the background
export FLASK_ENV=production
python app.py 2>&1 | awk '/\* Running on http:\/\/127.0.0.1:5000/ {print; exit} 1' &

# Get the process ID of the app
APP_PID=$!

# Give Flask some time to initialize
sleep 2

# Open the web page
os=$(detect_os)
if [[ "$os" == "linux" ]]; then
    xdg-open "http://127.0.0.1:5000"
elif [[ "$os" == "mac" ]]; then
    open "http://127.0.0.1:5000"
elif [[ "$os" == "windows" ]]; then
    start "http://127.0.0.1:5000"
fi

# Wait for the app to finish
wait $APP_PID
