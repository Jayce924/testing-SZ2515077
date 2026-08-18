$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Push-Location (Join-Path $repoRoot "01_service_api_test")
python -m pytest -q --junitxml=reports/junit.xml
Pop-Location

Push-Location (Join-Path $repoRoot "02_continuous_integration")
python -m pytest -q --junitxml=reports/junit.xml
python -m build
Pop-Location

Push-Location (Join-Path $repoRoot "03_performance_profiling")
python -m pytest -q --junitxml=reports/junit.xml
python profile_run.py --records 50000 --out results
Pop-Location

Write-Host "All experiments completed."
