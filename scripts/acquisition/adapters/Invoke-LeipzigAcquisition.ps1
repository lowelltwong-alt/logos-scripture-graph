param(
    [ValidateSet('inventory','acquire','verify','status','resume','init-catalog')]
    [string]$Mode = 'status'
)

$Root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $Root

python scripts/acquisition/run_acquisition.py `
  --task-id T479 `
  --mode $Mode `
  --rights-ledger "Z:/01-Projects/Logos/manuscript-witnesses/catalog/T479/rights_ledger.yaml" `
  --nas-root "Z:/01-Projects/Logos" `
  --config scripts/acquisition/config/leipzig_0000061851.yaml
