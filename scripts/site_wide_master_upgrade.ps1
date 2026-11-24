# scripts/site_wide_master_upgrade.ps1
# Automates Master Book V2 upgrades across all non-tool pages:
# 1. Unified @graph JSON-LD schema
# 2. Cannibalization elimination in category/comparison meta tags
# 3. Contextual payment pillar guide backlinking
# 4. AEO quick answer container fix

$rootDir = (Get-Location).Path

$orgEntity = [ordered]@{
    "@type" = "Organization"
    "@id" = "https://aidigitools.tech/#organization"
    "name" = "AIDigiTools"
    "url" = "https://aidigitools.tech/"
    "logo" = [ordered]@{
        "@type" = "ImageObject"
        "@id" = "https://aidigitools.tech/#logo"
        "url" = "https://aidigitools.tech/assets/images/logo.png"
        "caption" = "AIDigiTools"
    }
    "sameAs" = @(
        "https://github.com/abeerafarooq66",
        "https://wa.me/923326861112"
    )
    "contactPoint" = [ordered]@{
        "@type" = "ContactPoint"
        "telephone" = "+92-332-6861112"
        "contactType" = "customer service"
        "areaServed" = "PK"
        "availableLanguage" = @("English", "Urdu")
    }
}

$siteEntity = [ordered]@{
    "@type" = "WebSite"
    "@id" = "https://aidigitools.tech/#website"
    "url" = "https://aidigitools.tech/"
    "name" = "AIDigiTools"
    "publisher" = [ordered]@{
        "@id" = "https://aidigitools.tech/#organization"
    }
}

$authorEntity = [ordered]@{
    "@type" = "Person"
    "@id" = "https://aidigitools.tech/about.html#author"
    "name" = "Abeera Farooq"
    "url" = "https://aidigitools.tech/about.html"
    "sameAs" = @(
        "https://github.com/abeerafarooq66"
    )
}

# 1. Target files for schema unification
function Set-EntityId($ent, $idVal) {
    if ($ent.PSObject.Properties['@id']) {
        $ent.'@id' = $idVal
    } else {
        $ent | Add-Member -MemberType NoteProperty -Name '@id' -Value $idVal -Force
    }
}
$targetFiles = @(
    "categories\coding.html", "categories\image.html", "categories\video.html", "categories\vpn.html",
    "compare\chatgpt-vs-claude.html", "compare\runway-vs-pika.html",
    "best\best-ai-coding-tools.html", "best\best-ai-video-generators.html",
    "contact.html", "policies.html", "shipping-policy.html", "affiliate-disclosure.html", "blog.html", "deals.html",
    "guides\chatgpt-vs-claude.html",
    "blog\best-ai-tools-for-freelancers-in-pakistan.html",
    "blog\best-ai-video-generators-youtube-shorts-pakistan.html",
    "blog\claude-3-5-sonnet-vs-chatgpt-plus-coding-benchmark.html",
    "blog\claude-artifacts-practical-guide-freelancers.html",
    "blog\cursor-ai-vs-github-copilot-comparison.html",
    "blog\deepseek-r1-vs-chatgpt-plus-vs-claude-pro-comparison.html",
    "blog\how-to-pay-for-midjourney-in-pakistan-without-credit-card.html",
    "blog\runway-gen3-vs-capcut-pro-video-comparison.html"
)

Write-Host "Upgrading $($targetFiles.Count) pages to Unified Schema @graph..." -ForegroundColor Cyan

foreach ($rel in $targetFiles) {
    $fullPath = Join-Path $rootDir $rel
    if (-not (Test-Path $fullPath)) { continue }
    
    $content = Get-Content -LiteralPath $fullPath -Raw -Encoding UTF8
    $relSlash = $rel.Replace('\', '/')
    $pageUrl = "https://aidigitools.tech/$relSlash"
    
    # Extract page title
    $pageTitle = "AIDigiTools"
    if ($content -match '<title>(.*?)</title>') {
        $pageTitle = $matches[1] -replace '\s*\|\s*AIDigiTools.*$', ''
    }
    
    # Extract all JSON-LD blocks
    $scriptMatches = [regex]::Matches($content, '(?s)<script\s+type="application/ld\+json">(.*?)</script>')
    if ($scriptMatches.Count -eq 0) { continue }
    
    $rawEntities = @()
    foreach ($sm in $scriptMatches) {
        $rawJson = $sm.Groups[1].Value.Trim()
        try {
            $parsed = ConvertFrom-Json $rawJson -ErrorAction Stop
            if ($parsed.PSObject.Properties['@graph']) {
                $rawEntities += $parsed.'@graph'
            } else {
                $rawEntities += $parsed
            }
        } catch {
            Write-Warning "Failed to parse JSON in $rel`: $($_.Exception.Message)"
        }
    }
    
    $graphList = [System.Collections.ArrayList]::new()
    $graphList.Add($orgEntity) | Out-Null
    $graphList.Add($siteEntity) | Out-Null
    
    $webPageEntity = [ordered]@{
        "@type" = "WebPage"
        "@id" = "$pageUrl#webpage"
        "url" = $pageUrl
        "name" = $pageTitle
        "isPartOf" = [ordered]@{ "@id" = "https://aidigitools.tech/#website" }
        "breadcrumb" = [ordered]@{ "@id" = "$pageUrl#breadcrumb" }
    }
    
    # Process entities
    foreach ($ent in $rawEntities) {
        $type = $ent.'@type'
        if (-not $type) { continue }
        
        # Remove individual @context
        if ($ent.PSObject.Properties['@context']) {
            $ent.PSObject.Properties.Remove('@context')
        }
        
        if ($type -eq 'BreadcrumbList') {
            Set-EntityId $ent "$pageUrl#breadcrumb"
            $graphList.Add($ent) | Out-Null
        } elseif ($type -in @('TechArticle', 'Article', 'BlogPosting')) {
            Set-EntityId $ent "$pageUrl#article"
            $ent.author = $authorEntity
            $ent.publisher = [ordered]@{ "@id" = "https://aidigitools.tech/#organization" }
            $ent.mainEntityOfPage = [ordered]@{ "@id" = "$pageUrl#webpage" }
            $webPageEntity["mainEntity"] = [ordered]@{ "@id" = "$pageUrl#article" }
            $graphList.Add($ent) | Out-Null
        } elseif ($type -eq 'CollectionPage') {
            Set-EntityId $ent "$pageUrl#collection"
            $webPageEntity["mainEntity"] = [ordered]@{ "@id" = "$pageUrl#collection" }
            $graphList.Add($ent) | Out-Null
        } elseif ($type -eq 'ContactPage') {
            Set-EntityId $ent "$pageUrl#contact"
            $webPageEntity["mainEntity"] = [ordered]@{ "@id" = "$pageUrl#contact" }
            $graphList.Add($ent) | Out-Null
        } else {
            $graphList.Add($ent) | Out-Null
        }
    }
    
    # Insert WebPage entity before breadcrumbs or primary entity
    $graphList.Insert(2, $webPageEntity)
    
    $finalObj = [ordered]@{
        "@context" = "https://schema.org"
        "@graph" = $graphList
    }
    
    $jsonOutput = ConvertTo-Json -InputObject $finalObj -Depth 10
    
    # Replace all original <script type="application/ld+json"> blocks with the single unified block
    $firstScriptIndex = $content.IndexOf($scriptMatches[0].Value)
    $lastScript = $scriptMatches[$scriptMatches.Count - 1].Value
    $lastScriptEnd = $content.IndexOf($lastScript) + $lastScript.Length
    
    $newScriptTag = "`n  <script type=`"application/ld+json`">`n" + $jsonOutput + "`n  </script>`n"
    
    $before = $content.Substring(0, $firstScriptIndex)
    $after = $content.Substring($lastScriptEnd)
    
    $updatedContent = $before + $newScriptTag + $after
    
    Set-Content -LiteralPath $fullPath -Value $updatedContent -Encoding UTF8 -NoNewline
    Write-Host "✓ Unified @graph: $rel" -ForegroundColor Green
}

# 2. Fix Category & Comparison Meta Descriptions (Cannibalization)
$metaFixes = @{
    "categories\coding.html" = @{
        Desc = "Compare top AI coding assistants in Pakistan: Claude Sonnet 3.5, Cursor Pro & GitHub Copilot with verified PKR pricing, 15-min delivery & 30-day warranty."
        OgDesc = "Compare best AI coding assistants in Pakistan with verified PKR pricing and instant 15-minute WhatsApp activation."
    }
    "categories\image.html" = @{
        Desc = "Discover top AI image tools in Pakistan: Midjourney V6, Canva Pro & DALL-E with verified PKR rates, 15-minute WhatsApp setup & 30-day warranty."
        OgDesc = "Discover top AI image generators in Pakistan with verified PKR pricing and 15-minute WhatsApp concierge delivery."
    }
    "categories\video.html" = @{
        Desc = "Discover top AI video generators in Pakistan. Compare Runway Gen-3, Pika & CapCut Pro with verified PKR rates, 15-minute setup & 30-day warranty."
        OgDesc = "Compare top AI video generators in Pakistan with verified PKR pricing and instant 15-minute WhatsApp setup."
    }
    "categories\vpn.html" = @{
        Desc = "Discover top VPNs in Pakistan for secure browsing and unrestricted AI access. Fast setup, private credentials, and instant 15-minute WhatsApp delivery."
        OgDesc = "Top VPNs in Pakistan for secure browsing and AI tools with verified PKR pricing and 15-minute setup."
    }
    "compare\chatgpt-vs-claude.html" = @{
        Desc = "Detailed benchmark: ChatGPT Plus (Rs. 2,300 PKR / $8 USD) vs Claude Pro (Rs. 2,500 PKR / $9 USD). Coding speed, context window & 30-day warranty."
        OgDesc = "In-depth benchmark between ChatGPT Plus and Claude Pro in Pakistan with verified PKR pricing and 30-day warranty."
    }
    "compare\runway-vs-pika.html" = @{
        Desc = "Runway Gen-3 vs Pika AI comparison in Pakistan. Video rendering speed, cinematic camera control, PKR pricing, and 30-day warranty."
        OgDesc = "Runway Gen-3 vs Pika AI video generation shootout in Pakistan with verified PKR pricing."
    }
}

foreach ($rel in $metaFixes.Keys) {
    $fullPath = Join-Path $rootDir $rel
    if (Test-Path $fullPath) {
        $c = Get-Content -LiteralPath $fullPath -Raw -Encoding UTF8
        $desc = $metaFixes[$rel].Desc
        $ogDesc = $metaFixes[$rel].OgDesc
        
        $c = [regex]::Replace($c, '<meta\s+name=["'']description["'']\s+content=["''].*?["'']', "<meta name=`"description`" content=`"$desc`">")
        $c = [regex]::Replace($c, '<meta\s+property=["'']og:description["'']\s+content=["''].*?["'']', "<meta property=`"og:description`" content=`"$ogDesc`">")
        $c = [regex]::Replace($c, '<meta\s+name=["'']twitter:description["'']\s+content=["''].*?["'']', "<meta name=`"twitter:description`" content=`"$desc`">")
        
        Set-Content -LiteralPath $fullPath -Value $c -Encoding UTF8 -NoNewline
        Write-Host "✓ Cannibalization cleaned: $rel" -ForegroundColor Green
    }
}

# 3. Inject Contextual Payment Pillar Guide Link into Categories, Comparisons, and Blog Posts
$calloutHtml = @'

    <div class="payment-guide-callout" style="background:#F0FDF4;border-left:4px solid #10B981;padding:16px 20px;border-radius:0 8px 8px 0;margin:30px 0;">
      <p style="margin:0;font-size:1.02rem;color:#065F46;">
        💡 <strong>Need local payment support?</strong> Learn how to pay for AI subscriptions in Pakistan via EasyPaisa, JazzCash, and SadaPay in our <a href="/guides/how-to-pay-for-ai-tools-in-pakistan.html" style="color:#047857;font-weight:700;text-decoration:underline;">Complete Pakistan AI Payment Guide →</a>
      </p>
    </div>
'@

$linkTargets = @(
    "categories\coding.html", "categories\image.html", "categories\video.html", "categories\vpn.html",
    "compare\chatgpt-vs-claude.html", "compare\runway-vs-pika.html",
    "best\best-ai-coding-tools.html", "best\best-ai-video-generators.html",
    "blog\best-ai-tools-for-freelancers-in-pakistan.html",
    "blog\best-ai-video-generators-youtube-shorts-pakistan.html",
    "blog\claude-3-5-sonnet-vs-chatgpt-plus-coding-benchmark.html",
    "blog\claude-artifacts-practical-guide-freelancers.html",
    "blog\cursor-ai-vs-github-copilot-comparison.html",
    "blog\deepseek-r1-vs-chatgpt-plus-vs-claude-pro-comparison.html",
    "blog\how-to-pay-for-midjourney-in-pakistan-without-credit-card.html",
    "blog\runway-gen3-vs-capcut-pro-video-comparison.html"
)

foreach ($rel in $linkTargets) {
    $fullPath = Join-Path $rootDir $rel
    if (Test-Path $fullPath) {
        $c = Get-Content -LiteralPath $fullPath -Raw -Encoding UTF8
        if ($c -notmatch 'how-to-pay-for-ai-tools-in-pakistan') {
            if ($c -match '<footer') {
                $c = $c.Replace('<footer', $calloutHtml + "`n<footer")
            } elseif ($c -match '</main>') {
                $c = $c.Replace('</main>', $calloutHtml + "`n</main>")
            }
            Set-Content -LiteralPath $fullPath -Value $c -Encoding UTF8 -NoNewline
            Write-Host "✓ Injected payment guide pillar link: $rel" -ForegroundColor Green
        }
    }
}

# 4. Fix Quick Answer in guides/how-to-pay-for-ai-tools-in-pakistan.html
$guidePath = Join-Path $rootDir "guides\how-to-pay-for-ai-tools-in-pakistan.html"
if (Test-Path $guidePath) {
    $c = Get-Content -LiteralPath $guidePath -Raw -Encoding UTF8
    $c = $c.Replace('<div class="quick-answer" style="background:#F0FDF4; border-left:4px solid #10B981; padding:18px; border-radius:0 8px 8px 0; margin-bottom:30px; font-size:1.05rem;">', '<p class="quick-answer" style="background:#F0FDF4; border-left:4px solid #10B981; padding:18px; border-radius:0 8px 8px 0; margin-bottom:30px; font-size:1.05rem;">')
    # replace first </div> after quick-answer
    $qaPos = $c.IndexOf('class="quick-answer"')
    if ($qaPos -gt 0) {
        $divClosePos = $c.IndexOf('</div>', $qaPos)
        if ($divClosePos -gt 0 -and ($divClosePos - $qaPos) -lt 600) {
            $c = $c.Substring(0, $divClosePos) + '</p>' + $c.Substring($divClosePos + 6)
        }
    }
    Set-Content -LiteralPath $guidePath -Value $c -Encoding UTF8 -NoNewline
    Write-Host "✓ Fixed quick-answer container in payment guide" -ForegroundColor Green
}

# 5. Enrich llms.txt and llms-full.txt with payment pillar guide
$llmsPath = Join-Path $rootDir "llms.txt"
if (Test-Path $llmsPath) {
    $c = Get-Content -LiteralPath $llmsPath -Raw -Encoding UTF8
    if ($c -notmatch 'how-to-pay-for-ai-tools-in-pakistan') {
        $entry = "- [How to Pay for AI Tools in Pakistan (2026 Guide)](https://aidigitools.tech/guides/how-to-pay-for-ai-tools-in-pakistan.html): Comprehensive guide to buying ChatGPT Plus, Claude Pro, Midjourney, and Canva in Pakistan with EasyPaisa, JazzCash, SadaPay, and Raast.`n"
        $c = $c.Replace('## Guides & Comparisons', "## Guides & Comparisons`n`n$entry")
        Set-Content -LiteralPath $llmsPath -Value $c -Encoding UTF8 -NoNewline
        Write-Host "✓ Enriched llms.txt with payment guide" -ForegroundColor Green
    }
}

Write-Host "`nAll site-wide Master Book V2 upgrades complete!" -ForegroundColor Cyan
