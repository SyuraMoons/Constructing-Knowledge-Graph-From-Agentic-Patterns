$root = "D:\Projects\Constructing-Knowledge-Graph-From-Agentic-Patterns-main"
$outputFolder = Join-Path $root "output"
#bisa diubah sesuai dengan lokasi file

$shaclFile = Join-Path $root "shapes\shapes.ttl"
$reportFile = Join-Path $root "validation_report.txt"


"Knowledge Graph Validation Report" | Out-File $reportFile
"Generated on: $(Get-Date)" | Out-File $reportFile -Append
"Root Folder: $outputFolder" | Out-File $reportFile -Append
"SHACL Shape: $shaclFile" | Out-File $reportFile -Append
"`n============================================`n" | Out-File $reportFile -Append

$totalTriples = 0

Get-ChildItem -Path $outputFolder -Recurse -Filter *.ttl | ForEach-Object {
    $ttlFile = $_.FullName
    $relativePath = $ttlFile.Replace($outputFolder + '\', '')

    $tripleCount = py -c "
import rdflib
g = rdflib.Graph()
g.parse(r'$ttlFile', format='turtle')
print(len(g))
" | Out-String
    $tripleCount = $tripleCount.Trim()
    $tripleCountInt = [int]$tripleCount
    $totalTriples += $tripleCountInt

    $validation = py -c "
from pyshacl import validate
from rdflib import Graph

data = Graph()
data.parse(r'$ttlFile', format='turtle')

shapes = Graph()
shapes.parse(r'$shaclFile', format='turtle')

conforms, report_graph, report_text = validate(
    data_graph=data,
    shacl_graph=shapes,
    inference='rdfs',
    debug=False
)

print(conforms)
print('-----REPORT-----')
print(report_text)
" | Out-String

    $lines = $validation -split "`n"
    $conforms = $lines[0].Trim()
    $reportText = ($lines | Select-Object -Skip 2) -join "`n"

    Write-Host "$relativePath has $tripleCountInt triples."
    Write-Host "Conforms: $conforms"

    "FILE: $relativePath" | Out-File $reportFile -Append
    "Triples: $tripleCountInt" | Out-File $reportFile -Append
    "Conforms: $conforms" | Out-File $reportFile -Append

    if ($conforms -ne "True") {
        "Validation Errors:" | Out-File $reportFile -Append
        $reportText | Out-File $reportFile -Append
    }

    "`n--------------------------------------------`n" | Out-File $reportFile -Append
}

"`nTOTAL TRIPLES ACROSS ALL FILES: $totalTriples" | Out-File $reportFile -Append
"`nValidation Completed." | Out-File $reportFile -Append
