#!/usr/bin/env python3
"""
Q4: 销量最高的5道菜是哪些？（要显示菜名，不是dish_id）
解题方法: groupby + merge + sort + head(5)
"""

import pandas as pd

print("\n" + "="*80)
print("Q4: 销量最高的5道菜是哪些？（要显示菜名，不是dish_id）")
print("="*80)

# 读取CSV文件
order_items = pd.read_csv('data/csv/order_items.csv', encoding='utf-8-sig')
dishes = pd.read_csv('data/csv/dishes.csv', encoding='utf-8-sig')

print("\n📖 数据预览:")
print("order_items:")
print(order_items.head())
print("\ndishes:")
print(dishes.head())

# 代码实现
print("\n" + "="*80)
print("💡 解题代码:")
print("="*80)
code = """
# 步骤1: 按dish_id分组统计销量
sales_by_dish = order_items.groupby('dish_id')['quantity'].sum().reset_index()
sales_by_dish.columns = ['dish_id', 'total_quantity']

# 步骤2: 与dishes表merge获取菜名和价格
q4_result = sales_by_dish.merge(dishes[['id', 'name', 'price']], 
                                 left_on='dish_id', right_on='id')

# 步骤3: 计算营业额
q4_result['revenue'] = q4_result['total_quantity'] * q4_result['price']

# 步骤4: 按销量降序排序，取前5
q4_result = q4_result[['name', 'total_quantity', 'price', 'revenue']].sort_values('total_quantity', ascending=False).head(5)
print(q4_result)
"""
print(code)

# 执行代码
sales_by_dish = order_items.groupby('dish_id')['quantity'].sum().reset_index()
sales_by_dish.columns = ['dish_id', 'total_quantity']
q4_result = sales_by_dish.merge(dishes[['id', 'name', 'price']], 
                                 left_on='dish_id', right_on='id')
q4_result['revenue'] = q4_result['total_quantity'] * q4_result['price']
q4_result = q4_result[['name', 'total_quantity', 'price', 'revenue']].sort_values('total_quantity', ascending=False).head(5)

print("\n" + "="*80)
print("📊 执行结果:")
print("="*80)
print("\n销量前5的菜品:")
print()
for idx, (i, row) in enumerate(q4_result.iterrows(), 1):
    print(f"  {'🥇🥈🥉🏅🎖️'[idx-1]} 第{idx}名: {row['name']:15s} | 销量: {int(row['total_quantity']):4d}份 | 单价: ¥{row['price']:6.2f} | 营业额: ¥{row['revenue']:8.2f}")

print("\n" + "-"*80)
print("关键指标:")
print("-"*80)
print(f"✓ 销量冠军:        {q4_result.iloc[0]['name']}")
print(f"✓ 冠军销量:        {int(q4_result.iloc[0]['total_quantity'])}份")
print(f"✓ 冠军单价:        ¥{q4_result.iloc[0]['price']:.2f}")
print(f"✓ 冠军营业额:      ¥{q4_result.iloc[0]['revenue']:,.2f}")
print(f"✓ 前5名总销量:     {int(q4_result['total_quantity'].sum())}份")
print(f"✓ 前5名总营业额:   ¥{q4_result['revenue'].sum():,.2f}")

print("\n" + "="*80)
print("🎯 一句话结论:")
print("="*80)
conclusion = f"销量冠军是{q4_result.iloc[0]['name']}，共销售{int(q4_result.iloc[0]['total_quantity'])}份，营业额为¥{q4_result.iloc[0]['revenue']:,.2f}。"
print(f"\n{conclusion}\n")
print("="*80 + "\n")
