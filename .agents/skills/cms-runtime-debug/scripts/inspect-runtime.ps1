<#
.SYNOPSIS
    Read-only CMS runtime memory and port snapshot.
.DESCRIPTION
    Reports Windows physical/commit headroom, process groups, and TCP reachability.
    Does not expose command lines, start services, load models, or stop processes.
.PARAMETER Top
    Number of process groups to report (1-30).
.EXAMPLE
    .\inspect-runtime.ps1 -Top 10
#>
[CmdletBinding()]
param([ValidateRange(1, 30)][int]$Top = 12)

$ErrorActionPreference = 'Stop'
$osInfo = Get-CimInstance Win32_OperatingSystem
Write-Output ('Snapshot: {0}' -f (Get-Date -Format o))
[pscustomobject]@{
    TotalPhysicalMiB = [math]::Round($osInfo.TotalVisibleMemorySize / 1024)
    FreePhysicalMiB = [math]::Round($osInfo.FreePhysicalMemory / 1024)
    FreeCommitMiB = [math]::Round($osInfo.FreeVirtualMemory / 1024)
} | Format-List

Get-Process | Group-Object ProcessName | ForEach-Object {
    [pscustomobject]@{
        Name = $_.Name
        Count = $_.Count
        WorkingSetMiB = [math]::Round(($_.Group | Measure-Object WorkingSet64 -Sum).Sum / 1MB)
        PrivateCommitMiB = [math]::Round(($_.Group | Measure-Object PrivateMemorySize64 -Sum).Sum / 1MB)
    }
} | Sort-Object WorkingSetMiB -Descending | Select-Object -First $Top | Format-Table -AutoSize

foreach ($servicePort in @(7860, 8080)) {
    $client = New-Object System.Net.Sockets.TcpClient
    $reachable = $false
    try {
        $pending = $client.ConnectAsync('127.0.0.1', $servicePort)
        if ($pending.Wait(1000)) { $reachable = $client.Connected }
    } catch {
        $reachable = $false
    } finally {
        $client.Dispose()
    }
    [pscustomobject]@{ Host = '127.0.0.1'; Port = $servicePort; TcpReachable = $reachable }
}
Write-Output 'Working sets can share physical pages; do not sum them as unique system RAM.'
