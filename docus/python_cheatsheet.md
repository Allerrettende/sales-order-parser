# Python 速查

## 打开 Terminal
快捷键：
Ctrl + `

## 创建虚拟环境：
```bash
python -m venv .venv
```
## 激活 Python 虚拟环境
```bash
.\.venv\Scripts\activate
```
成功后：
(.venv) PS D:\PythonProjects\Python-Learning>

## 保存项目依赖
```bash
pip freeze > requirements.txt
```

# .py文件误删恢复
1. VS Code 中按下 Ctrl+Shift+P 打开命令面板。输入 Local History: Find Entry to Restore 并选择它。然后输入你被删除的文件名 main.py，看看是否能找到并恢复它
2. Time line查找删除的文件，按右键恢复。
