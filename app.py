import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import or_

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

from models import Memo

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    search = request.args.get('search', '')
    if search:
        memos = Memo.query.filter(
            or_(
                Memo.title.ilike(f'%{search}%'),
                Memo.content.ilike(f'%{search}%')
            )
        ).order_by(Memo.created_at.desc()).all()
    else:
        memos = Memo.query.order_by(Memo.created_at.desc()).all()
    return render_template('index.html', memos=memos, search=search)

@app.route('/memo/new', methods=['POST'])
def new_memo():
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    
    if not title or not content:
        flash('タイトルと内容を入力してください。', 'danger')
        return redirect(url_for('index'))
    
    memo = Memo(title=title, content=content)
    db.session.add(memo)
    db.session.commit()
    flash('メモを作成しました。', 'success')
    return redirect(url_for('index'))

@app.route('/memo/<int:id>/edit', methods=['POST'])
def edit_memo(id):
    memo = Memo.query.get_or_404(id)
    memo.title = request.form.get('title', '').strip()
    memo.content = request.form.get('content', '').strip()
    
    if not memo.title or not memo.content:
        flash('タイトルと内容を入力してください。', 'danger')
        return redirect(url_for('index'))
    
    memo.updated_at = datetime.utcnow()
    db.session.commit()
    flash('メモを更新しました。', 'success')
    return redirect(url_for('index'))

@app.route('/memo/<int:id>/delete', methods=['POST'])
def delete_memo(id):
    memo = Memo.query.get_or_404(id)
    db.session.delete(memo)
    db.session.commit()
    flash('メモを削除しました。', 'success')
    return redirect(url_for('index'))
