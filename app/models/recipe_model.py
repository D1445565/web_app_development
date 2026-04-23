from .db import get_db_connection

class RecipeModel:
    @staticmethod
    def get_all():
        """取得所有食譜"""
        conn = get_db_connection()
        recipes = conn.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(r) for r in recipes]

    @staticmethod
    def get_by_id(recipe_id):
        """根據 ID 取得單一食譜，包含食材與步驟"""
        conn = get_db_connection()
        
        # 查詢食譜主體
        recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
        if not recipe:
            conn.close()
            return None
            
        recipe_dict = dict(recipe)
        
        # 查詢食材
        ingredients = conn.execute('SELECT * FROM ingredients WHERE recipe_id = ?', (recipe_id,)).fetchall()
        recipe_dict['ingredients'] = [dict(i) for i in ingredients]
        
        # 查詢步驟
        steps = conn.execute('SELECT * FROM steps WHERE recipe_id = ? ORDER BY step_number ASC', (recipe_id,)).fetchall()
        recipe_dict['steps'] = [dict(s) for s in steps]
        
        conn.close()
        return recipe_dict

    @staticmethod
    def create(title, description, image_path, ingredients_list, steps_list):
        """新增食譜，並同時寫入食材與步驟"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # 1. 寫入食譜主表
            cursor.execute('''
                INSERT INTO recipes (title, description, image_path)
                VALUES (?, ?, ?)
            ''', (title, description, image_path))
            
            recipe_id = cursor.lastrowid
            
            # 2. 寫入食材 (ingredients_list 預期格式: [{'name': '牛肉', 'amount': '500g'}, ...])
            for item in ingredients_list:
                cursor.execute('''
                    INSERT INTO ingredients (recipe_id, name, amount)
                    VALUES (?, ?, ?)
                ''', (recipe_id, item['name'], item.get('amount', '')))
                
            # 3. 寫入步驟 (steps_list 預期格式: [{'content': '切塊'}, ...])
            for idx, step in enumerate(steps_list):
                cursor.execute('''
                    INSERT INTO steps (recipe_id, step_number, content)
                    VALUES (?, ?, ?)
                ''', (recipe_id, idx + 1, step['content']))
                
            # 提交交易
            conn.commit()
            return recipe_id
            
        except Exception as e:
            # 若中間有任何錯誤，還原所有操作，確保資料一致性
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def search(query):
        """簡單的關鍵字搜尋，比對標題與簡介"""
        conn = get_db_connection()
        like_query = f"%{query}%"
        recipes = conn.execute('''
            SELECT * FROM recipes 
            WHERE title LIKE ? OR description LIKE ?
            ORDER BY created_at DESC
        ''', (like_query, like_query)).fetchall()
        conn.close()
        return [dict(r) for r in recipes]
