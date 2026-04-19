# Web Crawler AI News Summarizer 🚀

這是一個整合新聞爬蟲與 AI 摘要技術的工具。它能自動從 Yahoo 新聞抓取最新娛樂消息，並透過 Google Gemini（Gemma
3）模型進行重點摘要與實體（Entity）辨識。

---

## 📂 專案目錄結構

```Plaintext
.
├── main.py                # 程式主入口
├── config.py              # 配置管理 (讀取環境變數)
├── requirements.txt       # 套件清單 (pandas, google-genai, bs4, requests)
├── Dockerfile             # Docker 映像檔定義
├── output                 # 放置本地輸出 csv
└── repository/            # 功能模組
    ├── crawler.py         # 網頁爬蟲邏輯
    ├── ai.py              # Gemini / Gemma 模型封裝
    └── text.py           # json_to_dict 等工具函數
```

---

## 📌 功能特點

- **多執行緒爬蟲**：快速抓取新聞內文
- **AI 自動摘要**：使用 `gemma-3-1b-it` 模型進行內容分析
- **資料清洗**：自動修正 JSON 格式錯誤，並處理缺失值
- **Docker 支援**：環境隔離，一鍵執行並匯出資料

---

## 🛠 準備工作

1. **取得 Gemini API Key**
2. **安裝 Docker**  
   確保你的開發環境已安裝 Docker Engine

---

## 📦 Docker 打包步驟

在專案根目錄執行：

```bash
docker build -t news-crawler-ai .
```

## 🚀 執行與輸出 (指定路徑)

為了能將執行結果（CSV 檔案）存回你的電腦，執行時需要掛載資料夾 (Volume)。

```bash
docker run -it --rm \
  -e GEMINI_API_KEY="你的_API_KEY" \
  -e FILENAME="預期的檔案名稱" \
  -v "$(pwd)/{你預期儲存的位置}:/output" \
  news-crawler-ai
```

參數解說：

- -e GEMINI_API_KEY: 傳入你的 API 密鑰
- -e OUTPUT_PATH: 指定 CSV 在容器內的檔案名稱
- -v ...:/app/output: 將主機的資料夾映射到容器內，這樣程式跑完後，你可以在本地的 指定資料夾找到檔案
- --rm: 程式執行完畢後自動移除容器，節省磁碟空間