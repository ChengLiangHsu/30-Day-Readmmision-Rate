# 部署說明 (Deployment Guide)

本專案已配置為可透過 Docker 進行單一容器部署，這表示您可以將前端 (Vue) 與後端 (Flask) 包裝在一起發布到任何支援 Docker 的雲端平台。

## 部署選項

### 1. 使用 Render (推薦，有免費方案)
Render 是一個簡單的雲端平台，可以直接連結 GitHub 進行部署。

1. 將代碼推送到 GitHub。
2. 在 [Render.com](https://render.com) 註冊帳號。
3. 點擊 "New +" -> "Web Service"。
4. 連結您的 GitHub Repository。
5. **關鍵步驟**：在設定頁面中，請確認 **Language** (Runtime) 選擇的是 **Docker**。
   - 如果 Render 預設選了 "Python"，請手動切換成 "Docker"。
   - **不要** 在 Build Command 欄位輸入 docker 指令，選擇 Docker Runtime 後 Render 會自動讀取 Dockerfile。
6. 點擊 "Create Web Service"。
7. 等待建置完成，您將獲得一個公開網址。

### 2. 使用 Railway
1. 在 [Railway.app](https://railway.app) 註冊。
2. 選擇 "Deploy from GitHub repo"。
3. Railway 會自動讀取 `Dockerfile` 並開始部署。

### 3. 本地測試 Docker
如果您安裝了 Docker Desktop，可以在本地測試：

```bash
# 建置映像檔
docker build -t hospital-app .

# 執行容器 (映射 Port 5000)
docker run -p 5000:5000 hospital-app
```
然後打開瀏覽器訪問 `http://localhost:5000`。

## 專案結構變更說明

為了支援部署，做了以下調整：

1. **Frontend (`frontend/`)**:
   - API 呼叫已改為相對路徑 (例如 `/predict` 而非 `http://localhost:5000/predict`)。
   - `vite.config.js` 加入了 Proxy 設定，讓您在本地開發 (`npm run dev`) 時仍能連線到後端。

2. **Backend (`backend/`)**:
   - `app.py` 已設定為在根路徑 `/` 提供前端網頁 (`index.html`)。
   - 新增 `Dockerfile` 用於自動化建置與執行。
   - 新增 `requirements.txt` 定義 Python 套件需求。

## 本地開發 (Local Development)

若要在本地繼續開發，請開啟兩個終端機：

**Terminal 1 (Backend):**
```bash
cd backend
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```
前端將在 `http://localhost:5173` 運行，並透過 Proxy 連線到 `http://localhost:5000` 的後端。
