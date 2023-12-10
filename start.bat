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
if not exist ".venv" (
    python -m venv .venv
    call .venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate
)

:: Open web page
start http://127.0.0.1:5000

echo Refresh the page after Litestar starts.
echo Starting Litestar...

:: Show message and run Litestar app
start litestar run -p 5000

:end
