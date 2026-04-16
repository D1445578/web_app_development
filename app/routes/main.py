from flask import Blueprint, request, render_template, redirect, url_for

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    HTTP GET
    首頁，顯示最新遺失物與拾獲物列表。
    """
    pass

@bp.route('/search')
def search():
    """
    HTTP GET
    根據 URL 參數進行搜尋與篩選。
    """
    pass

@bp.route('/items/<int:item_id>')
def item_detail(item_id):
    """
    HTTP GET
    顯示特定物品的詳細資訊與聯絡方式。
    """
    pass

@bp.route('/items/<int:item_id>/matches')
def item_matches(item_id):
    """
    HTTP GET
    顯示針對特定物件的比對建議列表。
    """
    pass
