$root = "D:\Projects\Constructing-Knowledge-Graph-From-Agentic-Patterns-main"
#bisa diubah sesuai dengan lokasi file

$yamlFolders = @(
    "$root\mappings\yaml\autogen",
    "$root\mappings\yaml\crewai",
    "$root\mappings\yaml\langraph",
    "$root\mappings\yaml\mastraai"
)

$ttlRMLRoot = "$root\mappings\ttl (rml)"

foreach ($folder in $yamlFolders) {
    $subfolderName = Split-Path $folder -Leaf
    $ttlRMLFolder = Join-Path $ttlRMLRoot $subfolderName
    if (-not (Test-Path $ttlRMLFolder)) { New-Item -ItemType Directory -Path $ttlRMLFolder }
}

foreach ($folder in $yamlFolders) {
    $subfolderName = Split-Path $folder -Leaf
    $ttlRMLFolder = Join-Path $ttlRMLRoot $subfolderName

    Get-ChildItem -Path $folder -Filter *.yaml | ForEach-Object {
        $yamlFile = $_.FullName
        $fileName = $_.BaseName
        $rmlTtlFile = Join-Path $ttlRMLFolder "$fileName.rml.ttl"

        Write-Host "Converting $fileName.yaml → $fileName.rml.ttl ..."

        yarrrml-parser -i $yamlFile -o $rmlTtlFile
    }
}

Write-Host "All YAML files converted to RML TTL successfully."
