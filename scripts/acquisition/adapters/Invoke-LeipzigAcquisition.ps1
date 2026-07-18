param(
    [ValidateSet('inventory','acquire','verify','status','resume','init-catalog','finalize-phases','complete-phases')]
    [string]$Mode = 'status'
)

$ExpectedDisplayRoot = '\\UNAS-Pro\AI.Workspace'
$Drive = Get-PSDrive -Name Z -ErrorAction Stop
if (-not [string]::Equals([string]$Drive.DisplayRoot, $ExpectedDisplayRoot, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Z: must map to $ExpectedDisplayRoot; observed '$($Drive.DisplayRoot)'"
}
if (-not (Test-Path -LiteralPath 'Z:/01-Projects/Logos' -PathType Container)) {
    throw 'Approved Logos NAS root is unavailable: Z:/01-Projects/Logos'
}

$Root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $Root

python scripts/acquisition/run_acquisition.py `
  --task-id T479 `
  --mode $Mode `
  --rights-ledger "Z:/01-Projects/Logos/manuscript-witnesses/catalog/T479/rights_ledger.yaml" `
  --nas-root "Z:/01-Projects/Logos" `
  --config scripts/acquisition/config/leipzig_0000061851.yaml
