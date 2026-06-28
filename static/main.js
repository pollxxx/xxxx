// ==================== 全局配置 ====================
const API_BASE = 'http://127.0.0.1:5000';
let trendChart = null;
let rankingChart = null;

// ==================== 工具函数 ====================
function showMessage(msg, type = 'success') {
    const msgDiv = document.getElementById('message');
    msgDiv.className = type;
    msgDiv.textContent = msg;
    msgDiv.style.display = 'block';
    setTimeout(() => {
        msgDiv.style.display = 'none';
    }, 3000);
}

function getFilters() {
    return {
        start: document.getElementById('startDate').value || '',
        end: document.getElementById('endDate').value || '',
        stall_id: document.getElementById('stallId').value || ''
    };
}

function buildQueryString(params) {
    return Object.keys(params)
        .filter(key => params[key])
        .map(key => `${key}=${encodeURIComponent(params[key])}`)
        .join('&');
}

function clearFilters() {
    document.getElementById('startDate').value = '';
    document.getElementById('endDate').value = '';
    document.getElementById('stallId').value = '';
    loadAllData();
}

// ==================== 数据加载函数 ====================
async function loadSummary() {
    try {
        const filters = getFilters();
        const query = buildQueryString(filters);
        const url = `${API_BASE}/api/summary${query ? '?' + query : ''}`;
        
        const res = await fetch(url);
        const body = await res.json();
        
        if (body.success) {
            document.getElementById('revenue').textContent = '¥' + body.data.revenue.toFixed(2);
            document.getElementById('orderCount').textContent = body.data.order_count;
            document.getElementById('avgOrderValue').textContent = '¥' + body.data.avg_order_value.toFixed(2);
        } else {
            showMessage('加载汇总数据失败：' + body.message, 'error');
        }
    } catch (error) {
        console.error('汇总数据加载错误:', error);
        showMessage('网络错误：' + error.message, 'error');
    }
}

async function loadTrend() {
    try {
        const filters = getFilters();
        const query = buildQueryString(filters);
        const url = `${API_BASE}/api/trend${query ? '?' + query : ''}`;
        
        const res = await fetch(url);
        const body = await res.json();
        
        if (body.success && body.data.length > 0) {
            const rows = body.data;
            
            if (!trendChart) {
                trendChart = echarts.init(document.querySelector('#trendChart'));
            }
            
            trendChart.setOption({
                title: { text: '' },
                tooltip: { 
                    trigger: 'axis',
                    formatter: (params) => {
                        if (params.length > 0) {
                            const data = params[0].data;
                            return `日期: ${params[0].axisValue}<br/>营业额: ¥${data.toFixed(2)}`;
                        }
                        return '';
                    }
                },
                grid: { containLabel: true },
                xAxis: { 
                    type: 'category', 
                    data: rows.map(r => r.date),
                    axisLabel: { rotate: 45 }
                },
                yAxis: { 
                    type: 'value', 
                    name: '元',
                    axisLabel: { formatter: '¥{value}' }
                },
                series: [{
                    type: 'line',
                    data: rows.map(r => r.revenue),
                    smooth: true,
                    itemStyle: { color: '#667eea' },
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: 'rgba(102, 126, 234, 0.3)' },
                            { offset: 1, color: 'rgba(102, 126, 234, 0.1)' }
                        ])
                    }
                }]
            });
        } else if (body.success) {
            showMessage('暂无趋势数据', 'error');
        } else {
            showMessage('加载趋势数据失败：' + body.message, 'error');
        }
    } catch (error) {
        console.error('趋势数据加载错误:', error);
        showMessage('网络错误：' + error.message, 'error');
    }
}

async function loadRanking() {
    try {
        const filters = getFilters();
        const query = buildQueryString(filters);
        const url = `${API_BASE}/api/ranking${query ? '?' + query : ''}`;
        
        const res = await fetch(url);
        const body = await res.json();
        
        if (body.success && body.data.length > 0) {
            const rows = body.data;
            
            if (!rankingChart) {
                rankingChart = echarts.init(document.querySelector('#rankingChart'));
            }
            
            rankingChart.setOption({
                title: { text: '' },
                tooltip: { trigger: 'axis' },
                grid: { containLabel: true },
                xAxis: { 
                    type: 'category', 
                    data: rows.map(r => r.dish_name),
                    axisLabel: { 
                        interval: 0,
                        rotate: 45,
                        fontSize: 12
                    }
                },
                yAxis: { 
                    type: 'value', 
                    name: '份数'
                },
                series: [{
                    type: 'bar',
                    data: rows.map(r => r.quantity),
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: '#667eea' },
                            { offset: 1, color: '#764ba2' }
                        ])
                    }
                }]
            });
        } else if (body.success) {
            showMessage('暂无排行数据', 'error');
        } else {
            showMessage('加载排行数据失败：' + body.message, 'error');
        }
    } catch (error) {
        console.error('排行数据加载错误:', error);
        showMessage('网络错误：' + error.message, 'error');
    }
}

async function loadWasteList() {
    try {
        const res = await fetch(`${API_BASE}/api/waste`);
        const body = await res.json();
        
        if (body.success) {
            const tbody = document.getElementById('wasteTableBody');
            
            if (body.data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #999;">暂无浪费记录</td></tr>';
                return;
            }
            
            tbody.innerHTML = body.data.map(row => `
                <tr>
                    <td>${row.id}</td>
                    <td>${row.dish_name}</td>
                    <td>${row.recorded_date}</td>
                    <td>${row.waste_weight_g}</td>
                    <td>${row.reason}</td>
                    <td>
                        <div class="actions">
                            <button class="btn-small" onclick="editWaste(${row.id})">编辑</button>
                            <button class="btn-small btn-delete" onclick="deleteWaste(${row.id})">删除</button>
                        </div>
                    </td>
                </tr>
            `).join('');
        } else {
            showMessage('加载浪费记录失败：' + body.message, 'error');
        }
    } catch (error) {
        console.error('浪费记录加载错误:', error);
        showMessage('网络错误：' + error.message, 'error');
    }
}

// ==================== 写操作函数 ====================
async function addWaste() {
    const dishId = document.getElementById('newWasteDishId').value;
    const date = document.getElementById('newWasteDate').value;
    const weight = document.getElementById('newWasteWeight').value;
    const reason = document.getElementById('newWasteReason').value;
    
    if (!dishId || !date || !weight || !reason) {
        showMessage('请填写所有字段', 'error');
        return;
    }
    
    try {
        const res = await fetch(`${API_BASE}/api/waste`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                dish_id: parseInt(dishId),
                recorded_date: date,
                waste_weight_g: parseInt(weight),
                reason: reason
            })
        });
        
        const body = await res.json();
        
        if (body.success) {
            showMessage('✅ 新增成功');
            document.getElementById('newWasteDishId').value = '';
            document.getElementById('newWasteDate').value = '';
            document.getElementById('newWasteWeight').value = '';
            document.getElementById('newWasteReason').value = '';
            loadWasteList();
        } else {
            showMessage('新增失败：' + body.message, 'error');
        }
    } catch (error) {
        showMessage('网络错误：' + error.message, 'error');
    }
}

async function deleteWaste(id) {
    if (!confirm('确定要删除这条记录吗？')) return;
    
    try {
        const res = await fetch(`${API_BASE}/api/waste/${id}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const body = await res.json();
        
        if (body.success) {
            showMessage('✅ 删除成功');
            loadWasteList();
        } else {
            showMessage('删除失败：' + body.message, 'error');
        }
    } catch (error) {
        showMessage('网络错误：' + error.message, 'error');
    }
}

function editWaste(id) {
    // 进阶功能：实现编辑功能
    alert('编辑功能开发中...');
}

// ==================== 主加载函数 ====================
async function loadAllData() {
    await Promise.all([
        loadSummary(),
        loadTrend(),
        loadRanking(),
        loadWasteList()
    ]);
}

// ==================== 初始化 ====================
window.addEventListener('load', () => {
    loadAllData();
    
    // 窗口resize时重新绘制图表
    window.addEventListener('resize', () => {
        if (trendChart) trendChart.resize();
        if (rankingChart) rankingChart.resize();
    });
});
