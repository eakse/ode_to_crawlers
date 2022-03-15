# simple script to automate some boring stuff



.\venv\Scripts\Activate.ps1
python.exe -m pip install --upgrade pip
pip install -r .\requirements.txt
# $setupPyPath = '.\setup.py'
# $contents = [System.IO.File]::ReadAllText($setupPyPath)
# $versionString = [RegEx]::Match($contents,"(version\=\'\d+\.\d+\',)")
# $currentBuild = [RegEx]::Match($versionString,"(\.)(\d+)(')").Groups[2]
# $newBuild= [int]$currentBuild.Value + 1
# $contents = [RegEx]::Replace($contents, "(version=\'\d+\.)(?:\d+)(\',)", ("`${1}" + $newBuild.ToString() + "`${2}"))
# [System.IO.File]::WriteAllText($setupPyPath, $contents)

git add *
git commit -m "$(Get-Date -Format G)"
git push