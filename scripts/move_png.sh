#!/bin/bash

# 指定目标目录名称（可根据需要修改）
target_dir="all_png_files"

# 创建目标目录（如果不存在）
mkdir -p "$target_dir"

# 使用 find 命令递归搜索所有 .png 文件并移动到目标目录
find "乒乓球4" -type f -iname "*.png" -exec mv -t "$target_dir" {} +

echo "所有 png 文件已移动到 $target_dir 目录"
