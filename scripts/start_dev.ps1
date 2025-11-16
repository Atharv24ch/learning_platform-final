# start_dev.ps1
# Kills any process listening on port 3000 (Node/Next), removes Next dev locks,
# then starts Django and Next dev servers in separate windows.

Write-Output "Stopping any process on port 3000..."
$lines = netstat -ano | findstr ":3000" 2>$null
if ($lines) {
    $pids = ($lines -split "\n" | ForEach-Object { ($_ -split '\s+')[-1] } ) | Where-Object { $_ -match '^[0-9]+$' } | Sort-Object -Unique
    foreach ($pid in $pids) {
        try {
            Write-Output "Killing PID $pid"
            taskkill /PID $pid /F | Out-Null
        } catch {
            Write-Output ([string]::Format('Failed to kill PID {0}: {1}', $pid, $_))
        }
    }
} else {
    Write-Output "No process found listening on port 3000."
}

# Remove Next lock files
$lock1 = Join-Path $PSScriptRoot "..\frontend\.next\dev\lock"
$lock2 = Join-Path $PSScriptRoot "..\frontend\.next\dev\server.lock"
Remove-Item -Path $lock1 -Force -ErrorAction SilentlyContinue
Remove-Item -Path $lock2 -Force -ErrorAction SilentlyContinue
Write-Output "Removed Next lock files if they existed."

# Start Django dev server in new window
$backendPath = Join-Path $PSScriptRoot "..\backend"
$manage = Join-Path $backendPath "manage.py"
if (Test-Path $manage) {
    Write-Output "Starting Django dev server..."
    Start-Process -FilePath "python" -ArgumentList "`"$manage`" runserver 127.0.0.1:8000" -WorkingDirectory $backendPath -WindowStyle Normal
} else {
    Write-Output "manage.py not found at $manage. Skipping Django start."
}

# Start Next dev in new window
$frontendPath = Join-Path $PSScriptRoot "..\frontend"
if (Test-Path $frontendPath) {
    Write-Output "Starting Next dev server..."
    Start-Process -FilePath "npm" -ArgumentList "run dev" -WorkingDirectory $frontendPath -WindowStyle Normal
} else {
    Write-Output "frontend folder not found at $frontendPath. Skipping Next start."
}

Write-Output "Start dev script finished. Check the spawned windows for logs."