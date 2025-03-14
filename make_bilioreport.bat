:: Creation: F. Bertin 2024-05-26
:: Refactoring: A. Chabli 2024-06-17

@echo off 
Title BiblioMeter.exe making

:: Setting useful editing parameters
set "TAB=   "

:: Setting useful directories
set "working_dir=%userprofile%\Pyvenv\BiblioReport"

:: Setting the name of the log file to debbug the executable making
set "LOG=%working_dir%\log.txt"

:: Creating a venv
:: adapted from https://stackoverflow.com/questions/45833736/how-to-store-python-version-in-a-variable-inside-bat-file-in-an-easy-way?noredirect=1
echo Creating a virtual environment
cd %working_dir%
set "python_dir=%userprofile%\PyVersions\python3.9.7"
if exist %python_dir% ( 
    echo %TAB%%python_dir% will be used to build the venv
    echo:
    %python_dir%\python -m venv venv
) else (
    echo %TAB%Unable to access %python_dir% so we will use the default python version
    echo:
    python -m venv venv)
    
:: Upgrading pip version
echo Upgrading pip version
venv\Scripts\python.exe -m pip install --upgrade pip
echo %TAB%Upgraded pip to latest version
echo:

:: Activating the venv
echo Activating the virtual environment
set "virtual_env=%working_dir%\venv"
call %virtual_env%\Scripts\activate.bat

:: Getting and displaying the python version used
for /F "tokens=* USEBACKQ" %%F in (`python --version`) do (set var=%%F)
if exist %working_dir%\venv (
    echo A virtual environment created with %var% and activated >> %LOG%
    echo %TAB%A virtual environment created with %var% and activated
    echo:
) else (
    echo Unable to create a virtual environment >> %LOG%
    echo %TAB%Unable to create a virtual environment
    GOTO FIN)

:: Installing packages
echo Installing BiblioParsing package
echo:
pip install git+https://github.com/TickyWill/BiblioParsing
cls
echo The package BiblioParsing successfully installed >> %LOG%
echo:
echo The package BiblioParsing successfully installed
echo:
echo Installing BiblioMeter packages
echo:
pip install git+https://github.com/TickyWill/BiblioMeter.git@collab-analysis-dev
cls
echo The package BiblioMeter successfully installed >> %LOG%
echo:
echo The BiblioMeter packages successfully installed
pip install git+https://github.com/Bertin-fap/BiblioReport
cls
echo The package BiblioReport successfully installed >> %LOG%
echo:
echo The BiblioMeter packages successfully installed
echo:
echo Installing required libraries
echo:
pip install -r %working_dir%\requirements.txt
cls
echo The required libraries successfully installed >> %LOG%
echo:
echo The required libraries successfully installed
echo:    

:: Getting the python program to launch the application
echo Getting the python program to launch the application
::set "PGM=%working_dir%\venv\Lib\site-packages\bmfuncts\ConfigFiles\app.py"
set "PGM=%working_dir%\app.py"
curl.exe https://raw.githubusercontent.com/Bertin-fap/BiblioReport/refs/heads/main/App.py -o %PGM%
set "HTML=%working_dir%\venv\Lib\site-packages\pyvis\templates\template.html"
curl.exe https://raw.githubusercontent.com/Bertin-fap/BiblioReport/refs/heads/main/template.html -o %HTML%