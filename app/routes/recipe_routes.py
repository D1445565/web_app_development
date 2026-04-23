from flask import Blueprint, render_template, request, redirect, url_for

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

@recipe_bp.route('/new', methods=['GET', 'POST'])
def new_recipe():
    """
    GET: 渲染 recipe_form.html 顯示新增表單
    POST: 接收表單資料，呼叫 Model 寫入資料庫，並重導向至詳細頁面
    """
    pass

@recipe_bp.route('/<int:recipe_id>', methods=['GET'])
def recipe_detail(recipe_id):
    """
    檢視單一食譜：呼叫 Model 取得詳細資料，若找不到則回傳 404，否則渲染 recipe_detail.html
    """
    pass
