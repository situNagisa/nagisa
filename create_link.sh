#!/bin/bash

# 确定目标链接目录
TARGET_DIR="$(realpath .)/include/nagisa"
echo "target dir: $TARGET_DIR"

# 创建目标目录（如果不存在）
mkdir -p "$TARGET_DIR"

# 遍历子项目目录
for project in ./submodules/*; do
    if [ -d "$project/include/nagisa" ]; then
        project_name=$(basename "$project")
        symlink_path="$TARGET_DIR/$project_name"

        # 检查链接是否存在
        if [ -L "$symlink_path" ]; then
            echo "Link for $project_name already exists. Updating..."
            rm "$symlink_path"  # 删除旧链接
        fi

        ln -s "$(realpath .)/submodules/$project_name/include/nagisa/$project_name" "$symlink_path"
        echo "Created symlink for $project_name in $TARGET_DIR"
    fi
done

echo "All links created."