# Discord Bot

## 簡介
這是一個 Discord 機器人，用 Python 編寫，它可以執行各種有趣的命令和操作。

## 功能
- **ping:** 獲取機器人的延遲。
- **clear:** 刪除頻道中指定數量的消息。
- **avatar:** 獲取用戶的頭像。
- **txt2img:** 讓AI實現你的想像。
## 使用方法
1. **安裝依賴：**
   ```
   pip install -r requirements.txt
   ```

2. **設置設定檔：**
   在根目錄下創建一個名為 `example.config.json` 的 JSON 格式設定檔，並添加必要的欄位，例如：
   ```json
   {
    "bot_token": "YOUR_DISCORD_BOT_TOKEN",
    "prefix": "!",
    "log_channel_id": "LOG_CHANNEL_ID",
    "error_channel_id": "ERROR_CHANNEL_ID",
    "owner_id": "OWNER_ID",
    }
   ```

3. **運行機器人：**
   運行 `main.py` 檔以啟動機器人：
   ```
   python main.py
   ```

4. **與機器人互動：**
   在 Discord 中使用首碼 `config.json中設置` 跟隨相應的命令來與機器人互動，例如：
   ```
   !help
   ```

## 注意事項
- 請確保你的 Discord Bot 已經被邀請到了你的 Discord 伺服器。
- 機器人的敏感資訊，如 Token，不應該被洩露或分享給他人。

## 常見問題
- **機器人無法正常工作怎麼辦？**
  - 請確保設定檔中的資訊是正確的，並且機器人已經被邀請到了伺服器。
  - 請確保你的機器人擁有管理權(身分組權限)，Discord developers Bot intents三項全開。

## 貢獻
歡迎貢獻程式碼或提出改進建議！如果有任何問題，請隨時提出 issue。