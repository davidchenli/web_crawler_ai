import time

from google import genai


# 初始化客戶端


class Gemini:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemma-3-1b-it'

    def ask_gemini(self, prompt_text):
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt_text
        )
        time.sleep(2)
        return response.text

    def content_measure(self, news):
        prompt = f'''
            你是一位網路輿情監控專家。請分析以下新聞內容並提取資訊。

            ### 新聞內容 ###
            <news_content>
            {news}
            </news_content>

            ### 處理規則 ###
            1. 忽略「更多報導、延伸閱讀」等垃圾資訊。
            2. summary: 提取新聞大意，不超過 100 字。
            3. person_or_org: 僅提取「人名」或「團體名」。排除地點、稱謂、活動名。若無則回傳空字串。如果有多個用,分開
            4. is_concert_related: 判斷是否提及演唱會、巡演、見面會、演出售票。

            ### 輸出規範 ###
            請務必以 JSON 格式輸出，且必須包含以下 key: "summary", "person_or_org", "is_concert_related"。
            '''
        return self.ask_gemini(prompt)

    def fix_format(self, json_str):
        prompt = f'''
            你是一位嚴謹的資料工程師。你的任務是修復毀損或格式不正確的 Python Dict 格式字串。

            ### 範例 ###
            輸入: "這則新聞的大意是... [{{summary: '...'}}]" (錯誤格式)
            輸出: {{"summary": "...", "entity": "...", "concert": false}}

            ### 待修復資料 ###
            {json_str}

            ### 指令 ###
            1. 確保所有的 Key 為雙引號。
            2. 確保 Bool 值為標準 Python 格式 (True/False)。
            3. 僅輸出修復後的內容，嚴禁任何解釋。
            '''
        return self.ask_gemini(prompt)
