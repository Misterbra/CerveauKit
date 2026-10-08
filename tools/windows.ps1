param([ValidateSet('Verify','Install','Open','InstallVideo','Videos')][string]$Action='Verify')
$ErrorActionPreference='Stop'
$kitRoot=Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $kitRoot
function Refresh-Tools {
 $paths=@($env:PATH,[Environment]::GetEnvironmentVariable('Path','User'),[Environment]::GetEnvironmentVariable('Path','Machine'))
 if ($env:USERPROFILE) { $paths+=(Join-Path $env:USERPROFILE '.local\bin') }
 if ($env:LOCALAPPDATA) { $paths+=(Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Links') }
 if ($env:APPDATA) { $paths+=(Join-Path $env:APPDATA 'npm') }
 $env:PATH=($paths|Where-Object { $_ }) -join ';'
}
function Has-Tool([string]$Name) { return [bool](Get-Command $Name -ErrorAction SilentlyContinue) }
function Version([string]$Name) {
 if (!(Has-Tool $Name)) { return 'absent' }
 try { $versionArg=if ($Name -eq 'ffmpeg') { '-version' } else { '--version' }; $v=& $Name $versionArg 2>&1; if ($LASTEXITCODE -eq 0) { return ($v|Select-Object -First 1) } } catch {}
 return 'present, verification manuelle necessaire'
}
function Offer([string]$Name,[string]$Id,[string]$Url) {
 if (Has-Tool $Name) { return }
 if (!(Has-Tool 'winget')) { throw "Installez $Name depuis $Url puis relancez." }
 if ((Read-Host "Installer $Id depuis WinGet ($Url) ? [o/N]") -ne 'o') { throw 'Installation annulee.' }
 & winget install --exact --id $Id --source winget
 if ($LASTEXITCODE -ne 0) { throw 'Installation WinGet non terminee. Consultez les erreurs.' }
 Refresh-Tools
}
function Python312 {
 $candidates=@()
 if (Has-Tool 'py') {
  try { $v=& py -3.12 -c "import sys; print(sys.executable)" 2>$null
   if ($LASTEXITCODE -eq 0) { $candidates+=$v } } catch {}
 }
 if (Has-Tool 'python') { $candidates+=(Get-Command python).Source }
 if ($env:LOCALAPPDATA) { $candidates+=(Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe') }
 foreach ($p in $candidates) {
  if (!$p -or !(Test-Path -LiteralPath $p)) { continue }
  try { & $p -c "import sys; raise SystemExit(0 if sys.version_info[:2]==(3,12) else 1)" 2>$null
   if ($LASTEXITCODE -eq 0) { return $p }
  } catch {}
 }
 return $null
}
try {
 Refresh-Tools
 $venv=Join-Path $kitRoot '.venv\Scripts\python.exe'
 $config=Join-Path $kitRoot 'tools\tubescribe\config.toml'
 if ($Action -eq 'Verify') {
  Write-Host 'Diagnostic sans installation ni envoi de document.'
  foreach ($name in @('claude','codex','git','node','python','ffmpeg','deno')) { Write-Host ($name+' : '+(Version $name)) }
  Write-Host 'Claude Code OU Codex : assistant au choix. Git : facultatif. Node LTS : installation Codex par npm.'
  Write-Host 'Python 3.12, FFmpeg et Deno : option video uniquement. Obsidian : lecteur facultatif.'
  if (Test-Path -LiteralPath $venv) {
   & $venv -c "import yt_dlp, faster_whisper; print('Modules video : OK')"
   if ($LASTEXITCODE -ne 0) { Write-Host 'Modules incomplets : INSTALLER-VIDEOS.cmd.' }
  } else { Write-Host 'Option video non installee.' }
  Write-Host 'Comptes Claude et ChatGPT non testes. Le kit ne fournit aucun abonnement IA.'
  if (!(Has-Tool 'claude') -and !(Has-Tool 'codex')) { Write-Host 'Etape suivante : INSTALLER.cmd'; exit 2 }
  Write-Host 'Etape suivante : OUVRIR-CERVEAU.cmd puis connexion a votre compte.'
  exit 0
 }
 if ($Action -eq 'Install' -or $Action -eq 'Open') {
  Write-Host '1. Claude Code (compte Claude compatible)'
  Write-Host '2. Codex (compte ChatGPT avec acces Codex)'
  $choice=Read-Host 'Votre assistant [1/2]'
  if ($choice -notin @('1','2')) { throw 'Choisissez 1 ou 2. Aucun changement.' }
  $engine=if ($choice -eq '1') { 'claude' } else { 'codex' }
  if ($Action -eq 'Install') {
   if ($engine -eq 'claude') {
    Offer 'claude' 'Anthropic.ClaudeCode' 'https://code.claude.com/docs/en/setup'
   } elseif (!(Has-Tool 'codex')) {
    Offer 'node' 'OpenJS.NodeJS.LTS' 'https://nodejs.org'
    if (!(Has-Tool 'npm.cmd')) { throw 'Node/npm absent. Relancez apres installation de Node LTS.' }
    $major=& node -p 'parseInt(process.versions.node)'
    if ($LASTEXITCODE -ne 0 -or [int]$major -lt 22) { throw 'Installez Node.js LTS recent (22 minimum), puis relancez.' }
    if ((Read-Host 'Installer le paquet officiel @openai/codex via npm ? [o/N]') -ne 'o') { throw 'Installation annulee.' }
    & npm.cmd install -g '@openai/codex'
    if ($LASTEXITCODE -ne 0) { throw 'Installation Codex non terminee.' }
    Refresh-Tools
   }
   if (!(Has-Tool $engine)) { throw 'Relancez VERIFIER.cmd dans une nouvelle fenetre pour actualiser le PATH.' }
   & $engine --version
   if ($LASTEXITCODE -ne 0) { throw 'Votre assistant ne demarre pas correctement.' }
   Write-Host 'Assistant disponible. Lancez OUVRIR-CERVEAU.cmd et connectez votre compte.'
   exit 0
  }
  if (!(Has-Tool $engine)) { throw 'Cet assistant manque. Lancez INSTALLER.cmd.' }
  & $engine
  exit $LASTEXITCODE
 }
 if ($Action -eq 'InstallVideo') {
  $pythonPath=Python312
  if (!$pythonPath) {
   if (!(Has-Tool 'winget')) { throw 'Installez Python 3.12 depuis python.org.' }
   if ((Read-Host 'Installer Python 3.12 via WinGet ? [o/N]') -ne 'o') { throw 'Option annulee.' }
   & winget install --exact --id Python.Python.3.12 --source winget
   if ($LASTEXITCODE -ne 0) { throw 'Installation Python non terminee.' }
   Refresh-Tools
   $pythonPath=Python312
   if (!$pythonPath) { throw 'Relancez ce fichier dans une nouvelle fenetre pour detecter Python 3.12.' }
  }
  Offer 'ffmpeg' 'Gyan.FFmpeg' 'https://ffmpeg.org'
  Offer 'deno' 'DenoLand.Deno' 'https://deno.com'
  if (!(Has-Tool 'ffmpeg') -or !(Has-Tool 'deno')) { throw 'Relancez dans une nouvelle fenetre pour actualiser le PATH.' }
  if (!(Test-Path -LiteralPath $venv)) {
   & $pythonPath -m venv (Join-Path $kitRoot '.venv')
   if ($LASTEXITCODE -ne 0) { throw 'Creation de .venv impossible.' }
  }
  & $venv -m pip install -r (Join-Path $kitRoot 'tools\tubescribe\requirements.txt')
  if ($LASTEXITCODE -ne 0) { throw 'Installation des modules incomplete.' }
  & $venv -c "import yt_dlp, faster_whisper"
  if ($LASTEXITCODE -ne 0) { throw 'Modules video non utilisables.' }
  & $venv -m pip freeze | Set-Content -LiteralPath (Join-Path $kitRoot '.venv\installed-requirements.txt')
  & $venv (Join-Path $kitRoot 'tools\setup.py')
  if ($LASTEXITCODE -ne 0) { throw 'Configuration non terminee.' }
  Write-Host 'Option video installee. Ajoutez vos liens dans youtube.md, puis TRAITER-VIDEOS.cmd.'
  exit 0
 }
 if (!(Test-Path -LiteralPath $venv) -or !(Test-Path -LiteralPath $config)) { throw 'Lancez INSTALLER-VIDEOS.cmd.' }
 Set-Location -LiteralPath (Join-Path $kitRoot 'tools\tubescribe')
 & $venv -m tubescribe --config $config watch
 if ($LASTEXITCODE -ne 0) { throw 'Traitement incomplet. Les sources sont conservees. Consultez les erreurs.' }
 Write-Host 'Termine : notes dans raw\youtube. Ouvrez Claude Code ou Codex, puis demandez de les resumer et de les classer.'
} catch { Write-Host ('[!] '+$_.Exception.Message) -ForegroundColor Red; exit 1 }
