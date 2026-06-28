# 校园食堂数据分析项目

## 📁 项目目录结构

```
campus-canteen-analysis/
│
├── README.md                          # 项目说明文档
├── data/
│   └── csv/                           # 数据文件目录
│       ├── stalls.csv                 # 档口信息表（6个档口）
│       ├── dishes.csv                 # 菜品信息表（30道菜）
│       ├── orders.csv                 # 订单表（1200个订单）
│       ├── order_items.csv            # 订单项目表（2500行）
│       └── waste_records.csv          # 浪费记录表（500行）
│
├── solutions/
│   ├── 01_basic_analysis.py           # Q1-Q5 基础分析（必做，30分）
│   ├── 02_advanced_analysis.py        # Q6 进阶分析（选做，发挥分）
│   ├── utils.py                       # 辅助函数
│   └── output/                        # 输出结果目录
│       ├── Q1_meal_periods.png
│       ├── Q2_waste_reasons.png
│       ├── Q3_revenue.txt
│       ├── Q4_top_dishes.png
│       ├── Q5_stall_ranking.png
│       └── Q6_deep_insights.png
│
├── analysis_report.md                 # 完整分析报告
└── requirements.txt                   # 项目依赖
```

## 📊 数据集简介

### 表结构设计

**stalls（档口表）**
- id: 档口ID（1-6）
- name: 档口名称
- location: 位置

**dishes（菜品表）**
- id: 菜品ID（1-30）
- stall_id: 所属档口
- name: 菜品名称
- category: 分类（主食/热菜/套餐/小吃/汤羹）
- price: 价格
- portion_weight_g: 份量（克）

**orders（订单表）**
- id: 订单ID（1-1200）
- ordered_at: 下单时间
- meal_period: 餐段（早餐/午餐/晚餐）

**order_items（订单项目表）**
- id: 项目ID
- order_id: 订单ID
- dish_id: 菜品ID
- quantity: 数量（1-3）
- unit_price: 单价

**waste_records（浪费记录表）**
- id: 记录ID
- dish_id: 菜品ID
- recorded_date: 记录日期
- waste_weight_g: 浪费量
- reason: 原因（备餐过量/制作失败/售后退回/临期报废/其他）

## 🎯 解题要求

### 第一部分：基础数据分析（必做，共30分）

| 题号 | 内容 | 分值 | 提交内容 |
|------|------|------|---------|
| Q1 | 三个餐段的订单数（热身） | 5分 | 代码 + 截图 + 结论 |
| Q2 | 5种浪费原因的次数（热身） | 5分 | 代码 + 截图 + 结论 |
| Q3 | 总营业额 | 5分 | 代码 + 截图 + 结论 |
| Q4 | 销量前5的菜名及销量 | 7分 | 代码 + 截图 + 结论 |
| Q5 | 各档口营业额排名 | 8分 | 代码 + 截图 + 结论 |

### 第二部分：进阶分析（选做，计入表达分）

| 题号 | 内容 | 分值 |
|------|------|------|
| Q6 | 自主挖掘结论并画图 | 加分 |

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行基础分析
python solutions/01_basic_analysis.py

# 3. 运行进阶分析
python solutions/02_advanced_analysis.py

# 4. 查看输出结果
# 生成的图表和结论保存在 solutions/output/ 目录
```

## 💡 解题思路提示

### Q1：三个餐段的订单数
- 使用 `groupby('meal_period').size()`
- 只需操作 `orders` 表

### Q2：5种浪费原因的次数
- 使用 `value_counts()` 
- 只需操作 `waste_records` 表

### Q3：总营业额
- 创建新列：`amount = quantity * unit_price`
- 对 `amount` 列求和

### Q4：销量前5的菜
- 按 `dish_id` 聚合 `quantity`
- 与 `dishes` 表进行 merge 获取菜名
- 排序并取前5

### Q5：各档口营业额排名
- `order_items` merge `dishes` 获取 `stall_id`
- 按 `stall_id` 汇总营业额
- 与 `stalls` 表 merge 获取档口名
- 按营业额排序

### Q6：自主探索
- 可以从以下角度切入：
  - 哪道菜"销得多但浪费也多"？
  - 早/午/晚餐的菜品偏好差异？
  - 浪费原因与菜品分类的关系？
  - 档口间的竞争力对比？

## 📝 注意事项

⚠️ **重要提示：**
1. CSV带BOM，使用 `encoding='utf-8-sig'`
2. 一张订单可能有多行（多道菜），统计订单数时不能直接数 `order_items` 行数
3. 使用 `merge` 时要注意左右表的匹配键
4. 截图需要标注题号（如"图1-1 / Q1"）

## 📚 相关资源

- Pandas文档: https://pandas.pydata.org/
- Matplotlib绘图: https://matplotlib.org/
- Seaborn美化: https://seaborn.pydata.org/

---

**作者**: pollxxx  
**创建日期**: 2026-06-28  
**最后更新**: 2026-06-28
