@echo off
setlocal

:: ASCII Art
echo               ██████████                                            
echo             ██░░░░░░░░░░████                                        
echo           ██░░░░░░░░░░░░░░░░██                                      
echo         ██░░░░░░░░░░░░░░░░░░░██                                    
echo       ██░░░░░░██░░░░░░░░░░░░████                                    
echo     ██░░░░░░░░██░░████████░░██░░██                                  
echo     ██░░░░░░░░░░░░██░░░░░░██░░░░██                                  
echo   ████░░░░░░░░░░░░██░░░░░░██░░░░░░██                                
echo   ██░░░░░░░░░░░░░░██░░░░░░██░░░░░░░░██                              
echo ██░░░░░░░░░░░░░░░░██░░░░████░░░░░░░░██                              
echo ██░░░░░░░░░░░░░░░░░░██░░██░░░░░░░░░░██                              
echo ██░░░░░░░░░░░░░░░░░░██░░██░░░░░░░░░░██                              
echo   ██░░░░░░░░░░░░░░░░░░██░░░░░░░░░░░░██                              
echo     ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                            
echo     ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████                        
echo     ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                      
echo     ██░░██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                    
echo     ██░░░░░░░░██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                  
echo     ████████████████████████████████████████████████                  

:: Check for Python 3
where python 1>nul 2>nul
if %errorlevel% neq 0 (
    echo Python 3 is required but it's not installed. Please install Python 3 and then run this script again.
    goto :EOF
)

:: Create Python virtual environment if it doesn't exist
if not exist "venv" (
    python -m venv venv
    call venv\Scripts\activate
    pip install Flask
) else (
    call venv\Scripts\activate
)

:: Run Flask app
set FLASK_ENV=production
start /b python app.py

:: Give Flask some time to initialize
timeout /t 2 /nobreak

:: Open web page
start http://127.0.0.1:5000

:end
