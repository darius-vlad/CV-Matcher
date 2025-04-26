$scriptPath = $PSScriptRoot
$configFolder = Join-Path -Path $scriptPath -ChildPath "model_config"

if (-not (Test-Path -Path $configFolder)) {
    New-Item -Path $configFolder -ItemType Directory | Out-Null
}

ollama rm deepseek-r1:1.5b_vram
# ----------------------------------------------------------
# Modelul deepseek-r1:1.5b_vram
# ----------------------------------------------------------
$modelfile1.5b = @"
FROM deepseek-r1:1.5b
PARAMETER num_gpu 64
PARAMETER num_ctx 6500
"@

$1.5bPath = Join-Path -Path $configFolder -ChildPath "deepseek_1.5b_vram.modelfile"
Set-Content -Path $1.5bPath -Value $modelfile1.5b

Write-Host "Creating 1.5b model from: $(Resolve-Path $1.5bPath)" -ForegroundColor Cyan
ollama create deepseek-r1:1.5b_vram -f $1.5bPath

