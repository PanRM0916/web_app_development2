# 系統流程圖與操作路徑 (FLOWCHART.md)

## 1. 使用者流程圖 (User Flow)
描述使用者進入系統後，如何與各項功能進行互動。

```mermaid
flowchart LR
    Start([使用者開啟網站]) --> Home[首頁 / 書籍清單]
    
    Home -->|點擊書籍| BookDetail[書籍詳情 / 筆記列表]
    Home -->|點擊新增書籍| AddBook[新增書籍表單]
    Home -->|標籤篩選| Home
    
    AddBook -->|送出| Home
    
    BookDetail -->|點擊筆記| ViewNote[查看筆記內容]
    BookDetail -->|點擊新增筆記| AddNote[新增筆記表單]
    BookDetail -->|返回| Home
    
    AddNote -->|送出| BookDetail
    ViewNote -->|點擊編輯| EditNote[編輯筆記表單]
    ViewNote -->|返回| BookDetail
    
    EditNote -->|儲存| ViewNote
```

---

## 2. 系統序列圖 (Sequence Diagram)
以「新增書籍筆記」為例，展示資料在不同元件間的流動過程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as SQLAlchemy Model
    participant DB as SQLite

    User->>Browser: 在筆記頁面填寫內容並點擊「儲存」
    Browser->>Flask: POST /books/<id>/notes/add
    
    activate Flask
    Flask->>Model: 建立 Note 物件並帶入資料
    Model->>DB: INSERT INTO notes (content, book_id, ...)
    activate DB
    DB-->>Model: 寫入成功
    deactivate DB
    Model-->>Flask: 回傳 Note 物件
    
    Flask-->>Browser: Redirect to /books/<id> (302)
    deactivate Flask
    
    Browser->>Flask: GET /books/<id>
    Flask->>DB: SELECT notes FROM notes WHERE book_id = <id>
    DB-->>Flask: 回傳筆記列表
    Flask-->>Browser: 渲染 book_detail.html
    Browser-->>User: 顯示包含新筆記的頁面
```

---

## 3. 功能清單與路徑對照表 (Route Map)
根據架構設計規劃的路由對應。

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **首頁 (書籍清單)** | `/` | GET | 顯示所有書籍，支援標籤篩選 |
| **新增書籍** | `/books/add` | GET/POST | 顯示表單與處理新增邏輯 |
| **書籍詳情** | `/books/<int:id>` | GET | 顯示特定書籍資訊與該書筆記列表 |
| **刪除書籍** | `/books/<int:id>/delete` | POST | 刪除書籍及其關聯筆記 |
| **新增筆記** | `/books/<int:id>/notes/add` | GET/POST | 針對特定書籍新增筆記 |
| **編輯筆記** | `/notes/<int:id>/edit` | GET/POST | 編輯現有筆記內容 |
| **刪除筆記** | `/notes/<int:id>/delete` | POST | 刪除特定筆記 |
