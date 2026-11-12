$ErrorActionPreference = 'Stop'
$workspace = Split-Path -Parent $PSScriptRoot
$output = Join-Path $workspace 'output/pdf'
New-Item -ItemType Directory -Force -Path $output | Out-Null
$compiler = (Get-Command pdflatex -ErrorAction Stop).Source
$jobs = @(
    @{ Project = 'governance-basics'; Name = 'databricks-governance-basics'; Passes = 3 },
    @{ Project = 'governance-lab'; Name = 'databricks-governance-lab'; Passes = 2 },
    @{ Project = 'governance-quiz'; Name = 'databricks-governance-quiz'; Passes = 2 },
    @{ Project = 'governance-solution'; Name = 'databricks-governance-solution'; Passes = 2 }
)
foreach ($job in $jobs) {
    $projectPath = Join-Path $PSScriptRoot $job.Project
    $buildPath = Join-Path $workspace ('tmp/pdfs/' + $job.Name + '-build')
    New-Item -ItemType Directory -Force -Path $buildPath | Out-Null
    Push-Location -LiteralPath $projectPath
    try {
        foreach ($pass in 1..$job.Passes) {
            $logPath = Join-Path $buildPath ("compile-pass{0}.txt" -f $pass)
            # pdflatex/MiKTeX writes warnings to stderr; rely on $LASTEXITCODE instead of treating stderr as fatal.
            $prevPref = $ErrorActionPreference
            $ErrorActionPreference = 'Continue'
            & $compiler '-interaction=nonstopmode' '-halt-on-error' '-file-line-error' "-output-directory=$buildPath" "-jobname=$($job.Name)" 'main.tex' *> $logPath
            $ErrorActionPreference = $prevPref
            if ($LASTEXITCODE -ne 0) {
                Get-Content -LiteralPath $logPath -Tail 35
                throw "Compilation failed for $($job.Name), pass $pass."
            }
        }
        $builtPdf = Join-Path $buildPath ($job.Name + '.pdf')
        Copy-Item -LiteralPath $builtPdf -Destination (Join-Path $output ($job.Name + '.pdf'))
        Write-Output ("Built {0}" -f $job.Name)
    }
    finally {
        Pop-Location
    }
}

# Slides: PowerPoint deck cloned from "Template Format trình bày.pptx" (workspace root).
# Rebuilding needs a Python with python-pptx (set $env:PPTX_PYTHON to choose one); the PDF export needs PowerPoint.
$deck = Join-Path $workspace 'output/databricks-governance-slides.pptx'
$template = Get-ChildItem -LiteralPath $workspace -Filter 'Template Format*.pptx' -ErrorAction SilentlyContinue | Select-Object -First 1
$python = $null
foreach ($candidate in @($env:PPTX_PYTHON, 'python', 'py') | Where-Object { $_ }) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        & $candidate -c 'import pptx' 2>$null
        if ($LASTEXITCODE -eq 0) { $python = $candidate; break }
    }
}
if (-not $template) {
    Write-Warning 'Template "Template Format*.pptx" not found in the workspace root; keeping the existing slide deck.'
}
elseif ($python) {
    & $python -I (Join-Path $PSScriptRoot 'governance-slides/build_deck.py') $deck
    if ($LASTEXITCODE -ne 0) { throw 'Slide deck build failed.' }
}
else {
    Write-Warning 'No Python with python-pptx found; keeping the existing output/databricks-governance-slides.pptx.'
}
if (Test-Path -LiteralPath $deck) {
    try {
        $app = New-Object -ComObject PowerPoint.Application
        try {
            $pres = $app.Presentations.Open($deck, $true, $false, $false)
            $pres.SaveAs((Join-Path $output 'databricks-governance-slides.pdf'), 32)
            $pres.Close()
            Write-Output 'Built databricks-governance-slides (PDF via PowerPoint)'
        }
        finally { $app.Quit() | Out-Null }
    }
    catch {
        Write-Warning ('PowerPoint is not available, slide PDF not refreshed: ' + $_.Exception.Message)
    }
}

$bundlePath = Join-Path $workspace 'output/databricks-governance-latex.zip'
$bundleFiles = @(
    'governance-basics', 'governance-lab', 'governance-slides', 'governance-quiz', 'governance-solution', 'assets',
    'databricks-governance-basics.md', 'databricks-governance-hands-on.md',
    'databricks-governance-quiz.md', 'databricks-governance-solution.md',
    'README.md', 'build-pdfs.ps1'
) | ForEach-Object { Join-Path $PSScriptRoot $_ }
$bundleFiles += Join-Path $workspace 'shared'
if (Test-Path -LiteralPath $deck) { $bundleFiles += $deck }
Compress-Archive -LiteralPath $bundleFiles -DestinationPath $bundlePath -Force
Write-Output 'Packaged output/databricks-governance-latex.zip'
