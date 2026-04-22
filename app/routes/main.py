from flask import Blueprint, request, render_template, abort
from app.models.items import get_all_items, get_item_by_id

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    HTTP GET
    首頁，顯示最新遺失物與拾獲物列表。
    """
    items = get_all_items()
    return render_template('index.html', items=items)

@bp.route('/search')
def search():
    """
    HTTP GET
    根據 URL 參數進行搜尋與篩選。
    """
    q = request.args.get('q', '')
    item_type = request.args.get('type', '')
    items = get_all_items(item_type=item_type if item_type else None, search_query=q if q else None)
    return render_template('index.html', items=items, search_query=q, current_type=item_type)

@bp.route('/items/<int:item_id>')
def item_detail(item_id):
    """
    HTTP GET
    顯示特定物品的詳細資訊與聯絡方式。
    """
    item = get_item_by_id(item_id)
    if not item:
        abort(404)
    return render_template('detail.html', item=item)

@bp.route('/items/<int:item_id>/matches')
def item_matches(item_id):
    """
    HTTP GET
    顯示針對特定物件的比對建議列表。
    """
    item = get_item_by_id(item_id)
    if not item:
        abort(404)
    
    # 配對邏輯：找另一種類型，且標題或地點相似
    target_type = 'found' if item['item_type'] == 'lost' else 'lost'
    matches = get_all_items(item_type=target_type, search_query=item['title'])
    
    return render_template('matches.html', item=item, matches=matches)
