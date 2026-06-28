#!/usr/bin/env python3
"""
Q1: 三个餐段（早餐/午餐/晚餐）各有多少订单？哪个餐段最忙？
解题方法: groupby + size
"""

import pandas as pd

print("\n" + "="*80)
print("Q1: 三个餐段（早餐/午餐/晚餐）各有多少订单？哪个餐段最忙？")
print("="*80)

# 读取CSV文件
orders = pd.read_csv('data/csv/orders.csv', encoding='utf-8-sig')

print("\n📖 数据预览:")
print(orders.head())
print(f"\n表格信息: {orders.shape[0]}行 {orders.shape[1]}列")

# 代码实现
print("\n" + "="*80)
print("💡 解题代码:")
print("="*80)
code = """
q1_result = orders.groupby('meal_period').size().sort_values(ascending=False)
print(q1_result)
"""
print(code)

# 执行代码
q1_result = orders.groupby('meal_period').size().sort_values(ascending=False)

print("\n" + "="*80)
print("📊 执行结果:")
print("="*80)
print("\n各餐段的订单数:")
print(q1_result)

print("\n" + "-"*80)
print("详细统计:")
print("-"*80)
for meal, count in q1_result.items():
    percentage = (count / q1_result.sum()) * 100
    bar = "▓" * int(percentage / 2.5)
    print(f"  {meal:6s} │ {bar:<40} │ {count:4d}个 ({percentage:5.1f}%)")

print("\n" + "-"*80)
print("关键指标:")
print("-"*80)
print(f"✓ 订单总数:       {q1_result.sum()}")
print(f"✓ 最忙的餐段:     {q1_result.idxmax()}")
print(f"✓ 最忙餐段订单数: {q1_result.max()}")
print(f"✓ 占比:          {(q1_result.max() / q1_result.sum() * 100):.1f}%")

print("\n" + "="*80)
print("🎯 一句话结论:")
print("="*80)
conclusion = f"{q1_result.idxmax()}是最忙的餐段，共有{q1_result.max()}个订单，占总订单数的{(q1_result.max() / q1_result.sum() * 100):.1f}%。"
print(f"\n{conclusion}\n")
print("="*80 + "\n")
