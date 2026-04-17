# 「天眼稻守」技术方案

## 文档信息
| 项目 | 内容 |
|------|------|
| 项目名称 | 天眼稻守 |
| 版本 | v1.0 |
| 创建日期 | 2026-04-17 |
| 状态 | 草稿 |

---

## 一、技术架构总览

### 1.1 系统架构图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              用户层                                          │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│   │ 飞书机器人 │  │ 多维表格  │  │ Web后台  │  │  移动H5  │  │  微信小程序 │    │
│   └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            API网关层                                        │
│                         Nginx / uvicorn                                     │
│                    (路由 / 认证 / 限流 / 日志)                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐
│   数据采集服务     │   │    分析服务       │   │    协作服务       │
│   (Data Agent)    │   │  (Analysis Agent) │   │ (Collaboration)   │
│                   │   │                   │   │                   │
│ • Sentinel-2采集  │   │ • NDVI计算        │   │ • 飞书消息推送    │
│ • 气象数据拉取     │   │ • 产量预测        │   │ • 多维表格同步    │
│ • 地块数据同步     │   │ • 病虫害识别      │   │ • 周报生成        │
│ • 数据清洗入库     │   │ • 风险评估        │   │ • 任务创建        │
└─────────┬─────────┘   └─────────┬─────────┘   └─────────┬─────────┘
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             数据层                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ PostgreSQL  │  │ TimescaleDB │  │   MongoDB   │  │   MinIO     │        │
│  │  (关系数据)  │  │  (时序数据)  │  │  (文档存储)  │  │  (文件存储)  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             外部数据源                                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Sentinel-2  │  │  气象API    │  │  地块GIS    │  │  农业统计    │        │
│  │  卫星影像    │  │             │  │             │  │             │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 核心服务说明

| 服务名称 | 技术栈 | 功能描述 | 部署方式 |
|----------|--------|----------|----------|
| Data Agent | Python 3.10+ / schedule / Prefect | 定时采集卫星、气象、地块数据 | Docker |
| Analysis Agent | Python / PyTorch / scikit-learn | NDVI计算、产量预测、病虫害识别 | Docker |
| Collaboration | Python / FastAPI / 飞书SDK | 消息推送、表格同步、报告生成 | Docker |
| API Gateway | Nginx / FastAPI | 统一入口、路由、认证 | Docker |
| Web Backend | Python / FastAPI | 管理后台API | Docker |
| Web Frontend | Vue3 / Element Plus / Leaflet | 管理后台界面 | Nginx |

---

## 二、数据采集模块

### 2.1 Sentinel-2 卫星数据采集

**采集策略**：
- 目标分辨率：10米（Band 4/8/11）
- 采集频率：每7天一次（云遮挡严重时顺延）
- 区域覆盖：示范地块边界外扩500米

**数据源**：
| 数据源 | 用途 | 访问方式 |
|--------|------|----------|
| Copernicus Open Access Hub | 主数据源 | API (scihub.copernicus.eu) |
| Sentinel Hub | 备用/快速访问 | API (www.sentinel-hub.com) |
| AWS Public Dataset | 归档数据 | AWS CLI |

**NDVI计算公式**：
```
NDVI = (NIR - Red) / (NIR + Red)
     = (B08 - B04) / (B08 + B04)
```

**预处理流程**：
```
原始影像 → 云掩膜(S2Cloudless) → 大气校正 → 地形校正
     ↓
地块裁剪 → 重采样(统一分辨率) → 月度合成(MEDIAN) → NDVI计算
     ↓
时序入库
```

### 2.2 气象数据采集

**数据源**：
| 数据源 | 内容 | 更新频率 | 访问方式 |
|--------|------|----------|----------|
| 国家气象局API | 温度、降水、日照 | 每日 | HTTP API |
| 和风天气API | 气象预警、实况 | 实时 | HTTP API |
| 农业气象站 | 积温、蒸发量 | 每日 | 地方共享 |

**关键气象因子**：
- 日均温度、积温（生长季累计）
- 降水量、降水天数
- 日照时数
- 相对湿度
- 气象灾害预警（干旱、洪涝、台风）

### 2.3 地块边界数据

**数据格式**：GeoJSON / Shapefile
**坐标系**：WGS84 (EPSG:4326)
**字段要求**：
```json
{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "properties": {
      "plot_id": "PLOT_001",
      "plot_name": "王大哥-示范田",
      "area_mu": 50.5,
      "crop_type": "rice",
      "variety": "杂交稻",
      "owner": "王大哥",
      "phone": "138xxxx"
    },
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[lng, lat], ...]]
    }
  }]
}
```

---

## 三、数据存储方案

### 3.1 数据库选型

| 数据库 | 用途 | 数据示例 | 容量预估 |
|--------|------|----------|----------|
| PostgreSQL | 关系数据（地块、用户、配置） | 地块元数据、用户表 | <1GB |
| TimescaleDB | 时序数据（NDVI、气象） | 每日NDVI时序、气象数据 | 100GB/年 |
| MongoDB | 文档数据（报告、日志） | 生成的周报、预警记录 | 10GB/年 |
| MinIO | 对象存储（影像、图表） | 卫星影像、生成的图片 | 500GB/年 |

### 3.2 数据表设计

**plot_base（地块基础表）**：
```sql
CREATE TABLE plot_base (
    id SERIAL PRIMARY KEY,
    plot_id VARCHAR(50) UNIQUE NOT NULL,
    plot_name VARCHAR(100),
    area_mu DECIMAL(10,2),
    crop_type VARCHAR(20),
    variety VARCHAR(50),
    owner_name VARCHAR(50),
    owner_phone VARCHAR(20),
    geom GEOMETRY(Polygon, 4326),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**plot_ndvi_timeseries（NDVI时序表）**：
```sql
CREATE TABLE plot_ndvi_timeseries (
    id BIGSERIAL,
    plot_id VARCHAR(50) NOT NULL,
    observation_date DATE NOT NULL,
    ndvi_mean DECIMAL(5,4),
    ndvi_min DECIMAL(5,4),
    ndvi_max DECIMAL(5,4),
    cloud_coverage DECIMAL(5,2),
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(plot_id, observation_date)
);
SELECT create_hypertable('plot_ndvi_timeseries', 'observation_date');
```

**plot_yield_prediction（产量预测表）**：
```sql
CREATE TABLE plot_yield_prediction (
    id SERIAL PRIMARY KEY,
    plot_id VARCHAR(50) NOT NULL,
    prediction_date DATE NOT NULL,
    expected_harvest_date DATE,
    predicted_yield_kg_mu DECIMAL(10,2),
    confidence_level DECIMAL(5,2),
    growth_stage VARCHAR(20),
    risk_level INTEGER CHECK (risk_level BETWEEN 1 AND 4),
    PRIMARY KEY(plot_id, prediction_date)
);
```

---

## 四、分析模型设计

### 4.1 产量预测模型

**模型架构**：双阶段预测

**阶段一：特征提取**
- 输入：NDVI时序曲线 + 气象因子 + 地块基本信息
- 处理：滑动窗口提取时序特征（均值、斜率、峰值、谷值）
- 输出：特征向量

**阶段二：产量预测**
- 模型选择：
  - V1（简化版）：线性回归 / Ridge回归
  - V2（LSTM）：LSTM时序网络
- 输出：产量预测值 + 置信区间

**特征工程**：
| 特征类别 | 特征名 | 说明 |
|----------|--------|------|
| NDVI特征 | ndvi_mean_season | 生长季NDVI均值 |
| NDVI特征 | ndvi_peak_value | NDVI峰值 |
| NDVI特征 | ndvi_peak_date | 峰值出现日期 |
| NDVI特征 | ndvi_slope | NDVI上升斜率 |
| 气象特征 | cum_temp | 累计积温 |
| 气象特征 | cum_rainfall | 累计降雨 |
| 地块特征 | area_mu | 地块面积 |
| 地块特征 | variety_type | 品种类型(编码) |

### 4.2 病虫害识别模型

**识别策略**：基于NDVI时序突变检测

**检测算法**：
```
1. 计算NDVI时序的一阶差分
2. 设定突变阈值：|ΔNDVI| > 0.15 且 持续3天以上
3. 结合气象条件（高温高湿→稻瘟病高发）
4. 输出风险区域热力图
```

**常见病虫害特征**：
| 病虫害类型 | NDVI特征 | 气象条件 |
|------------|----------|----------|
| 稻瘟病 | NDVI快速下降 | 低温高湿 |
| 纹枯病 | NDVI局部突变 | 高温高湿 |
| 褐飞虱 | NDVI阶段性停滞 | 持续高温 |
| 纵卷叶螟 | NDVI纹理异常 | 晴朗高温 |

### 4.3 灾害评估模型

**受灾面积估算**：
```
受灾面积 = Σ(像素数 × 分辨率²) / 亩换算系数
损失程度 = (灾前NDVI - 灾后NDVI) / 灾前NDVI × 100%
```

**风险等级划分**：
| 风险等级 | NDVI变化 | 产量影响预估 | 预警动作 |
|----------|----------|--------------|----------|
| 1级（正常） | >-5% | <5% | 正常监控 |
| 2级（关注） | -5%~-15% | 5%-15% | 推送周报 |
| 3级（警告） | -15%~-30% | 15%-30% | 立即预警 |
| 4级（危险） | <-30% | >30% | 紧急预警+建议现场查勘 |

---

## 五、Agent工作流设计

### 5.1 Prefect工作流定义

```python
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

@flow(name="weekly-analysis-pipeline", schedule=IntervalSchedule(interval=timedelta(weeks=1)))
def weekly_pipeline():
    # 1. 数据采集
    plots = fetch_plot_list()
    for plot in plots:
        fetch_satellite_data.submit(plot)
        fetch_weather_data.submit(plot)

    # 2. 数据处理
    processed = process_data.map(plots)

    # 3. 分析推理
    predictions = predict_yield.map(processed)
    disease_risks = assess_disease.map(processed)

    # 4. 协作推送
    generate_weekly_report()
    check_and_push_alerts(predictions, disease_risks)
```

### 5.2 决策规则配置

```yaml
rules:
  disease_detection:
    ndvi_drop_threshold: 0.15
    consecutive_days: 3
    weather_condition:
      temperature_range: [25, 35]
      humidity_min: 80

  yield_warning:
    prediction_drop_threshold: 0.10
    risk_level_mapping:
      - {range: [0, 0.05], level: 1, action: "monitor"}
      - {range: [0.05, 0.15], level: 2, action: "weekly_report"}
      - {range: [0.15, 0.30], level: 3, action: "immediate_alert"}
      - {range: [0.30, 1.0], level: 4, action: "emergency"}
```

---

## 六、飞书集成方案

### 6.1 应用架构

```
飞书应用
├── 机器人能力（消息推送、对话交互）
├── 多维表格（数据存储、协作）
├── 文档能力（周报生成）
└── 审批流（保险理赔）
```

### 6.2 机器人消息卡片设计

**预警消息卡片**：
```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": "🌾 【风险预警】XX地块长势异常",
      "template": "red"
    },
    "elements": [
      {
        "tag": "markdown",
        "content": "**地块**：王大哥-示范田 (50.5亩)\n**当前风险等级**：🔴 3级警告"
      },
      {
        "tag": "img",
        "content": "https://your-server.com/maps/plot_001_risk.png"
      },
      {
        "tag": "column_set",
      },
      {
        "actions": [
          {"tag": "button", "text": "确认收到", "type": "primary"},
          {"tag": "button", "text": "申请现场查勘", "type": "default"}
        ]
      }
    ]
  }
}
```

### 6.3 多维表格字段配置

| 字段名 | 字段类型 | 填充方式 | 说明 |
|--------|----------|----------|------|
| 地块编号 | 文本 | 手动 | 唯一标识 |
| 地块名称 | 文本 | 手动 | 显示名称 |
| 面积（亩） | 数字 | 手动 | 种植面积 |
| 当前NDVI | 数字 | API同步 | 最新植被指数 |
| NDVI变化 | 数字 | API同步 | 环比变化 |
| 风险等级 | 单选 | API同步 | 1-4级 |
| 预测产量(斤/亩) | 数字 | API同步 | 产量预测 |
| 气象状况 | 文本 | API同步 | 简要气象 |
| 最后更新 | 日期 | 自动 | 更新时间 |
| 操作 | 按钮 | - | 查看详情 |

### 6.4 API调用限制应对

| 限制项 | 限制值 | 应对策略 |
|--------|--------|----------|
| 机器人消息 | 100次/分钟/应用 | 批量聚合 + 消息队列 |
| 多维表格写 | 100次/分钟/应用 | 定时批量写入 |
| 文档创建 | 20次/分钟/应用 | 缓存+异步写入 |

---

## 七、部署架构

### 7.1 Docker Compose 部署

```yaml
version: '3.8'

services:
  api-gateway:
    build: ./docker/nginx
    ports:
      - "80:80"
    depends_on:
      - web-backend
      - data-agent
      - analysis-agent

  web-backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/tianyan
    depends_on:
      - db
      - timeseries-db

  data-agent:
    build: ./agents/data-agent
    environment:
      - PREFECT_API_URL=http://prefect:4200/api
    volumes:
      - ./data:/app/data

  analysis-agent:
    build: ./agents/analysis-agent
    environment:
      - PYTHONPATH=/app

  prefect:
    image: prefect/prefect:2.x
    ports:
      - "4200:4200"

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=tianyan
    volumes:
      - postgres_data:/var/lib/postgresql/data

  timeseries-db:
    image: timescale/timescaledb:latest-pg15
    environment:
      - POSTGRES_DB=tianyan
    volumes:
      - timeseries_data:/var/lib/postgresql/data

  mongodb:
    image: mongo:6
    volumes:
      - mongo_data:/data/db

  minio:
    image: minio/minio
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data

volumes:
  postgres_data:
  timeseries_data:
  mongo_data:
  minio_data:
```

### 7.2 服务器资源要求

| 环境 | 规格 | 说明 |
|------|------|------|
| 开发环境 | 2核4G | 单机部署 |
| 测试环境 | 4核8G | 单机部署 |
| 生产环境 | 8核16G | 推荐云服务器 |

---

## 八、API接口设计

### 8.1 核心接口列表

| 接口路径 | 方法 | 说明 | 认证 |
|----------|------|------|------|
| `/api/v1/plots` | GET | 获取地块列表 | 需认证 |
| `/api/v1/plots/{id}` | GET | 获取地块详情 | 需认证 |
| `/api/v1/plots/{id}/ndvi` | GET | 获取NDVI时序 | 需认证 |
| `/api/v1/plots/{id}/prediction` | GET | 获取产量预测 | 需认证 |
| `/api/v1/plots/{id}/risk` | GET | 获取风险评估 | 需认证 |
| `/api/v1/alerts` | GET | 获取预警列表 | 需认证 |
| `/api/v1/reports/weekly` | POST | 手动触发周报 | 需认证 |
| `/health` | GET | 健康检查 | 无需认证 |

### 8.2 响应示例

**产量预测响应**：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "plot_id": "PLOT_001",
    "plot_name": "王大哥-示范田",
    "prediction_date": "2026-04-17",
    "expected_harvest_date": "2026-09-15",
    "predicted_yield_kg_mu": 620.5,
    "confidence_interval": {
      "lower": 550.0,
      "upper": 690.0
    },
    "risk_level": 2,
    "risk_factors": ["近期降水偏少", "NDVI略低于去年同期"]
  }
}
```

---

## 九、安全方案

### 9.1 认证授权

| 组件 | 方案 | 说明 |
|------|------|------|
| API认证 | JWT Token | 飞书OAuth2.0获取 |
| 权限控制 | RBAC | 角色：管理员/农技员/保险员/农户 |
| 数据隔离 | 地块级 | 用户只能查看授权地块 |

### 9.2 数据安全

- 敏感数据（农户电话等）加密存储
- 影像数据定期备份（MinIO跨区域复制）
- 数据库定期全量备份
- 传输全程HTTPS

---

## 十、监控与运维

### 10.1 监控指标

| 类别 | 指标 | 告警阈值 |
|------|------|----------|
| 系统 | CPU > 80% | 持续5分钟 |
| 系统 | 内存 > 85% | 持续5分钟 |
| 应用 | 接口错误率 > 1% | 立即告警 |
| 数据 | 数据更新延迟 > 24h | 每日检查 |
| 任务 | Prefect任务失败 | 立即告警 |

### 10.2 日志方案

- 结构化日志（JSON格式）
- 集中收集（ELK或 Loki）
- 保留周期：30天

---

*文档版本：v1.0*
*最后更新：2026-04-17*
