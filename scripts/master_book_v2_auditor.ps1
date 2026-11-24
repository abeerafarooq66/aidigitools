# AIDigiTools Master Audit Engine V2 (Native PowerShell)
# Compliant with: Universal Web Search & SEO Master Book V2 (Nov 2026 Edition)

$rootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$htmlFiles = Get-ChildItem -Path $rootDir -Recurse -Filter "*.html" | Where-Object { $_.FullName -notmatch '\\admin\\' -and $_.FullName -notmatch '\\\.git\\' }

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "   AIDIGITOOLS FORENSIC DEEP AUDIT ENGINE (MASTER BOOK V2 BENCHMARK)           " -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "Total HTML Pages Scanned: $($htmlFiles.Count)"
Write-Host "Base Directory: $rootDir`n"

$restricted = @('turnitin-student', 'linkedin-premium', 'netflix-premium', 'spotify-premium', 'coursera-plus', 'claude-artifacts', 'deepseek-pro')
$keywordTracker = @{}
$targetKws = @('sadapay', 'nayapay', 'jazzcash', 'easypaisa')
foreach ($k in $targetKws) { $keywordTracker[$k] = [System.Collections.ArrayList]::new() }

$stats = @{
    CrawlabilityPass = 0; CrawlabilityFail = 0
    CanonicalPass = 0; CanonicalFail = 0
    H1Pass = 0; H1Fail = 0
    SchemaPass = 0; SchemaFail = 0
    AeoGeoPass = 0; AeoGeoFail = 0
    EeatPass = 0; EeatFail = 0
}

# 1. Robots.txt
$robotsPath = Join-Path $rootDir "robots.txt"
if (Test-Path $robotsPath) {
    $robotsTxt = Get-Content -LiteralPath $robotsPath -Raw -Encoding UTF8
    $requiredBots = @('OAI-SearchBot', 'Claude-SearchBot', 'PerplexityBot', 'Applebot', 'Googlebot', 'Bingbot')
    foreach ($b in $requiredBots) {
        if ($robotsTxt -match $b) { $stats.CrawlabilityPass++ } else { $stats.CrawlabilityFail++; Write-Warning "Missing in robots.txt: $b" }
    }
}

# 2. Iterate HTML Files
foreach ($file in $htmlFiles) {
    $rel = $file.FullName.Substring($rootDir.Length + 1).Replace('\', '/')
    $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
    
    # Canonical
    if ($content -match '<link\s+rel=["'']canonical["'']\s+href=["''](https://aidigitools\.tech/[^"'']*)["'']') {
        $stats.CanonicalPass++
    } else {
        $stats.CanonicalFail++
        Write-Warning "${rel}: Invalid or missing canonical link"
    }

    # Single H1
    $h1Count = ([regex]::Matches($content, '<h1[^>]*>([\s\S]*?)</h1>', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)).Count
    if ($h1Count -eq 1) {
        $stats.H1Pass++
    } else {
        $stats.H1Fail++
        Write-Warning "${rel}: Expected 1 H1, found $h1Count"
    }

    # Schema
    if ($content -match '<script\s+type=["'']application/ld\+json["'']>') {
        $slug = $file.BaseName
        if ($rel.StartsWith('tools/')) {
            if ($restricted -contains $slug) {
                if ($content -match '"availability":\s*"https://schema\.org/OutOfStock"') { $stats.SchemaPass++ } else { $stats.SchemaFail++; Write-Warning "${rel}: Restricted product must be OutOfStock" }
            } else {
                if ($content -match '"availability":\s*"https://schema\.org/InStock"') { $stats.SchemaPass++ } else { $stats.SchemaFail++; Write-Warning "${rel}: Active tool must be InStock" }
            }
        } else {
            $stats.SchemaPass++
        }
    } else {
        $stats.SchemaFail++
        Write-Warning "${rel}: Missing JSON-LD schema"
    }

    # Cannibalization
    $titleMatch = [regex]::Match($content, '<title>([\s\S]*?)</title>', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    $titleText = if ($titleMatch.Success) { $titleMatch.Groups[1].Value.ToLower() } else { "" }
    $descMatch = [regex]::Match($content, '<meta\s+name=["'']description["'']\s+content=["'']([^"'']*)["'']', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    $descText = if ($descMatch.Success) { $descMatch.Groups[1].Value.ToLower() } else { "" }
    
    foreach ($k in $targetKws) {
        if ($titleText.Contains($k) -or $descText.Contains($k)) {
            $keywordTracker[$k].Add($rel) | Out-Null
        }
    }

    # AEO / GEO Quick Answer
    $qaMatch = [regex]::Match($content, 'class=["''][^"'']*quick-answer[^"'']*["''][^>]*>([\s\S]*?)</p>', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    if ($qaMatch.Success) {
        $cleanQa = $qaMatch.Groups[1].Value -replace '<[^>]+>', ''
        $words = $cleanQa.Split([char[]]@(' ', "`t", "`n", "`r"), [System.StringSplitOptions]::RemoveEmptyEntries).Count
        if ($words -ge 30 -and $words -le 120 -and $cleanQa -match '\d+' -and ($cleanQa -match 'pkr|rs\.|\$|usd')) {
            $stats.AeoGeoPass++
        } else {
            $stats.AeoGeoFail++
        }
    } elseif ($rel.StartsWith('tools/') -or $rel.StartsWith('guides/') -or $rel.StartsWith('blog/')) {
        $stats.AeoGeoFail++
    }

    # E-E-A-T
    if ($rel.StartsWith('blog/') -or $rel.StartsWith('guides/')) {
        if ($content -match 'Abeera\s+Farooq' -and $content -match '2026') {
            $stats.EeatPass++
        } else {
            $stats.EeatFail++
        }
    }
}

Write-Host "`n--------------------------------------------------------------------------------" -ForegroundColor Cyan
Write-Host "                    MASTER BOOK V2 COMPLIANCE RESULTS                           " -ForegroundColor Cyan
Write-Host "--------------------------------------------------------------------------------" -ForegroundColor Cyan

function Format-Score($title, $pass, $fail) {
    $tot = $pass + $fail
    $pct = if ($tot -gt 0) { [math]::Round(($pass / $tot) * 100, 1) } else { 0 }
    $icon = if ($pct -ge 95) { "🟢" } elseif ($pct -ge 75) { "🟡" } else { "🔴" }
    Write-Host ("{0} {1,-18} : {2,5}% Passed ({3}/{4})" -f $icon, $title, $pct, $pass, $tot)
}

Format-Score "CRAWLABILITY" $stats.CrawlabilityPass $stats.CrawlabilityFail
Format-Score "CANONICAL TAGS" $stats.CanonicalPass $stats.CanonicalFail
Format-Score "H1 HIERARCHY" $stats.H1Pass $stats.H1Fail
Format-Score "SCHEMA GRAPH" $stats.SchemaPass $stats.SchemaFail
Format-Score "AEO/GEO CAPSULES" $stats.AeoGeoPass $stats.AeoGeoFail
Format-Score "EEAT FOOTPRINT" $stats.EeatPass $stats.EeatFail

Write-Host "`n--- Local Payment Keyword Dispersion (Cannibalization Risk) ---" -ForegroundColor Yellow
foreach ($k in $targetKws) {
    $count = $keywordTracker[$k].Count
    $risk = if ($count -gt 2) { "🔴 High Cannibalization" } else { "🟢 Clean" }
    Write-Host ("Keyword '{0,-10}' : {1,2} Pages ({2})" -f $k, $count, $risk)
}
Write-Host "`n================================================================================" -ForegroundColor Cyan


