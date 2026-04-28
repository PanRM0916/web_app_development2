# 路由與頁面設計文件 (ROUTES.md)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **書籍列表 (首頁)** | GET | `/` | `index.html` | 顯示所有書籍，支援標籤篩選 |
| **新增書籍頁面** | GET | `/books/add` | `book_form.html` | 顯示新增書籍的表單 |
| **建立書籍** | POST | `/books/add` | — | 接收表單資料，存入資料庫 |
| **書籍詳情** | GET | `/books/<int:id>` | `book_detail.html` | 顯示單本書籍資訊與筆記列表 |
| **編輯書籍頁面** | GET | `/books/<int:id>/edit` | `book_form.html` | 顯示編輯書籍的表單 |
| **更新書籍** | POST | `/books/<int:id>/edit` | — | 接收表單資料，更新資料庫 |
| **刪除書籍** | POST | `/books/<int:id>/delete` | — | 刪除書籍及其筆記，重導向回首頁 |
| **新增筆記頁面** | GET | `/books/<int:id>/notes/add` | `note_form.html` | 顯示新增筆記的表單 |
| **建立筆記** | POST | `/books/<int:id>/notes/add` | — | 針對特定書籍建立筆記 |
| **編輯筆記頁面** | GET | `/notes/<int:id>/edit` | `note_form.html` | 顯示編輯筆記的表單 |
| **更新筆記** | POST | `/notes/<int:id>/edit` | — | 接收表單資料，更新筆記 |
| **刪除筆記** | POST | `/notes/<int:id>/delete` | — | 刪除筆記，重導向回書籍詳情頁 |

---

## 2. 路由詳細說明

### 書籍管理 (Book Management)
*   **GET `/books/<id>`**
    *   **輸入**：書籍 ID (URL 參數)
    *   **處理**：呼叫 `Book.get_by_id(id)`，若不存在則回傳 404。
    *   **輸出**：渲染 `book_detail.html`，傳入書籍物件。
*   **POST `/books/add`**
    *   **輸入**：表單欄位 (title, author, isbn, total_pages, status, tags)
    *   **處理**：建立 Book 物件，處理標籤關聯。
    *   **輸出**：成功後重導向至 `/`。

### 筆記管理 (Note Management)
*   **POST `/books/<id>/notes/add`**
    *   **輸入**：書籍 ID (URL), 筆記內容 (Form)
    *   **處理**：呼叫 `Note.create()` 並與書籍關聯。
    *   **輸出**：重導向至 `/books/<id>`。

---

## 3. Jinja2 模板清單
所有模板皆位於 `app/templates/` 目錄下。

| 檔案名稱 | 繼承對象 | 說明 |
| :--- | :--- | :--- |
| `base.html` | — | 基礎佈局，包含導航列、CSS/JS 引用 |
| `index.html` | `base.html` | 書籍列表與搜尋區塊 |
| `book_detail.html` | `base.html` | 書籍詳細資訊、進度條與筆記列表 |
| `book_form.html` | `base.html` | 共用的書籍新增/編輯表單 |
| `note_form.html` | `base.html` | 共用的筆記新增/編輯表單 |

---

## 4. 路由骨架程式碼 (app/routes/)
路由將使用 Flask Blueprints 進行模組化管理。

*   `app/routes/main.py`: 處理全域頁面。
*   `app/routes/book.py`: 處理書籍 CRUD。
*   `app/routes/note.py`: 處理筆記 CRUD。
