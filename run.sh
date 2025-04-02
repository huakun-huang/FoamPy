#!/bin/bash

# 获取脚本所在目录的绝对路径（自动处理符号链接）
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# 将路径追加到PATH并写入.bashrc
echo "export PYTHONPATH=\"\${PYTHONPATH}:$SCRIPT_DIR\"" >> ~/.bashrc

# 将路径追加到PATH并写入.bashrc
echo "export PYTHONPATH=\"\${PYTHONPATH}:$SCRIPT_DIR/material\"" >> ~/.bashrc

# 提示用户
echo "已将脚本目录添加到 PYTHONPATH: $SCRIPT_DIR"
echo "执行以下命令使配置生效："
echo "source ~/.bashrc"