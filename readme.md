
# Database Uploader documentation
## Prerequisites
1. Install Python3 https://www.python.org/downloads/release/python-3106/

2. Run install.bat (for Windows) or ./install.sh (if you are on Linux/Mac) as Admin.

## Usage
Make  sure you generate service account creds from the Firebase console, rename it to "firebase.json" and put it in the "config" folder.

Put all your CSV files into the "csv" folder.


If you are on windows, just go to the folder where you cloned the repo. Double click the "run_app.bat" file and it will run the python app on a console window.

If you are on Linux or Mac just open the terminal. cd to the directory and run the command ``python3 app.py``

All of the functionality of the app is self explaimentory. Just run the app everything else is automated. 

You will need to run the "run_cache_checker.bat" to upload the data cached for usage limit. You can also set up this bat file to run every 24 hour to automatically upload any data cached if needed. Please refer to your OS instruction for the details.
