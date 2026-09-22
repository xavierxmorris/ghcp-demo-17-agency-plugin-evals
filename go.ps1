#requires -Version 7.0
[CmdletBinding()]
param(
    [switch]$Check,
    [switch]$Live,
    [switch]$Manual,
    [switch]$NoBrowser
)

$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    $projects = @(
        'projects\01-skill-routing',
        'projects\02-mcp-tool-selection',
        'projects\03-custom-agent-regression'
    )

    if ($Manual) {
        Write-Host @'
Workshop commands
-----------------
1. python -m pip install -r projects\02-mcp-tool-selection\requirements.txt
2. .\go.ps1 -Check
3. agency copilot --plugin mp:plugin-eval@curated
4. /agency-eval-guide
5. agency eval-new generate --plugin .\projects\01-skill-routing --out .\generated-evals\01-skill-routing
6. agency eval-new run --plugin .\projects\01-skill-routing --task incident-brief--checkout-handoff --keep-tempdir

Public CI validates deterministic contracts. Full model-scored evals use the
manual self-hosted Agency workflow.
'@
        exit 0
    }

    & python -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 2)"
    if ($LASTEXITCODE -ne 0) {
        throw 'Python 3.11+ is required.'
    }

    & python -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) {
        throw 'Unit tests failed.'
    }

    & python scripts\check_repo.py
    if ($LASTEXITCODE -ne 0) {
        throw 'Repository checks failed.'
    }

    $agency = Get-Command agency -ErrorAction SilentlyContinue
    if ($agency) {
        $generatedRoot = Join-Path $env:TEMP "agency-eval-demo-$([guid]::NewGuid().ToString('N'))"
        try {
            foreach ($project in $projects) {
                Write-Host "`n=== Agency validation: $project" -ForegroundColor Cyan
                & agency plugin check $project
                if ($LASTEXITCODE -ne 0) {
                    throw "agency plugin check failed for $project"
                }

                & agency eval-new doctor --plugin $project --no-tokens
                if ($LASTEXITCODE -ne 0) {
                    throw "agency eval-new doctor failed for $project"
                }

                $out = Join-Path $generatedRoot (Split-Path $project -Leaf)
                & agency eval-new generate --plugin $project --out $out
                if ($LASTEXITCODE -ne 0) {
                    throw "agency eval-new generate failed for $project"
                }
            }
        } finally {
            if (Test-Path $generatedRoot) {
                Remove-Item -LiteralPath $generatedRoot -Recurse -Force
            }
        }
    } else {
        Write-Warning 'Agency CLI not found; skipped plugin check and eval materialization.'
    }

    if ($Check) {
        Write-Host "`nAll deterministic checks passed." -ForegroundColor Green
        exit 0
    }

    $runId = (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0, 8)
    $bundle = Join-Path $PSScriptRoot "out\demo-$runId"
    & python scripts\render_catalog.py --out $bundle
    if ($LASTEXITCODE -ne 0) {
        throw 'Report generation failed.'
    }

    if (-not $NoBrowser) {
        Start-Process -FilePath (Join-Path $bundle 'report.html') | Out-Null
    }

    Write-Host "Evidence: $bundle" -ForegroundColor Green
    Write-Host 'No model-scored eval ran. Use agency eval-new run with a configured harness.'

    if ($Live) {
        Write-Host @'

Live beats
----------
1. Compare the three plugin types in report.html.
2. Open one instruction.md beside task.toml to show answer-key isolation.
3. Search for expected_tool = "NONE" to show negative coverage.
4. Open the two CI workflows to show deterministic versus model-scored evidence.
'@
    }
} finally {
    Pop-Location
}
