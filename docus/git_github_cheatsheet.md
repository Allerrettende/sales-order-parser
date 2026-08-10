# Git + GitHub 速查表

> 日常开发最常用的 Git 命令和 GitHub 操作，按场景分类。

---
## Git使用步骤
### 首次使用配置Git
```bash
# 配置全局用户信息
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱"
# 检查：
git config --list
# 初始化Git,创建本地仓库
cd D:\PythonProjects\Python-Learning

# 1. 本地已有项目
git init
git add .
git commit -m "first commit"

# 2. 去 GitHub 网页新建一个仓库（空的，不要创建 README）

# 3. 关联本地和远程仓库 origin = 远程仓库的代号（你可以理解为给网址起的昵称）
git remote add origin git@github.com:RunCao2004/Python-Learning.git

# 4. 推送代码到远程
git branch -M main #本地分支名改为main, GitHub 默认主分支叫 main,Git 默认主分支叫 master
git push -u origin main

# 5. 连接GitHub有二种方式，见后面介绍。
# https
git remote set-url origin https://github.com/RunCao2004/Python-Learning.git
# SSH
git remote add origin git@github.com:RunCao2004/Python-Learningt.git

```
### 日常使用
```bash
git status
git add .
git commit -m "Complete day01 Python basic"
git push

```
## 📦 安装与配置

### 首次配置（全局）
```bash
# 设置用户名和邮箱（提交时会显示）
git config --global user.name "你的名字"
git config --global user.email "your.email@example.com"

# 设置默认编辑器
git config --global core.editor "code --wait"   # VSCode

# 查看所有配置
git config --list
```

## SSH 配置（连接 GitHub）
```bash
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your.email@example.com"
# 保存在 C:\Users\Lian.Cao\.ssh

# 查看公钥，复制后添加到 GitHub Settings → SSH and GPG keys
cat ~/.ssh/id_ed25519.pub

# 测试连接
ssh -T git@github.com
```

### SSH 密钥是"电脑+用户"级别的
```bash
# SSH 密钥是绑定在当前电脑的当前用户账户上的，换电脑后不能直接使用。
# 在新电脑生成新密钥，操作同上。
```

### 验证当前电脑的 SSH 密钥位置
```bash
# 查看你当前的公钥
cat ~/.ssh/id_ed25519.pub

# 查看密钥文件位置
ls ~/.ssh/

```

### 💡 重要提示

```bash
🔐 私钥安全
#id_ed25519（没有 .pub）是私钥，绝对不能泄露！
- 不要发送给任何人
- 不要在 GitHub 上公开
- 不要放在网盘或公开仓库

📦 备份建议
# 如果你经常换电脑，可以把
 ~/.ssh/id_ed25519.pub（公钥）存到云盘/密码管理器（安全）
私钥 id_ed25519 备份到加密 U 盘或 1Password 等安全工具

```
## HTTPS连接
```bash
# 1. 克隆用 HTTPS
git clone https://github.com/RunCao2004/Python-Learning.git

# 2. 第一次推送时输入 Token
git push
# Username: RunCao2004
# Password: 粘贴你的 Token

# 3. 配置凭证缓存（避免每次都输入）
git config --global credential.helper manager

# 之后推送就不用再输了
```

## 🔄 两种方式随时切换
```bash
# 切到 HTTPS
git remote set-url origin https://github.com/RunCao2004/Python-Learning.git

# 切回 SSH
git remote set-url origin git@github.com:RunCao2004/Python-Learning.git

```

## clone 步骤

安装好Python, Vscode, Git.
创建主目录，要Clone的目录不用创建，clone时会自动创建。
1. clone 用https连接
```bash
git clone https://github.com/RunCao2004/Python-Learning.git
```
2. 在python-learning下，创建虚拟环境，导入依赖模块.
```bash
python -m venv .venv
set-ExecutionPolicy RemoteSigned
.\.venv\scripts\activate
pip install -r requirements.txt

```
3. 配置当地仓库，初始化
```bash
git config --global user.name "allerrettende"
git config --global user.email "run.cao@outlook.com"

git init
git add.
git commit

```

4.  使用SSH方式和GitHub建立远程连接
```bash
ssh-keygen -t ed25519 -C "run.cao@outlook.com"
cat ~/.ssh/id_ed25519.pub
ssh - T git@github.com
git remote set-url origin git@ggithub.com/RunCao2004/Python-Learning.git
git push
```



