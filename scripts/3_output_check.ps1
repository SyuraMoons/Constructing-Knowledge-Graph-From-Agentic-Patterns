$ttlRoot = "D:\Projects\Constructing-Knowledge-Graph-From-Agentic-Patterns-main"
#bisa diubah sesuai dengan lokasi file

Get-ChildItem -Path $ttlRoot -Recurse -Filter *.ttl | ForEach-Object {
    $file = $_.FullName
    $content = Get-Content $file -Raw

    $newContent = $content -replace 'agento:(domain|range)\s+"([^"]*(agento:|xsd:)[^"]*)"', 'agento:$1 $2'

    Set-Content -Path $file -Value $newContent

    Write-Host "$($_.FullName) updated"
}
