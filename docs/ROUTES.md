# 路由設計 (Routes Design)

本文件定義「食譜收藏夾」網站的路由清單、對應邏輯以及所需的 HTML 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (食譜列表) | GET | `/` | `index.html` | 顯示所有食譜列表 |
| 搜尋食譜 | GET | `/search` | `index.html` | 根據關鍵字搜尋食譜並顯示結果 |
| 新增食譜頁面 | GET | `/recipes/new` | `recipe_form.html` | 顯示新增食譜表單 |
| 建立食譜 | POST | `/recipes/new` | — | 接收表單，存入資料庫，成功後重導向至詳細頁 |
| 食譜詳細頁面 | GET | `/recipes/<int:recipe_id>` | `recipe_detail.html` | 顯示單一食譜的材料與步驟 |

*(註：本階段為 MVP，編輯與刪除功能將在後續階段加入。)*

## 2. 每個路由的詳細說明

### `GET /` (首頁)
- **處理邏輯**：呼叫 `RecipeModel.get_all()` 取得所有食譜資料。
- **輸出**：渲染 `index.html`，將食譜列表傳入模板。

### `GET /search` (搜尋)
- **輸入**：URL 參數 `q` (例如：`/?q=牛肉`)。
- **處理邏輯**：如果 `q` 有值，呼叫 `RecipeModel.search(q)`；如果無值，導回首頁。
- **輸出**：渲染 `index.html`，顯示搜尋結果。

### `GET /recipes/new` (新增食譜頁面)
- **處理邏輯**：直接準備空表單。
- **輸出**：渲染 `recipe_form.html`。

### `POST /recipes/new` (建立食譜)
- **輸入**：表單資料 (包含 title, description, image_path, ingredients, steps 等)。
- **處理邏輯**：解析表單並整理成對應格式，呼叫 `RecipeModel.create(...)` 存入資料庫。
- **錯誤處理**：若必填欄位缺失，可回傳錯誤訊息並重新渲染 `recipe_form.html`。
- **輸出**：成功後使用 `redirect` 重導向到剛建立的食譜詳細頁 `/recipes/<recipe_id>`。

### `GET /recipes/<int:recipe_id>` (食譜詳細頁面)
- **輸入**：網址中的 `recipe_id`。
- **處理邏輯**：呼叫 `RecipeModel.get_by_id(recipe_id)`。
- **錯誤處理**：如果找不到資料，回傳 404 Not Found 頁面。
- **輸出**：渲染 `recipe_detail.html`。

## 3. Jinja2 模板清單

所有的 HTML 檔案皆存放於 `app/templates/` 目錄：

1. **`base.html`**：共用版型，包含 HTML 骨架、`<head>`、導覽列與頁尾。
2. **`index.html`**：首頁 / 搜尋結果頁。繼承自 `base.html`，以卡片形式顯示食譜列表。
3. **`recipe_detail.html`**：食譜詳細頁。繼承自 `base.html`，顯示圖文、材料清單與步驟說明。
4. **`recipe_form.html`**：新增食譜表單頁。繼承自 `base.html`，包含輸入食譜資訊、動態新增材料與步驟欄位的 UI。

## 4. 路由骨架

請參考 `app/routes/` 目錄內的 `.py` 檔案（`main_routes.py` 與 `recipe_routes.py`）。
