# 路由設計文件 (API & Routes Design)

這份文件用於定義校園遺失物查詢系統中，所有介面的 URL 路由設計、藍圖 (Blueprint) 切割、與負責響應的視圖模板。

## 1. 路由總覽表格

| 模組 | 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| `main` | 首頁與全部列表 | GET | `/` | `index.html` | 進入系統的第一畫面，預設顯示所有遺失與拾獲清單 |
| `main` | 搜尋與篩選結果 | GET | `/search` | `index.html` | 接收 `?q=` 或 `?type=` 等參數，查詢符合的物件 |
| `main` | 物件詳情頁面 | GET | `/items/<int:item_id>` | `detail.html` | 根據特定 ID 顯示完整的物件資訊與聯絡方式 |
| `main` | 潛在配對提示 | GET | `/items/<int:item_id>/matches`| `matches.html` | 基於特徵或地名自動比對出的建議列表 |
| `lost` | 新增遺失物(頁面)| GET | `/lost/new` | `form.html` | 顯示讓使用者填寫遺失內容的表單 |
| `lost` | 新增遺失物(送出)| POST | `/lost/new` | — | 寫入資料庫，成功後重導向至其詳情頁 |
| `found`| 新增拾獲物(頁面)| GET | `/found/new` | `form.html` | 顯示讓使用者填寫拾獲內容的表單 |
| `found`| 新增拾獲物(送出)| POST | `/found/new` | — | 寫入資料庫，成功後重導向至其詳情頁 |

## 2. 路由詳細說明

### Blueprint: `main`

- **首頁與全部列表 (`/`)**
  - **輸入**: 無
  - **處理邏輯**: 呼叫 `get_all_items()`，無條件抓取最近建立的文章
  - **輸出**: 渲染 `index.html`，帶入 `items` 變數
  - **錯誤處理**: 資料庫連線異常時回傳 500
- **搜尋與篩選 (`/search`)**
  - **輸入**: URL 參數 `q` (字串)、`location` (字串)
  - **處理邏輯**: 取出參數後呼叫 `get_all_items(search_query=q)`
  - **輸出**: 同樣渲染 `index.html`，帶入 `items` 變數
- **物件詳情 (`/items/<id>`)**
  - **輸入**: URL 中的 `id`
  - **處理邏輯**: `get_item_by_id(id)`
  - **輸出**: `detail.html`，帶入 `item` 變數
  - **錯誤處理**: 若回傳 Null 則報錯 404 Not Found
- **潛在配對 (`/items/<id>/matches`)**
  - **輸入**: URL 中的 `id`
  - **處理邏輯**: 取得本身資料後，根據條件 (反向類型、相同關鍵字等地緣因素) 篩選 `items` 表
  - **輸出**: `matches.html`

### Blueprint: `lost` 與 `found`

- **新增資料 (GET `/lost/new` 或 `/found/new`)**
  - **輸出**: `form.html` (透過變數傳遞，通知模板目前是建立 lost 還是 found 以變更標題)
- **送出資料 (POST `/lost/new` 或 `/found/new`)**
  - **輸入**: 表單資料 `FormData` (title, description, location, item_date, contact_info, 以及上傳的圖片)
  - **處理邏輯**: 
    1. 驗證必填。
    2. 儲存實體圖片至 `static/uploads/` 並取得路徑。
    3. 插入欄位資料至資料庫 `items` 中，`item_type` 自動帶為對應類型。
  - **輸出**: 重導向 (Redirect) 至 `/items/<new_id>`
  - **錯誤處理**: 若表單驗證有誤，返回原本表單頁面帶上 Error Message

## 3. Jinja2 模板清單

將在 `app/templates/` 中建立如下清單與繼承關係：

1. **`base.html`**
   - 包含 `<head>` 區塊 (載入 CSS/JS)，以及頂部 Navbar (導覽列) 與 Footer。做為系統的主框架。
2. **`index.html`** (繼承自 `base.html`)
   - `<main>` 中用於顯示多筆物品清單的 Card Grid 設計，並在其頂部附帶一個簡易的搜尋 Bar。
3. **`form.html`** (繼承自 `base.html`)
   - `<main>` 中提供給「遺失」或「拾獲」的共通 HTML `<form>`。會依照後端傳來的變數來動態隱藏/顯示不需填寫的欄位或切換標題名稱。
4. **`detail.html`** (繼承自 `base.html`)
   - 用於單筆物品展示的介紹頁。大圖瀏覽區與屬性條列區塊。
5. **`matches.html`** (繼承自 `base.html`)
   - 用於顯示系統找到的可能吻合項目列表 (與 index 相似，但針對特定物件產生)。
