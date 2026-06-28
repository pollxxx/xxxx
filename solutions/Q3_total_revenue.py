#!/usr/bin/env python3
"""
Q3: 这批数据的总营业额是多少？
解题方法: 创建新列 amount = quantity * unit_price，然后sum()
"""

import pandas as pd

print("\n" + "="*80)
print("Q3: 这批数据的总营业额是多少？")
print("="*80)

# 读取CSV文件
order_items = pd.read_csv('data/csv/order_items.csv', encoding='utf-8-sig')
orders = pd.read_csv('data/csv/orders.csv', encoding='utf-8-sig')

print("\n📖 数据预览:")
print(order_items.head())
print(f"\n表格信息: {order_items.shape[0]}行 {order_items.shape[1]}列")

# 代码实现
print("\n" + "="*80)
print("💡 解题代码:")
print("="*80)
code = """
order_items['amount'] = order_items['quantity'] * order_items['unit_price']
total_revenue = order_items['amount'].sum()
print(f"总营业额: ¥{total_revenue:,.2f}")
"""
print(code)

# 执行代码
order_items['amount'] = order_items['quantity'] * order_items['unit_price']
total_revenue = order_items['amount'].sum()

print("\n" + "="*80)
print("📊 执行结果:")
print("="*80)

print(f"\n总营业额: ¥{total_revenue:,.2f}")

print("\n" + "-"*80)
print("详细统计:")
print("-"*80)
print(f"✓ 总营业额:        ¥{total_revenue:,.2f}")
print(f"✓ 订单总数:        {orders.shape[0]}")
print(f"✓ 平均订单金额:    ¥{total_revenue / orders.shape[0]:,.2f}")
print(f"✓ 项目总数:        {order_items.shape[0]}")
print(f"✓ 平均项目金额:    ¥{order_items['amount'].mean():,.2f}")
print(f"✓ 项目金额中位数:  ¥{order_items['amount'].median():,.2f}")
print(f"✓ 项目金额标准差:  ¥{order_items['amount'].std():,.2f}")
print(f"✓ 最高单项金额:    ¥{order_items['amount'].max():,.2f}")
print(f"✓ 最低单项金额:    ¥{order_items['amount'].min():,.2f}")

# 按餐段统计
print("\n" + "-"*80)
print("按餐段统计营业额:")
print("-"*80)
merged = orders.merge(order_items, left_on='id', right_on='order_id')
revenue_by_meal = merged.groupby('meal_period')['amount'].sum().sort_values(ascending=False)
for meal, rev in revenue_by_meal.items():
    percentage = (rev / total_revenue) * 100
    print(f"  {meal:6s}: ¥{rev:>10,.2f} ({percentage:5.1f}%)")

print("\n" + "="*80)
print("🎯 一句话结论:")
print("="*80)
conclusion = f"这批数据的总营业额为¥{total_revenue:,.2f}，平均每个订单的金额约为¥{total_revenue / orders.shape[0]:,.2f}。"
print(f"\n{conclusion}\n")
print("="*80 + "\n")
