import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import feedparser

# -------------------------------
# 기본 설정
# -------------------------------
st.set_page_config(page_title="울버햄튼 원더러스 대시보드", page_icon="🐺", layout="wide")
st.title("🐺 울버햄튼 원더러스 데이터 대시보드")
st.markdown("### Premier League 2024/25 시즌 통계 (비공식 예시 데이터)")

# -------------------------------
# 1️⃣ 시즌 개요
# -------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("리그 순위", "11위")
col2.metric("승", "5")
col3.metric("무", "4")
col4.metric("패", "6")

# -------------------------------
# 2️⃣ 최근 경기 데이터 (예시)
# -------------------------------
matches = pd.DataFrame({
    "날짜": ["2025-10-25", "2025-11-02", "2025-11-09"],
    "상대팀": ["Man United", "Everton", "Newcastle"],
    "결과": ["2-1 승", "1-1 무", "0-2 패"],
    "득점": [2, 1, 0],
    "실점": [1, 1, 2],
})
st.subheader("📅 최근 경기 결과")
st.dataframe(matches, use_container_width=True)

# -------------------------------
# 3️⃣ 득점 추이 그래프
# -------------------------------
st.subheader("📈 경기별 득점 추이")
fig = px.line(matches, x="날짜", y="득점", markers=True, title="득점 변화")
st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 4️⃣ 주요 선수 통계 (예시)
# -------------------------------
players = pd.DataFrame({
    "선수": ["Pedro Neto", "Matheus Cunha", "Hwang Hee-chan", "João Gomes"],
    "득점": [3, 4, 6, 1],
    "어시스트": [2, 3, 1, 1],
})
st.subheader("👕 주요 선수 스탯")
st.dataframe(players, use_container_width=True)

fig2 = px.bar(players, x="선수", y="득점", color="선수", title="선수별 득점 현황")
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# 5️⃣ 최신 뉴스 (BBC RSS)
# -------------------------------
st.subheader("📰 최신 팀 뉴스")
rss_url = "https://feeds.bbci.co.uk/sport/football/teams/wolves/rss.xml"
feed = feedparser.parse(rss_url)
for entry in feed.entries[:5]:
    st.markdown(f"- [{entry.title}]({entry.link})")

# -------------------------------
# 푸터
# -------------------------------
st.write("---")
st.caption("© 2025 Wolverhampton Wanderers Data Dashboard | Made with Streamlit 🐺")

