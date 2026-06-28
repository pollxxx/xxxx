#!/usr/bin/env python3
"""
运行所有Q1-Q6分析
"""

import subprocess
import sys

scripts = [
    ('Q1', 'Q1_meal_periods.py'),
    ('Q2', 'Q2_waste_reasons.py'),
    ('Q3', 'Q3_total_revenue.py'),
    ('Q4', 'Q4_top_dishes.py'),
    ('Q5', 'Q5_stall_ranking.py'),
    ('Q6', 'Q6_deep_analysis.py'),
]

print("\n" + "#"*80)
print("#" + " "*78 + "#")
print("#" + "  校园食堂数据分析 - 完整分析报告".center(78) + "#")
print("#" + " "*78 + "#")
print("#"*80)

for name, script in scripts:
    print(f"\n\n⏰ 正在运行 {name}...")
    print("-"*80)
    try:
        subprocess.run([sys.executable, script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ {name} 执行失败: {e}")
        sys.exit(1)

print("\n" + "#"*80)
print("#" + " "*78 + "#")
print("#" + "  ✅ 所有分析完成！".center(78) + "#")
print("#" + " "*78 + "#")
print("#"*80 + "\n")
