# 实时天气查询工具

这是一个基于 Python Flask 和原生前端技术的实时天气查询 Web 应用，支持通过城市名查询实时天气及预报。

[![Build and Push Docker Image](https://github.com/USERNAME/weather-app/actions/workflows/docker-build.yml/badge.svg)](https://github.com/USERNAME/weather-app/actions/workflows/docker-build.yml)

## 功能特性

- 实时天气查询（温度、天气状况、风力风向、湿度等）
- 响应式设计，支持移动端和桌面端
- 容器化部署，便于快速部署和扩展
- GitHub Actions 自动化构建和推送 Docker 镜像到 GHCR
- 完善的配置管理和日志系统

## 技术栈

- 后端：Python 3.8+ + Flask 2.0+
- 前端：HTML5 + CSS3 + JavaScript（原生）
- 配置：YAML 格式（支持环境变量注入）
- 日志：Python logging 模块（控制台+文件输出，支持轮转）
- 容器化：Docker + Dockerfile
- 自动化部署：GitHub Actions
- 容器仓库：GitHub Container Registry (GHCR)
- 第三方服务：和风天气免费API

## 快速开始

### 1. 本地运行

1. 克隆项目：
   ```bash
   git clone <repository-url>
   cd weather-app
   ```

2. 创建虚拟环境并激活：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate     # Windows
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 配置和风天气 API Key：
   ```bash
   # 复制配置文件
   cp config/config.default.yaml config/config.yaml
   
   # 编辑 config/config.yaml 文件，填入你的和风天气 API Key
   ```

5. 运行应用：
   ```bash
   python app.py
   ```

6. 访问应用：http://localhost:5001

### 2. Docker 运行

1. 构建镜像：
   ```bash
   docker build -t weather-app .
   ```

2. 运行容器：
   ```bash
   docker run -d -p 5001:5001 --name weather-app weather-app
   ```

3. 访问应用：http://localhost:5001

### 3. 从 GHCR 拉取镜像运行

1. 登录 GHCR（需要 GitHub Personal Access Token）：
   ```bash
   echo $GHCR_PAT | docker login ghcr.io -u <用户名> --password-stdin
   ```

2. 拉取镜像：
   ```bash
   docker pull ghcr.io/<用户名>/weather-app:latest
   ```

3. 运行容器：
   ```bash
   docker run -d -p 5001:5001 --name weather-app ghcr.io/<用户名>/weather-app:latest
   ```

## 配置说明

应用支持多种配置方式，优先级从高到低为：

1. 环境变量
2. `config/config.yaml`
3. `config/config.default.yaml`

### 主要配置项

| 配置项 | 环境变量 | 说明 |
|--------|---------|------|
| 服务器主机 | HOST | 默认: 0.0.0.0 |
| 服务器端口 | PORT | 默认: 5001 |
| 调试模式 | DEBUG | 默认: false |
| 和风天气API Key | WEATHER_API_KEY | 必须配置 |
| 日志等级 | LOG_LEVEL | 默认: INFO |

## GitHub Actions 自动化

项目配置了 GitHub Actions 工作流，实现自动构建和推送 Docker 镜像到 GHCR：

- 推送到 `main` 分支时：自动构建并推送镜像
- 提交 PR 到 `main` 分支时：仅构建镜像不推送
- 手动触发：通过 GitHub 界面执行构建

## 项目结构

```
weather-app/
├── app.py                    # 后端主程序（Flask入口）
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

## 获取和风天气 API Key

1. 访问 [和风天气开发者平台](https://dev.qweather.com/)
2. 注册账号并登录
3. 创建应用并获取 API Key
4. 将 API Key 配置到应用中

## 许可证

MIT