# run_data_hiding.ps1


# Display welcome message
Write-Host "`n===================================================" -ForegroundColor Yellow
Write-Host "Welcome To Image Steganography Tool! By Atanu Bera" -ForegroundColor Yellow
Write-Host "===================================================`n" -ForegroundColor Yellow
Write-Host "Wait a Moment ..." -ForegroundColor Cyan
Write-Host "Installing All The Required Environment" -ForegroundColor Cyan

# Create virtual environment folder
$venvPath = ".\venv"
python -m venv $venvPath

# Activate the virtual environment
$activateScript = Join-Path $venvPath "Scripts\Activate"
& $activateScript

# Install OpenCV
pip install opencv-python
Write-Host "" -ForegroundColor Cyan
Write-Host "Done!" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Cyan
Write-Host "Name your Image '1.jpg' " -ForegroundColor Yellow
Write-Host "" -ForegroundColor Cyan
# Run the Python script
python ImageSteganography.py

# Pause at the end to prevent the terminal from closing
pause
