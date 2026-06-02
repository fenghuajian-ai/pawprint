# 跨境电商 AI 全流程自动化管线

## 一句话说清楚
> 输入一个品类名称，自动跑完：市场扫描 → 竞品分析 → Listing 生成 → 质量审核 → 竞品监控部署。全程 AI 驱动 + 人工关键节点把关。

## 四个阶段

```
[选品扫描] → [竞品拆解] → [Listing生成+审核] → [监控部署]
   API             爬虫              AI API              定时任务
```

| 阶段 | 做什么 | 实际生产用什么 | 时间 |
|------|--------|---------------|------|
| 1 | 市场规模、价格带、机会区间 | Keepa API / Jungle Scout | 2 min |
| 2 | 竞品数据 + 差评痛点归类 | Playwright + AI 分类 | 10 min |
| 3 | 标题/五点生成 + 合规审核 | Claude API + 人工 checklist | 10 min |
| 4 | 每日监控 + 异常告警部署 | Python 定时任务 + 飞书推送 | 5 min |

## 怎么跑

```bash
python auto_pipeline.py --product "蓝牙耳机" --market "US"
```

替换品类和站点就能复用到任何产品线：
```bash
python auto_pipeline.py --product "宠物饮水机" --market "US"
python auto_pipeline.py --product "瑜伽裤" --market "DE"
```

## 效率对比

| 环节 | 传统方式 | AI 管线 | 提升 |
|------|---------|--------|------|
| 市场扫描 | 手动翻报告 2h | API 自动 + AI 摘要 2min | 60x |
| 竞品差评分析 | 人工看 500 条评论 3h | AI 批量分类 10min | 18x |
| Listing 生成 + 审核 | 手写+来回改 2h | AI 生成 + checklist 审核 10min | 12x |
| 监控部署 | 每天手动查 1h/天 | 脚本自动+异常告警 0min | ∞ |

## 人工把关节点

自动化不是放手不管。以下环节必须人工确认：
1. 数据来源核实（AI 可能编数字）
2. FTC/平台合规审查（AI 不知道法律红线）
3. 文化敏感性检查（AI 默认西方视角）
4. 最终 Listing 终审批复
