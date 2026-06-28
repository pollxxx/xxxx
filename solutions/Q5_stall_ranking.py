#!/usr/bin/env python3
"""
Q5: 各档口的营业额排名（从高到低）
解题方法: merge + groupby + merge + sort
"""

import pandas as pd

print("\n" + "="*80)
print("Q5: 各档口的营业额排名（从高到低）")
print("="*80)

# 读取CSV文件
order_items = pd.read_csv('data/csv/order_items.csv', encoding='utf-8-sig')
dishes = pd.read_csv('data/csv/dishes.csv', encoding='utf-8-sig')
stalls = pd.read_csv('data/csv/stalls.csv', encoding='utf-8-sig')

print("\n📖 数据预览:")
print("stalls:")
print(stalls)
print("\ndishes (头10行):")
print(dishes.head(10))

# 代码实现
print("\n" + "="*80)
print("💡 解题代码:")
print("="*80)
code = """
# 步骤1: 创建amount列
order_items['amount'] = order_items['quantity'] * order_items['unit_price']

# 步骤2: order_items与dishes merge获取stall_id
merged_for_stall = order_items.merge(dishes[['id', 'stall_id']], 
                                      left_on='dish_id', right_on='id')

# 步骤3: 按stall_id汇总营业额
stall_revenue = merged_for_stall.groupby('stall_id')['amount'].sum().reset_index()
stall_revenue.columns = ['id', 'revenue']

# 步骤4: 与stalls表merge获取档口名和位置
q5_result = stall_revenue.merge(stalls[['id', 'name', 'location']], on='id')

# 步骤5: 按营业额降序排序
q5_result = q5_result.sort_values('revenue', ascending=False)
print(q5_result)
"""
print(code)

# 执行代码
order_items['amount'] = order_items['quantity'] * order_items['unit_price']
merged_for_stall = order_items.merge(dishes[['id', 'stall_id']], 
                                      left_on='dish_id', right_on='id')
stall_revenue = merged_for_stall.groupby('stall_id')['amount'].sum().reset_index()
stall_revenue.columns = ['id', 'revenue']
q5_result = stall_revenue.merge(stalls[['id', 'name', 'location']], on='id')
q5_result = q5_result.sort_values('revenue', ascending=False).reset_index(drop=True)

print("\n" + "="*80)
print("📊 执行结果:")
print("="*80)
print("\n各档口营业额排名:")
print()
for idx, (i, row) in enumerate(q5_result.iterrows(), 1):
    bar = "▓" * int(row['revenue'] / 1000)
    print(f"  {idx}. {row['name']:12s} │ {bar:<40} │ ¥{row['revenue']:>10,.2f} │ {row['location']}")

print("\n" + "-"*80)
print("关键指标:")
print("-"*80)
print(f"✓ 档口总数:        {len(q5_result)}")
print(f"✓ 营业额最高:      {q5_result.iloc[0]['name']}")
print(f"✓ 最高营业额:      ¥{q5_result.iloc[0]['revenue']:,.2f}")
print(f"✓ 营业额最低:      {q5_result.iloc[-1]['name']}")
print(f"✓ 最低营业额:      ¥{q5_result.iloc[-1]['revenue']:,.2f}")
print(f"✓ 平均营业额:      ¥{q5_result['revenue'].mean():,.2f}")
print(f"✓ 总营业额:        ¥{q5_result['revenue'].sum():,.2f}")

print("\n" + "="*80)
print("🎯 一句话结论:")
print("="*80)
ranking = ' > '.join([row['name'] for _, row in q5_result.iterrows()])
conclusion = f"{q5_result.iloc[0]['name']}营业额最高（¥{q5_result.iloc[0]['revenue']:,.2f}），整体排名为: {ranking}。"
print(f"\n{conclusion}\n")
print("="*80 + "\n")
