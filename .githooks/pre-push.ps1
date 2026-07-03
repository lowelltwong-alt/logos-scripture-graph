$ErrorActionPreference = 'Stop'
$DadHub = $env:DAD_HUB_PATH
if (-not $DadHub) {
  Write-Error 'DAD_HUB_PATH is required before this DAD hook can enforce postflight.'
  exit 1
}
python "$DadHub/scripts/enforce_postflight.py" --hub "$DadHub" --repo (Get-Location).Path
