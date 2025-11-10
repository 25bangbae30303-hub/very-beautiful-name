import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="울버햄튼 원더러스 팬사이트", page_icon="🐺", layout="wide")

st.title("🐺 울버햄튼 원더러스 팬사이트")
st.markdown("프리미어리그의 **Wolves** 최신 소식과 데이터를 한눈에!")

# 예시 데이터 (실제 API 연동 가능)
data = {
    "선수": ["Pedro Neto", "Matheus Cunha", "Hwang Hee-chan", "João Gomes"],
    "포지션": ["FW", "FW", "FW", "MF"],
    "득점": [3, 4, 6, 1],
}
df = pd.DataFrame(data)

st.subheader("📊 주요 선수 스탯")
st.dataframe(df)

# 팀 뉴스 (예시)
st.subheader("📰 최근 뉴스 (BBC Sport RSS 불러오기)")
rss_url = "https://feeds.bbci.co.uk/sport/football/teams/wolves/rss.xml"
try:
    import feedparser
    feed = feedparser.parse(rss_url)
    for entry in feed.entries[:5]:
        st.markdown(f"- [{entry.title}]({entry.link})")
except Exception as e:
    st.warning("뉴스를 불러오지 못했습니다. 😢")

st.write("---")
st.caption("© 2025 Wolverhampton Wanderers Fan Page | Made with Streamlit")
