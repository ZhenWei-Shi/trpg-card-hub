# TRPG Card Hub

**专为口述团和自制规则设计的在线角色卡共享系统**

DM 在后台配置规则，玩家手机打开链接填卡——不需要安装任何软件，不需要传 Excel 文件。

---

## 为什么做这个

口述团和小规则跑团通常没有专属工具支持。玩家要么手写卡，要么用 Excel 本地存储。出门在外无法查看角色卡，DM 也难以统一管理所有玩家的角色信息。

这个系统解决的核心问题：
- 玩家离家时用手机查看自己的角色卡
- DM 在一个页面看到所有玩家的角色状态
- 任何自制规则都可以在后台配置，无需改代码

---

## 功能

- **后台规则配置** — 设置属性名称、初始值、说明文字，开关显示模块，调整主题颜色
- **战役房间系统** — DM 创建房间，复制邀请链接发给玩家，角色卡按战役归档
- **角色卡共享** — 所有数据存在服务器，URL 即档案，手机直接访问
- **密码保护** — 每张角色卡可设密码，保护隐私信息
- **DM 总览** — 后台查看所有玩家角色卡，包含属性和密码

---

## 部署方式

### 本地运行（开发 / 局域网使用）

```bash
# Python 直接运行
pip install -r requirements.txt
python app.py

# 或 Docker
docker-compose up -d
```

访问 `http://localhost:5000`

---

### 云部署（推荐 · 让玩家随时访问）

> 云部署后服务 24/7 运行，玩家无需 DM 在线即可查看角色卡。

#### Railway（最简单，有免费额度）

1. Fork 本仓库到你的 GitHub
2. 登录 [Railway](https://railway.app) → New Project → Deploy from GitHub repo
3. 选择你 fork 的仓库，Railway 自动识别 Dockerfile 并部署
4. 进入项目 → **Volumes** → Add Volume，挂载路径填 `/app/data`（持久化数据库）
5. 部署完成后在 **Settings → Domains** 生成公开域名

> 可选：在 Variables 里设置 `SECRET_KEY` 为随机字符串，提高 session 安全性。

#### Render

1. Fork 本仓库到你的 GitHub
2. 登录 [Render](https://render.com) → New → Web Service → 连接仓库
3. Runtime 选 **Docker**，Render 会自动读取 `render.yaml` 配置
4. `render.yaml` 已预配置 1GB 持久磁盘挂载至 `/app/data`
5. 点击 **Create Web Service**，等待部署完成

> Render 免费套餐无持久磁盘，数据会在重启后丢失。建议使用 Starter 套餐（$7/月）。

#### 阿里云 / 腾讯云（国内访问推荐）

> 适合玩家全在国内的团，访问速度最佳，价格约 **24 元/月**。

**推荐机型：**

| 产品 | 最低配置 | 参考价格 |
|------|---------|---------|
| 阿里云轻量应用服务器 | 1 核 1G | ~24 元/月 |
| 腾讯云轻量应用服务器 | 1 核 1G | ~24 元/月 |
| 华为云耀云服务器 | 1 核 1G | ~25 元/月 |

**部署步骤（阿里云 / 腾讯云 / 华为云步骤相同）：**

```bash
# 1. 购买轻量应用服务器，镜像选 Ubuntu 22.04，SSH 登录后执行：

# 2. 安装 Docker（国内镜像加速）
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun

# 3. 安装 docker-compose
apt install -y docker-compose-plugin

# 4. 拉取项目
git clone https://github.com/ZhenWei-Shi/trpg-card-hub
cd trpg-card-hub

# 5. 设置环境变量（可选但推荐）
cp .env.example .env
# 编辑 .env，修改 SECRET_KEY

# 6. 启动服务
docker compose up -d
```

```bash
# 7. 开放端口（在云控制台防火墙 / 安全组放行 5000 端口）
# 阿里云：控制台 → 轻量应用服务器 → 防火墙 → 添加规则 → TCP 5000
# 腾讯云：控制台 → 轻量应用服务器 → 防火墙 → 添加规则 → TCP 5000
# 华为云：控制台 → 安全组 → 入方向规则 → TCP 5000
```

访问 `http://你的服务器公网IP:5000`

> **绑定域名（可选）：** 将域名解析到服务器 IP，配置 Nginx 反向代理到 5000 端口，并申请免费 SSL 证书（Let's Encrypt）。

---

#### 环境变量说明

复制 `.env.example` 为 `.env` 后按需修改：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `PORT` | 服务监听端口（云平台自动注入） | `5000` |
| `SECRET_KEY` | Session 加密密钥，生产环境请务必修改 | 内置默认值 |

---

## 使用流程

```
1. DM 登录后台（默认密码：dm123456）
   └── 规则配置 Tab → 设置属性、字段名、显示模块

2. DM 创建战役房间
   └── 战役房间 Tab → 新建 → 复制邀请链接发给玩家

3. 玩家打开链接
   └── 按 DM 配好的规则填写角色卡，设置密码保护

4. 随时查看
   └── 手机打开房间链接 → 输入密码 → 查看角色卡
```

---

## 配置说明

所有规则配置通过 **DM 后台 → 规则配置** 完成，无需编辑任何文件：

| 配置项 | 说明 |
|--------|------|
| 属性列表 | 自定义属性名、缩写、初始值、最小值、说明文字 |
| 字段名称 | 修改"职业/外貌/背景"等字段的显示名和提示文字 |
| 显示模块 | 开关特性区、技能区、物品区 |
| 主题颜色 | 主色调、背景色、边框色 |

修改后玩家刷新建卡页即时生效，现有角色卡数据不受影响。

---

## 修改默认 DM 密码

部署后请修改 `config.json` 中的密码：

```json
{
  "admin": {
    "password": "你的新密码"
  }
}
```

---

## 技术栈

- Python 3.11 / Flask
- SQLite（数据存储在 `data/characters.db`）
- 原生 HTML / CSS / JavaScript（无框架依赖）

---

## License

MIT — 随意 fork 部署成自己的版本
