#!/usr/bin/env python3
"""
Q2: 5种浪费原因各出现多少次？哪种原因最多？
解题方法: value_counts()
"""

import pandas as pd

print("\n" + "="*80)
print("Q2: 5种浪费原因各出现多少次？哪种原因最多？")
print("="*80)

# 读取CSV文件
waste = pd.read_csv('data/csv/waste_records.csv', encoding='utf-8-sig')

print("\n📖 数据预览:")
print(waste.head())
print(f"\n表格信息: {waste.shape[0]}行 {waste.shape[1]}列")

# 代码实现
print("\n" + "="*80)
print("💡 解题代码:")
print("="*80)
code = """
q2_result = waste['reason'].value_counts()
print(q2_result)
"""
print(code)

# 执行代码
q2_result = waste['reason'].value_counts()

print("\n" + "="*80)
print("📊 执行结果:")
print("="*80)
print("\n5种浪费原因的次数统计:")
print(q2_result)

print("\n" + "-"*80)
print("详细统计:")
print("-"*80)
for reason, count in q2_result.items():
    percentage = (count / q2_result.sum()) * 100
    bar = "▓" * int(percentage / 2.5)
    print(f"  {reason:10s} │ {bar:<40} │ {count:3d}次 ({percentage:5.1f}%)")

print("\n" + "-"*80)
print("关键指标:")
print("-"*80)
print(f"✓ 浪费记录总数:  {q2_result.sum()}")
print(f"✓ 最常见原因:    {q2_result.idxmax()}")
print(f"✓ 发生次数:      {q2_result.max()}")
print(f"✓ 占比:         {(q2_result.max() / q2_result.sum() * 100):.1f}%")

print("\n" + "="*80)
print("🎯 一句话结论:")
print("="*80)
conclusion = f"{q2_result.idxmax()}是最常见的浪费原因，共发生{q2_result.max()}次，占浪费原因总数的{(q2_result.max() / q2_result.sum() * 100):.1f}%。"
print(f"\n{conclusion}\n")
print("="*80 + "\n")
