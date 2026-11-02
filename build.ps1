# Builds the deployable artifact on Windows: dist\webapp.tar.gz
# With -Upload it also sends the artifact to S3.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File .\build.ps1
#   powershell -ExecutionPolicy Bypass -File .\build.ps1 -Upload

param(
  [switch]$Upload,
  [string]$Bucket = "teodora-cato-artifacts",
  [string]$AwsProfile = "user2",
  [string]$Region = "eu-west-1"
)

$ErrorActionPreference = "Stop"

$root = $PSScriptRoot
$dist = Join-Path $root "dist"
$staging = Join-Path $dist "staging"
$artifact = Join-Path $dist "webapp.tar.gz"

# 1. Start from an empty dist folder
if (Test-Path $dist) { Remove-Item $dist -Recurse -Force }
New-Item -ItemType Directory -Path $staging | Out-Null

# 2. Put everything the server needs into one folder
Copy-Item (Join-Path $root "common") $staging -Recurse
Copy-Item (Join-Path $root "webapp") $staging -Recurse
Copy-Item (Join-Path $root "webapp\requirements.txt") $staging
Get-ChildItem $staging -Recurse -Directory -Filter "__pycache__" |
  Remove-Item -Recurse -Force

# 3. Pack it into one file (tar is built into Windows 10/11)
tar -czf "$artifact" -C "$staging" .
if ($LASTEXITCODE -ne 0) { throw "tar failed" }
Remove-Item $staging -Recurse -Force
Write-Host "Built $artifact"

# 4. Optionally upload to S3
if ($Upload) {
  aws s3 cp "$artifact" "s3://$Bucket/webapp/webapp.tar.gz" --profile $AwsProfile --region $Region
  if ($LASTEXITCODE -ne 0) { throw "Upload to S3 failed" }
  Write-Host "Uploaded to s3://$Bucket/webapp/webapp.tar.gz"
}
