# TRPG Card Hub

一个开源、可自定义的 TRPG 跑团角色卡管理系统。只需修改 `config.json`，即可适配任意规则系统（武侠、克苏鲁、D&D、赛博朋克等）。

## 功能

- 📝 角色卡创建与编辑
- 📜 角色卡大厅（支持密码保护）
- 🎨 主题颜色完全自定义
- ⚙️ 属性名称、货币系统可配置
- 📚 世界观参考侧边栏
- 🐳 Docker 一键部署

## 快速开始

### 方式一：直接运行

```bash
pip install flask
python app.py
```

访问 http://localhost:5000

### 方式二：Docker（推荐）

```bash
docker compose up -d
```

## 自定义你的跑团系统

编辑根目录下的 `config.json`：

```json
{
  "app": {
    "name": "你的站点名称",
    "description": "副标题"
  },
  "theme": {
    "primary_color": "#8b2121",
    "bg_color": "#f4eee1",
    "border_color": "#cbb494"
  },
  "character": {
    "stats": [
      {"key": "str", "label": "力量", "short": "力", "min": 6, "default": 6}
    ]
  },
  "currency": {
    "enabled": true,
    "units": [
      {"key": "gold", "label": "金币", "rate": 100}
    ]
  }
}
```

### 改为 D&D 主题示例

```json
{
  "app": { "name": "D&D Character Vault", "description": "角色卡管理系统" },
  "theme": { "primary_color": "#2c5282", "bg_color": "#ebf4ff", "border_color": "#90cdf4" },
  "character": {
    "stats": [
      {"key": "str", "label": "力量", "short": "STR", "min": 1, "default": 10},
      {"key": "dex", "label": "敏捷", "short": "DEX", "min": 1, "default": 10},
      {"key": "con", "label": "体质", "short": "CON", "min": 1, "default": 10},
      {"key": "int", "label": "智力", "short": "INT", "min": 1, "default": 10},
      {"key": "wis", "label": "感知", "short": "WIS", "min": 1, "default": 10},
      {"key": "cha", "label": "魅力", "short": "CHA", "min": 1, "default": 10}
    ],
    "fields": {
      "realm":      {"label": "职业/等级", "placeholder": "例如：战士 Lv.5"},
      "appearance": {"label": "外貌",      "placeholder": "描述角色外貌"},
      "background": {"label": "背景故事",  "placeholder": "角色的背景故事"}
    }
  },
  "currency": { "enabled": false }
}
```

## 项目结构

```
trpg-card-hub/
├── app.py              # Flask 后端
├── config.json         # 游戏主题配置（修改这里来自定义）
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── templates/
    ├── index.html      # 主页
    ├── player.html     # 建卡/编辑页
    └── char_list.html  # 角色卡大厅
```

## License

MIT
