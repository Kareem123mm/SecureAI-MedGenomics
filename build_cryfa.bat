@echo off
REM Build Cryfa on Windows

echo Building Cryfa for Windows...
echo.

cd /d "%~dp0cryfa-master"

REM Check if CMake is installed
where cmake >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: CMake not found!
    echo Install CMake: https://cmake.org/download/
    echo Or run: choco install cmake
    pause
    exit /b 1
)

REM Configure CMake
echo Configuring CMake...
cmake -B build -DCMAKE_BUILD_TYPE=Release

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: CMake configuration failed!
    echo You may need Visual Studio Build Tools
    echo Install: choco install visualstudio2022buildtools
    pause
    exit /b 1
)

REM Build
echo Building Cryfa...
cmake --build build --config Release --parallel 4

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

REM Copy executable
echo Copying executable...
if exist "build\Release\cryfa.exe" (
    copy "build\Release\cryfa.exe" "..\cryfa.exe"
    copy "build\Release\cryfa.exe" "..\backend\cryfa.exe"
    echo.
    echo ========================================
    echo SUCCESS! Cryfa built successfully!
    echo ========================================
    echo.
    echo Cryfa.exe copied to:
    echo   - Project root
    echo   - Backend folder
    echo.
    echo Test it: cryfa --version
    echo.
) else (
    echo ERROR: cryfa.exe not found after build
    pause
    exit /b 1
)

pause
