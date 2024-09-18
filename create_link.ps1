Remove-Item -Path "./include/nagisa" -Recurse
New-Item -Path "./include/nagisa" -ItemType Directory
python ./tools/create_link/main.py ./include/nagisa ./submodules
