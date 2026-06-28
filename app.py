"""
Flask后端：校园食堂数据看板接口
支持三个筛选参数：start, end, stall_id（都是可选）
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

# ==================== 工具函数 ====================
def ok(data):
    """成功响应"""
    return jsonify({"success": True, "data": data, "message": ""})

def err(msg):
    """错误响应"""
    return jsonify({"success": False, "data": None, "message": msg}), 400

def load_data():
    """加载所有CSV文件"""
    try:
        orders = pd.read_csv('data/orders.csv')
        dishes = pd.read_csv('data/dishes.csv')
        order_items = pd.read_csv('data/order_items.csv')
        waste_records = pd.read_csv('data/waste_records.csv')
        
        # 转换时间列为datetime
        orders['ordered_at'] = pd.to_datetime(orders['ordered_at'])
        waste_records['recorded_date'] = pd.to_datetime(waste_records['recorded_date'])
        
        return orders, dishes, order_items, waste_records
    except Exception as e:
        print(f"数据加载错误: {e}")
        return None, None, None, None

def apply_filters(order_items, orders, dishes, start=None, end=None, stall_id=None):
    """
    应用筛选条件
    - start/end: 日期范围 (YYYY-MM-DD格式)
    - stall_id: 档口ID
    """
    # 先合并订单信息
    merged = order_items.merge(orders, left_on='order_id', right_on='id', how='left')
    merged = merged.merge(dishes, left_on='dish_id', right_on='id', how='left', suffixes=('_order', '_dish'))
    
    # 按日期筛选
    if start:
        try:
            start_date = pd.to_datetime(start).date()
            merged = merged[merged['ordered_at'].dt.date >= start_date]
        except:
            pass
    
    if end:
        try:
            end_date = pd.to_datetime(end).date()
            merged = merged[merged['ordered_at'].dt.date <= end_date]
        except:
            pass
    
    # 按档口筛选
    if stall_id:
        try:
            stall_id = int(stall_id)
            merged = merged[merged['stall_id'] == stall_id]
        except:
            pass
    
    return merged

# ==================== API 接口 ====================

@app.get("/api/summary")
def summary():
    """
    获取汇总指标：营业额、订单数、客单价
    
    参数：
    - start: 开始日期 (YYYY-MM-DD)
    - end: 结束日期 (YYYY-MM-DD)
    - stall_id: 档口ID
    """
    start = request.args.get('start')
    end = request.args.get('end')
    stall_id = request.args.get('stall_id')
    
    orders, dishes, order_items, waste_records = load_data()
    
    if orders is None:
        return err("数据加载失败")
    
    # 应用筛选
    merged = apply_filters(order_items, orders, dishes, start, end, stall_id)
    
    if len(merged) == 0:
        return ok({
            "revenue": 0,
            "order_count": 0,
            "avg_order_value": 0
        })
    
    # 计算营业额：SUM(quantity * unit_price)
    merged['line_revenue'] = merged['quantity'] * merged['unit_price']
    revenue = merged['line_revenue'].sum()
    
    # 计算订单数：COUNT(DISTINCT order_id)
    order_count = merged['order_id'].nunique()
    
    # 计算客单价
    avg_order_value = revenue / order_count if order_count > 0 else 0
    
    return ok({
        "revenue": round(float(revenue), 2),
        "order_count": int(order_count),
        "avg_order_value": round(float(avg_order_value), 2)
    })

@app.get("/api/trend")
def trend():
    """
    获取每日营业额趋势
    
    参数：
    - start: 开始日期 (YYYY-MM-DD)
    - end: 结束日期 (YYYY-MM-DD)
    - stall_id: 档口ID
    
    返回：[{date, revenue, order_count}, ...]
    """
    start = request.args.get('start')
    end = request.args.get('end')
    stall_id = request.args.get('stall_id')
    
    orders, dishes, order_items, waste_records = load_data()
    
    if orders is None:
        return err("数据加载失败")
    
    # 应用筛选
    merged = apply_filters(order_items, orders, dishes, start, end, stall_id)
    
    if len(merged) == 0:
        return ok([])
    
    # 按日期分组
    merged['date'] = merged['ordered_at'].dt.date
    merged['line_revenue'] = merged['quantity'] * merged['unit_price']
    
    daily = merged.groupby('date').agg({
        'line_revenue': 'sum',
        'order_id': 'nunique'
    }).reset_index()
    
    daily.columns = ['date', 'revenue', 'order_count']
    daily['date'] = daily['date'].astype(str)
    daily = daily.sort_values('date')
    
    return ok(daily.to_dict(orient='records'))

@app.get("/api/ranking")
def ranking():
    """
    获取菜品销量排行（前10）
    
    参数：
    - start: 开始日期 (YYYY-MM-DD)
    - end: 结束日期 (YYYY-MM-DD)
    - stall_id: 档口ID
    
    返回：[{dish_name, quantity}, ...]
    """
    start = request.args.get('start')
    end = request.args.get('end')
    stall_id = request.args.get('stall_id')
    
    orders, dishes, order_items, waste_records = load_data()
    
    if orders is None:
        return err("数据加载失败")
    
    # 应用筛选
    merged = apply_filters(order_items, orders, dishes, start, end, stall_id)
    
    if len(merged) == 0:
        return ok([])
    
    # 按菜品分组，求和销量
    ranking_data = merged.groupby('name_dish')['quantity'].sum().reset_index()
    ranking_data.columns = ['dish_name', 'quantity']
    ranking_data = ranking_data.sort_values('quantity', ascending=False).head(10)
    
    return ok(ranking_data.to_dict(orient='records'))

@app.get("/api/waste")
def waste_list():
    """
    获取浪费记录列表
    
    返回：[{id, dish_name, recorded_date, waste_weight_g, reason}, ...]
    """
    orders, dishes, order_items, waste_records = load_data()
    
    if waste_records is None:
        return err("数据加载失败")
    
    # 合并菜品名称
    merged = waste_records.merge(dishes[['id', 'name']], left_on='dish_id', right_on='id', how='left')
    
    result = merged[['id_x', 'name', 'recorded_date', 'waste_weight_g', 'reason']].copy()
    result.columns = ['id', 'dish_name', 'recorded_date', 'waste_weight_g', 'reason']
    result['recorded_date'] = result['recorded_date'].astype(str)
    
    return ok(result.to_dict(orient='records'))

@app.post("/api/waste")
def add_waste():
    """新增浪费记录"""
    try:
        data = request.get_json()
        
        # 验证必需字段
        required = ['dish_id', 'recorded_date', 'waste_weight_g', 'reason']
        if not all(k in data for k in required):
            return err("缺少必需字段")
        
        orders, dishes, order_items, waste_records = load_data()
        
        # 新记录ID = 最大ID + 1
        new_id = waste_records['id'].max() + 1
        
        new_record = {
            'id': new_id,
            'dish_id': int(data['dish_id']),
            'recorded_date': data['recorded_date'],
            'waste_weight_g': int(data['waste_weight_g']),
            'reason': data['reason']
        }
        
        # 追加到CSV
        waste_records = pd.concat([
            waste_records,
            pd.DataFrame([new_record])
        ], ignore_index=True)
        
        waste_records.to_csv('data/waste_records.csv', index=False)
        
        return ok(new_record)
    
    except Exception as e:
        return err(f"新增失败: {str(e)}")

@app.put("/api/waste/<int:waste_id>")
def update_waste(waste_id):
    """修改浪费记录"""
    try:
        data = request.get_json()
        orders, dishes, order_items, waste_records = load_data()
        
        if waste_id not in waste_records['id'].values:
            return err("记录不存在")
        
        # 更新字段
        mask = waste_records['id'] == waste_id
        for key in data:
            if key in waste_records.columns:
                waste_records.loc[mask, key] = data[key]
        
        waste_records.to_csv('data/waste_records.csv', index=False)
        
        record = waste_records[mask].iloc[0].to_dict()
        return ok(record)
    
    except Exception as e:
        return err(f"修改失败: {str(e)}")

@app.delete("/api/waste/<int:waste_id>")
def delete_waste(waste_id):
    """删除浪费记录"""
    try:
        orders, dishes, order_items, waste_records = load_data()
        
        if waste_id not in waste_records['id'].values:
            return err("记录不存在")
        
        waste_records = waste_records[waste_records['id'] != waste_id]
        waste_records.to_csv('data/waste_records.csv', index=False)
        
        return ok({"id": waste_id})
    
    except Exception as e:
        return err(f"删除失败: {str(e)}")

# ==================== 错误处理 ====================
@app.errorhandler(404)
def not_found(e):
    return err("接口不存在"), 404

@app.errorhandler(500)
def server_error(e):
    return err("服务器错误"), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
