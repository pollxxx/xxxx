"""
校园食堂数据分析系统 - Flask Web应用
主程序入口
"""

from flask import Flask, render_template, jsonify, request
import pandas as pd
import json
from pathlib import Path
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['JSON_AS_ASCII'] = False

# ============================================================================
# 数据加载
# ============================================================================

def load_data():
    """加载所有数据"""
    try:
        data = {
            'stalls': pd.read_csv('data/csv/stalls.csv', encoding='utf-8-sig'),
            'dishes': pd.read_csv('data/csv/dishes.csv', encoding='utf-8-sig'),
            'orders': pd.read_csv('data/csv/orders.csv', encoding='utf-8-sig'),
            'order_items': pd.read_csv('data/csv/order_items.csv', encoding='utf-8-sig'),
            'waste': pd.read_csv('data/csv/waste_records.csv', encoding='utf-8-sig'),
        }
        return data
    except Exception as e:
        print(f"数据加载失败: {e}")
        return None

# 全局数据加载
DATA = load_data()

# ============================================================================
# Q1: 三个餐段的订单数
# ============================================================================

@app.route('/api/q1', methods=['GET'])
def get_q1():
    """Q1: 三个餐段的订单数"""
    if DATA is None:
        return jsonify({'error': '数据加载失败'}), 500
    
    orders = DATA['orders']
    q1_result = orders.groupby('meal_period').size().sort_values(ascending=False)
    
    return jsonify({
        'title': 'Q1: 三个餐段的订单数',
        'data': {
            '早餐': int(q1_result.get('早餐', 0)),
            '午餐': int(q1_result.get('午餐', 0)),
            '晚餐': int(q1_result.get('晚餐', 0)),
        },
        'total': int(q1_result.sum()),
        'busiest': q1_result.idxmax(),
        'busiest_count': int(q1_result.max()),
        'busiest_percentage': round(q1_result.max() / q1_result.sum() * 100, 1),
        'conclusion': f"{q1_result.idxmax()}是最忙的餐段，共有{q1_result.max()}个订单，占比{round(q1_result.max() / q1_result.sum() * 100, 1)}%。"
    })

# ============================================================================
# Q2: 5种浪费原因的次数
# ============================================================================

@app.route('/api/q2', methods=['GET'])
def get_q2():
    """Q2: 5种浪费原因的次数"""
    if DATA is None:
        return jsonify({'error': '数据加载失败'}), 500
    
    waste = DATA['waste']
    q2_result = waste['reason'].value_counts()
    
    return jsonify({
        'title': 'Q2: 5种浪费原因的次数',
        'data': q2_result.to_dict(),
        'total': int(q2_result.sum()),
        'most_common': q2_result.idxmax(),
        'most_common_count': int(q2_result.max()),
        'most_common_percentage': round(q2_result.max() / q2_result.sum() * 100, 1),
        'conclusion': f"{q2_result.idxmax()}是最常见的浪费原因，共发生{q2_result.max()}次，占浪费原因总数的{round(q2_result.max() / q2_result.sum() * 100, 1)}%。"
    })

# ============================================================================
# Q3: 总营业额
# ============================================================================

@app.route('/api/q3', methods=['GET'])
def get_q3():
    """Q3: 总营业额"""
    if DATA is None:
        return jsonify({'error': '数据加载失败'}), 500
    
    order_items = DATA['order_items']
    orders = DATA['orders']
    
    order_items['amount'] = order_items['quantity'] * order_items['unit_price']
    total_revenue = order_items['amount'].sum()
    
    # 按餐段统计营业额
    merged = orders.merge(order_items, left_on='id', right_on='order_id')
    revenue_by_meal = merged.groupby('meal_period')['amount'].sum()
    
    return jsonify({
        'title': 'Q3: 总营业额',
        'total_revenue': round(total_revenue, 2),
        'avg_order_revenue': round(total_revenue / orders.shape[0], 2),
        'avg_item_revenue': round(order_items['amount'].mean(), 2),
        'median_revenue': round(order_items['amount'].median(), 2),
        'max_revenue': round(order_items['amount'].max(), 2),
        'min_revenue': round(order_items['amount'].min(), 2),
        'revenue_by_meal': {
            '早餐': round(revenue_by_meal.get('早餐', 0), 2),
            '午餐': round(revenue_by_meal.get('午餐', 0), 2),
            '晚餐': round(revenue_by_meal.get('晚餐', 0), 2),
        },
        'conclusion': f"这批数据的总营业额为¥{total_revenue:,.2f}，平均每个订单的金额约为¥{total_revenue / orders.shape[0]:.2f}。"
    })

# ============================================================================
# Q4: 销量前5的菜
# ============================================================================

@app.route('/api/q4', methods=['GET'])
def get_q4():
    """Q4: 销量前5的菜"""
    if DATA is None:
        return jsonify({'error': '数据加载失败'}), 500
    
    order_items = DATA['order_items']
    dishes = DATA['dishes']
    
    sales_by_dish = order_items.groupby('dish_id')['quantity'].sum().reset_index()
    sales_by_dish.columns = ['dish_id', 'total_quantity']
    q4_result = sales_by_dish.merge(dishes[['id', 'name', 'price']], 
                                     left_on='dish_id', right_on='id')
    q4_result = q4_result[['name', 'total_quantity', 'price']].sort_values('total_quantity', ascending=False).head(5)
    q4_result['revenue'] = q4_result['total_quantity'] * q4_result['price']
    
    data_list = []
    for idx, row in q4_result.iterrows():
        data_list.append({
            'rank': len(data_list) + 1,
            'name': row['name'],
            'quantity': int(row['total_quantity']),
            'price': round(row['price'], 2),
            'revenue': round(row['revenue'], 2)
        })
    
    return jsonify({
        'title': 'Q4: 销量前5的菜品',
        'data': data_list,
        'top_dish': q4_result.iloc[0]['name'],
        'top_quantity': int(q4_result.iloc[0]['total_quantity']),
        'top_revenue': round(q4_result.iloc[0]['revenue'], 2),
        'conclusion': f"销量冠军是{q4_result.iloc[0]['name']}，共销售{int(q4_result.iloc[0]['total_quantity'])}份，营业额为¥{q4_result.iloc[0]['revenue']:,.2f}。"
    })

# ============================================================================
# Q5: 各档口营业额排名
# ============================================================================

@app.route('/api/q5', methods=['GET'])
def get_q5():
    """Q5: 各档口营业额排名"""
    if DATA is None:
        return jsonify({'error': '数据加载失败'}), 500
    
    order_items = DATA['order_items']
    dishes = DATA['dishes']
    stalls = DATA['stalls']
    
    merged_for_stall = order_items.merge(dishes[['id', 'stall_id']], 
                                          left_on='dish_id', right_on='id')
    merged_for_stall['amount'] = merged_for_stall['quantity'] * merged_for_stall['unit_price']
    stall_revenue = merged_for_stall.groupby('stall_id')['amount'].sum().reset_index()
    stall_revenue.columns = ['id', 'revenue']
    q5_result = stall_revenue.merge(stalls[['id', 'name', 'location']], on='id').sort_values('revenue', ascending=False)
    q5_result = q5_result[['name', 'location', 'revenue']].reset_index(drop=True)
    
    data_list = []
    for idx, row in q5_result.iterrows():
        data_list.append({
            'rank': idx + 1,
            'name': row['name'],
            'location': row['location'],
            'revenue': round(row['revenue'], 2)
        })
    
    return jsonify({
        'title': 'Q5: 各档口营业额排名',
        'data': data_list,
        'top_stall': q5_result.iloc[0]['name'],
        'top_revenue': round(q5_result.iloc[0]['revenue'], 2),
        'avg_revenue': round(q5_result['revenue'].mean(), 2),
        'conclusion': f"{q5_result.iloc[0]['name']}营业额最高，为¥{q5_result.iloc[0]['revenue']:,.2f}。"
    })

# ============================================================================
# Q6: 深度分析
# ============================================================================

@app.route('/api/q6', methods=['GET'])
def get_q6():
    """Q6: 深度分析"""
    if DATA is None:
        return jsonify({'error': '数据加载失败'}), 500
    
    order_items = DATA['order_items']
    dishes = DATA['dishes']
    orders = DATA['orders']
    waste = DATA['waste']
    
    # 分析1: 销量vs浪费
    order_items['amount'] = order_items['quantity'] * order_items['unit_price']
    sales = order_items.groupby('dish_id')['quantity'].sum()
    waste_by_dish = waste.groupby('dish_id')['waste_weight_g'].sum()
    revenue_by_dish = order_items.groupby('dish_id')['amount'].sum()
    
    analysis = pd.DataFrame({
        'sales': sales,
        'waste': waste_by_dish,
        'revenue': revenue_by_dish
    }).fillna(0).reset_index()
    
    analysis = analysis.merge(dishes[['id', 'name']], left_on='dish_id', right_on='id')
    analysis['waste_ratio'] = analysis['waste'] / (analysis['sales'] + 0.1)
    
    # 分析2: 餐段偏好
    order_with_meal = orders.merge(order_items, left_on='id', right_on='order_id')
    order_with_meal = order_with_meal.merge(dishes[['id', 'name']], 
                                             left_on='dish_id', right_on='id')
    
    meal_stats = order_with_meal.groupby('meal_period')['amount'].agg(['sum', 'count', 'mean'])
    
    # 分析3: 浪费原因统计
    waste_stats = waste['reason'].value_counts()
    
    return jsonify({
        'title': 'Q6: 深度分析与有趣发现',
        'analysis1': {
            'title': '销量 vs 浪费分析',
            'max_waste_dish': analysis.loc[analysis['waste'].idxmax(), 'name'],
            'max_waste': round(analysis['waste'].max(), 0),
            'max_sales_dish': analysis.loc[analysis['sales'].idxmax(), 'name'],
            'max_sales': int(analysis['sales'].max()),
            'avg_waste_per_unit': round(analysis['waste'].sum() / analysis['sales'].sum(), 2)
        },
        'analysis2': {
            'title': '餐段营业额对比',
            '早餐': {
                'revenue': round(meal_stats.loc['早餐', 'sum'] if '早餐' in meal_stats.index else 0, 2),
                'count': int(meal_stats.loc['早餐', 'count'] if '早餐' in meal_stats.index else 0),
                'avg': round(meal_stats.loc['早餐', 'mean'] if '早餐' in meal_stats.index else 0, 2)
            },
            '午餐': {
                'revenue': round(meal_stats.loc['午餐', 'sum'] if '午餐' in meal_stats.index else 0, 2),
                'count': int(meal_stats.loc['午餐', 'count'] if '午餐' in meal_stats.index else 0),
                'avg': round(meal_stats.loc['午餐', 'mean'] if '午餐' in meal_stats.index else 0, 2)
            },
            '晚餐': {
                'revenue': round(meal_stats.loc['晚餐', 'sum'] if '晚餐' in meal_stats.index else 0, 2),
                'count': int(meal_stats.loc['晚餐', 'count'] if '晚餐' in meal_stats.index else 0),
                'avg': round(meal_stats.loc['晚餐', 'mean'] if '晚餐' in meal_stats.index else 0, 2)
            }
        },
        'analysis3': {
            'title': '浪费原因分布',
            'reasons': waste_stats.to_dict()
        },
        'conclusion': '深度分析发现了多个有趣的规律，详见各分析板块。'
    })

# ============================================================================
# 首页和静态页面
# ============================================================================

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """仪表板"""
    return render_template('dashboard.html')

@app.route('/report')
def report():
    """报告"""
    return render_template('report.html')

# ============================================================================
# 数据概览API
# ============================================================================

@app.route('/api/overview', methods=['GET'])
def get_overview():
    """获取数据概览"""
    if DATA is None:
        return jsonify({'error': '数据加载失败'}), 500
    
    orders = DATA['orders']
    dishes = DATA['dishes']
    stalls = DATA['stalls']
    order_items = DATA['order_items']
    waste = DATA['waste']
    
    order_items['amount'] = order_items['quantity'] * order_items['unit_price']
    
    return jsonify({
        'orders_count': int(orders.shape[0]),
        'dishes_count': int(dishes.shape[0]),
        'stalls_count': int(stalls.shape[0]),
        'items_count': int(order_items.shape[0]),
        'waste_count': int(waste.shape[0]),
        'total_revenue': round(order_items['amount'].sum(), 2),
        'total_waste': round(waste['waste_weight_g'].sum(), 0),
        'avg_order_value': round(order_items['amount'].sum() / orders.shape[0], 2),
    })

# ============================================================================
# 错误处理
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({'error': '页面未找到'}), 404

@app.errorhandler(500)
def server_error(error):
    """500错误处理"""
    return jsonify({'error': '服务器错误'}), 500

# ============================================================================
# 主程序
# ============================================================================

if __name__ == '__main__':
    # 创建必要的目录
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # 启动Flask应用
    app.run(debug=True, host='0.0.0.0', port=5000)
