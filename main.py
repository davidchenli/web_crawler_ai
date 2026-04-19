import pandas as pd

from config import config
from repository import Crawler, Gemini, json_to_dict


def main():
    crawler = Crawler("https://tw.news.yahoo.com/entertainment/archive")
    ai = Gemini(config.gemini_api_key)

    news_list = crawler.get_all_news_list()
    news_df = pd.DataFrame(news_list)
    if not news_list:
        return
    news_content = crawler.run_multithreaded_scraper(news_list)
    print("完成資料爬蟲，開始進行推論...")

    news_ai_content = []
    count = 0
    for x in news_content:
        news = x["content"]
        summary = ai.content_measure(news)
        data_return = json_to_dict(summary)

        if type(data_return) is dict:
            final_dict = data_return.copy()
        elif type(data_return) is str:
            summary = ai.fix_format(data_return)
            data_return_fix = json_to_dict(summary)
            if type(data_return_fix) is dict:
                final_dict = data_return_fix.copy()
            else:
                continue
        else:
            continue
        final_dict["id"] = x["id"]
        news_ai_content.append(final_dict)
        count += 1
        print(f"完成推論 {count}/{len(news_content)}")

    print("完成推論，開始輸出 csv...")
    ai_content_df = pd.DataFrame(news_ai_content)
    news_final_df = news_df.merge(ai_content_df, how="left", on=["id"])

    news_final_df["entity"] = news_final_df["person_or_org"].apply(lambda x: x if x else "NULL")
    news_final_df["concert_related"] = news_final_df["is_concert_related"].astype(bool)
    news_final_df["summary"] = news_final_df["summary"].fillna("NULL")
    news_final_df.drop(columns=["id", "is_concert_related", "person_or_org"]).to_csv(f"./output/{config.filename}")
    return news_final_df


if __name__ == '__main__':
    main()
