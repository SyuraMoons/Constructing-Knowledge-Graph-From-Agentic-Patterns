$root = "D:\Projects\Constructing-Knowledge-Graph-From-Agentic-Patterns-main"
#bisa diubah sesuai dengan lokasi file

$ttlRMLRoot = "$root\mappings\ttl (rml)"
$outputRDFRoot = "$root\output"
$rmlMapperJar = "$root\rmlmapper-8.0.0-r378-all.jar"

if (-not (Test-Path $outputRDFRoot)) { New-Item -ItemType Directory -Path $outputRDFRoot }

Get-ChildItem -Path $ttlRMLRoot -Directory | ForEach-Object {
    $subfolderName = $_.Name
    $subfolderPath = $_.FullName

    $outputSubfolder = Join-Path $outputRDFRoot $subfolderName
    if (-not (Test-Path $outputSubfolder)) { New-Item -ItemType Directory -Path $outputSubfolder }

    Get-ChildItem -Path $subfolderPath -Filter *.rml.ttl | ForEach-Object {
        $rmlTtlFile = $_.FullName
        $fileName = $_.BaseName -replace "\.rml$", ""  
        $rdfFile = Join-Path $outputSubfolder "$fileName.ttl"

        Write-Host "Mapping $($_.Name) → $subfolderName/$fileName.ttl ..."

        java -jar $rmlMapperJar -m $rmlTtlFile -o $rdfFile -s turtle
    }
}

Write-Host "All RML TTL files converted to RDF TTL in respective subfolders successfully."
