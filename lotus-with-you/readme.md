這是一個 Python 程式，您可以按照以下步驟在您的電腦上運行它：
1. 準備環境
確保您的電腦已安裝 Python。如果還沒有，可以從 python.org 下載安裝。
2. 安裝必要的工具庫
打開您的終端機（Windows 的 CMD 或 PowerShell，Mac 的 Terminal），執行以下指令來安裝程式需要的工具：
```Bash
pip install requests beautifulsoup4 html5lib
```
3. 下載並修改程式
下載我附上的 web_to_markdown.py。
使用文字編輯器（如記事本、VS Code）打開它。
找到程式末尾的這幾行：

```Python
if __name__ == "__main__":
    # 在這裡更換您想轉換的網頁連結
    url = "https://lotuswithyou.com/publication_issue.php?pgClass=2&pgID=19&pbTopic=history&pID=182"
    # ...
```
將 url 後面的網址換成您想轉換的期數連結 。
4. 執行程式
在終端機中切換到檔案所在的資料夾，執行：
```Bash
python web_to_markdown.py
```
執行結果：
程式會自動在同一個資料夾下生成一個 output.md 檔案。
所有的圖片會自動下載並存放在 images/ 資料夾中。
Markdown 檔案內的圖片連結會自動指向這些本地圖片，方便您離線閱讀。