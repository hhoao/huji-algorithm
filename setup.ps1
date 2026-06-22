$ErrorActionPreference = "Stop"

python -m venv .venv
& .\.venv\Scripts\Activate.ps1

Write-Host "Setting up development environment..."

Write-Host "Installing dependencies..."
pip install -r requirements.txt
pip install pre-commit ruff pyright

Write-Host "Installing pre-commit hooks..."
pre-commit uninstall
if ($LASTEXITCODE -ne 0) { $LASTEXITCODE = 0 }
pre-commit install
pre-commit install --hook-type commit-msg

Write-Host "Running initial check..."
pre-commit run --all-files

Write-Host "Setup complete! Activate with: .venv\Scripts\activate"
