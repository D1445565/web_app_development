from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    首頁：呼叫 Model 取得所有食譜，並渲染 index.html
    """
    pass

@main_bp.route('/search', methods=['GET'])
def search():
    """
    搜尋：根據 GET 參數 q 搜尋食譜，並渲染 index.html
    """
    pass
