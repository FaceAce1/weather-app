# Weather App - 实时天气查询工具

[![Build and Push Docker Image](https://github.com/FaceAce1/weather-app/actions/workflows/docker-build.yml/badge.svg)](https://github.com/FaceAce1/weather-app/actions/workflows/docker-build.yml)

这是一个基于 Python Flask 和原生前端技术的实时天气查询 Web 应用，支持通过城市名查询实时天气及预报。

## 功能特性

- 🌤️ 实时天气查询：通过城市名获取当前天气信息
- 📱 响应式设计：支持移动端和桌面端访问
- ⚙️ 多配置方式：支持环境变量、配置文件等多种配置方式
- 🐳 Docker支持：提供Docker镜像便于部署
- 📜 日志记录：支持日志文件轮转和控制台输出
- 🔧 API集成：集成和风天气API获取准确的天气数据

## 技术架构

### 整体架构

```
+---------------------+
|     前端界面        |
|  (HTML/CSS/JS)      |
+----------+----------+
           |
+----------v----------+
|     后端服务        |
|  (Python Flask)     |
+----------+----------+
           |
+----------v----------+
|  第三方API服务      |
| (和风天气API)       |
+---------------------+
```

### 技术栈

- 后端框架：Python Flask 2.0+
- 前端技术：HTML5 + CSS3 + 原生JavaScript
- 样式框架：Tailwind CSS + Font Awesome
- 构建工具：Docker
- 配置管理：YAML + 环境变量
- 日志系统：Python logging模块 + 文件轮转
- API服务：和风天气免费API

## 快速开始

### 1. 环境要求

- Python 3.8+
- pip 包管理器
- 和风天气API Key（免费获取：https://dev.qweather.com/）

### 2. 本地运行

1. 克隆项目：
```bash
git clone <repository-url>
cd weather-app
```

2. 创建虚拟环境并激活：
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置API密钥：
```bash
# 复制配置文件
cp config/config.default.yaml config/config.yaml

# 编辑配置文件，填入您的和风天气API Key
vim config/config.yaml
```

5. 运行应用：
```bash
python app.py
```

6. 访问应用：
打开浏览器访问 http://localhost:5001

### 3. Docker部署

1. 构建Docker镜像：
```bash
docker build -t weather-app .
```

2. 运行容器：
```bash
docker run -d \
  -p 5001:5001 \
  -e WEATHER_API_KEY="your_api_key_here" \
  --name weather-app \
  weather-app
```

3. 访问应用：
打开浏览器访问 http://localhost:5001

## 配置说明

应用支持多种配置方式，优先级从高到低为：

1. 环境变量
2. `config/config.yaml`
3. `config/config.default.yaml`

### 支持的配置项

| 配置项 | 环境变量 | 说明 |
|--------|---------|------|
| debug | DEBUG | 调试模式开关 |
| server.host | HOST | 服务器监听地址 |
| server.port | PORT | 服务器监听端口 |
| weather_api.key | WEATHER_API_KEY | 和风天气API密钥 |
| weather_api.url | WEATHER_API_URL | 天气API地址 |
| log.level | LOG_LEVEL | 日志级别 |
| log.file | LOG_FILE | 日志文件路径 |

## 项目结构

```
weather-app/
├── app.py                    # 主程序（Flask入口）
├── requirements.txt          # Python依赖清单
├── README.md                 # 项目说明文档
├── Dockerfile                # Docker镜像构建配置
├── .dockerignore             # Docker构建忽略文件
├── .gitignore                # Git版本控制忽略文件
├── .github/                  # GitHub Actions配置目录
│   └── workflows/
│       └── docker-build.yml  # 自动构建并推送Docker镜像到GHCR的工作流配置
├── static/                   # 前端静态资源
│   ├── css/
│   │   └── style.css         # 页面样式
│   ├── js/
│   │   └── script.js         # 前端交互逻辑
│   └── images/               # 天气图标
├── templates/
│   └── index.html            # 主页面（输入+结果展示）
├── config/                   # 配置文件目录
│   ├── config.default.yaml   # 示例配置（含注释，纳入版本控制）
│   └── config.yaml           # 实际配置（自动生成，不纳入版本控制）
├── logs/                     # 日志文件目录（自动创建）
└── utils/                    # 工具函数目录
    ├── __init__.py           # 包初始化
    ├── config_utils.py       # 配置加载/复制/环境变量处理
    ├── logger_utils.py       # 日志初始化/轮转配置
    └── weather_api.py        # 和风天气API调用/数据解析
```

## 核心模块说明

### 1. 配置管理模块 (utils/config_utils.py)

- 支持多级配置来源（优先级从高到低）：
  1. 环境变量
  2. config.yaml
  3. config.default.yaml
- 配置合并策略：深度合并嵌套字典

### 2. 日志模块 (utils/logger_utils.py)

- 支持双输出：
  - 控制台输出
  - 文件输出（带轮转）
- 日志格式：
  `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- 支持日志级别配置（DEBUG, INFO, WARNING, ERROR, CRITICAL）

### 3. 天气API模块 (utils/weather_api.py)

- 功能：
  - 城市信息查询
  - 实时天气数据获取
  - 错误处理和重试机制
- 请求流程：
  1. 查询城市ID
  2. 使用城市ID获取天气数据
- 异常处理：
  - 网络错误处理
  - API错误处理
  - 数据解析错误处理

### 4. 主程序 (app.py)

- 路由说明：
  - [/](#)：首页（返回HTML模板）
  - `/api/weather`：获取天气数据（GET请求）
- 配置加载流程：
  1. 在文件顶部立即加载配置
  2. 支持环境变量覆盖
  3. 调试模式自动转换为布尔值

### 5. 前端界面 (templates/index.html)

- 响应式设计：
  - 移动端优化
  - 桌面端适配
- 主要组件：
  - 城市搜索输入框
  - 天气结果卡片
  - 详细天气数据卡片
  - 加载状态指示
  - 错误提示

### 6. 前端脚本 (static/js/script.js)

- 核心功能：
  - 事件监听（点击、回车）
  - 天气数据获取
  - 数据展示
  - 状态管理（加载、错误）
- 天气图标映射：
  - 根据天气代码显示对应图标
- 数据格式化：
  - 时间格式转换
  - 单位添加
  - 状态提示

## API接口说明

### 天气数据API

- 请求方法：GET
- 请求路径：`/api/weather`
- 请求参数：
  - city: 城市名称（必填）
  
- 请求示例：
```bash
curl "http://localhost:5001/api/weather?city=北京"
```

- 响应示例：
```json
{
  "city": "北京",
  "code": "200",
  "updateTime": "2023-07-25T15:30+08:00",
  "fxLink": "https://www.qweather.com/weather/beijing-101010100.html",
  "now": {
    "temp": "32",
    "feelsLike": "35",
    "text": "晴",
    "wind360": "180",
    "windDir": "南风",
    "windScale": "2",
    "windSpeed": "10",
    "humidity": "40",
    "pressure": "1005",
    "vis": "10",
    "precip": "0.0",
    "cloud": "10",
    "dew": "25"
  },
  "refer": {
    "sources": ["QWeather"]
  }
}
```

## 部署建议

### 生产环境部署

1. 设置环境变量：
```bash
export FLASK_ENV=production
export WEATHER_API_KEY="your_production_api_key"
```

2. 使用反向代理（如Nginx）：
```
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. 配置HTTPS证书

### 日志管理

- 建议定期清理日志
- 可配置日志轮转策略
- 错误日志应定期检查

## 开发指南

### 本地开发

1. 克隆项目
2. 创建虚拟环境
3. 安装依赖
4. 配置API密钥
5. 运行应用

### 调试技巧

- 启用调试模式：
  - 设置`DEBUG=true`
  - 查看详细日志
- 使用浏览器开发者工具：
  - 查看网络请求
  - 检查控制台输出
- 日志分析：
  - 查看控制台输出
  - 检查日志文件

## 许可证

本项目采用 MIT 许可证，详情请见 [LICENSE](LICENSE) 文件。
