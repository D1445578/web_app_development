import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from app.models.items import create_item

bp = Blueprint('found', __name__, url_prefix='/found')

@bp.route('/new', methods=['GET', 'POST'])
def new_found_item():
    """
    HTTP GET: 顯示拾獲物的新增表單
    HTTP POST: 接收表單與附圖，存入資料庫
    """
    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location')
        description = request.form.get('description', '')
        item_date = request.form.get('item_date', '')
        contact_info = request.form.get('contact_info', '')
        
        if not title or not location:
            flash('物品名稱與地點為必填', 'danger')
            return render_template('form.html', form_type='found')

        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads')
                file.save(os.path.join(uploads_dir, filename))
                image_path = f'uploads/{filename}'
        
        data = {
            'item_type': 'found',
            'title': title,
            'description': description,
            'location': location,
            'item_date': item_date,
            'image_path': image_path,
            'contact_info': contact_info,
            'status': 'open'
        }
        
        item_id = create_item(data)
        flash('拾獲物登記成功！', 'success')
        return redirect(url_for('main.item_detail', item_id=item_id))
        
    return render_template('form.html', form_type='found')
