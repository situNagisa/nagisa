

# 确定目标链接目录
$targetDir = ".\include\nagisa"

# 创建目标目录（如果不存在）
if (-not (Test-Path -Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir
}

# 遍历子项目目录
Get-ChildItem -Path ".\submodules" -Directory | ForEach-Object {
    $projectName = $_.Name
    $project = $_.FullName
    $includePath = Join-Path -Path $project -ChildPath "include\nagisa"
    $includePath = Join-Path -Path $includePath -ChildPath $projectName
    $symlinkPath = Join-Path -Path $targetDir -ChildPath $projectName

    if (Test-Path -Path $includePath) {
        # 检查链接是否存在
        if (Test-Path -Path $symlinkPath) {
            Write-Host "Link for $projectName already exists. Updating..."
            Remove-Item -Path $symlinkPath # 删除旧链接
        }

        cmd /c mklink /D "$symlinkPath" "$includePath"
        Write-Host "Created symlink for $projectName in $targetDir"
    }
}

Write-Host "All links created."