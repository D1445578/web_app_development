from flask import Blueprint, request, render_template, redirect, url_for

bp = Blueprint('found', __name__, url_prefix='/found')

@bp.route('/new', methods=['GET', 'POST'])
def new_found_item():
    """
    HTTP GET: 顯示拾獲物的新增表單
    HTTP POST: 接收表單與附圖，存入資料庫
    """
    if request.method == 'POST':
        # 實作表單接收邏輯
        pass
    
    # 實作表單頁面渲染邏輯
    pass
