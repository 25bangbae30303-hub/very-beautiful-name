import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import feedparser

# -------------------------------
# 기본 설정
# -------------------------------
st.set_page_config(page_title="울버햄튼 데이터 대시보드", page_icon="🐺", layout="wide")
st.title("🐺 울버햄튼 원더러스 실시간 대시보드")

# -------------------------------
# Football-Data.org API 설정
# -------------------------------
API_KEY = st.secrets.get("FOOTBALL_DATA_API_KEY", None)
TEAM_ID = 76  # Wolverhampton Wanderers (football-data.org 기준)
COMP_ID = 2021  # Premier League

if not API_KEY:
    st.error("⚠️ Streamlit Secrets에 FOOTBALL_DATA_API_KEY를 등록해주세요.")
    st.stop()

headers = {"X-Auth-Token": API_KEY}

# -------------------------------
# 1️⃣ 팀 정보
# -------------------------------
team_url = f"https://api.football-data.org/v4/teams/{TEAM_ID}"
team = requests.get(team_url, headers=headers).json()

st.sidebar.image(team["crest"], width=100)
st.sidebar.header(team["name"])
st.sidebar.write(f"경기장: {team['venue']}")
st.sidebar.write(f"창단: {team['founded']}")
st.sidebar.write(f"국가: {team['area']['name']}")

# -------------------------------
# 2️⃣ 최근 경기
# -------------------------------
matches_url = f"https://api.football-data.org/v4/teams/{TEAM_ID}/matches?competitions={COMP_ID}&status=FINISHED"
matches = requests.get(matches_url, headers=headers).json()["matches"]

data = []
for m in matches[-10:]:  # 최근 10경기
    home = m["homeTeam"]["shortName"]
    away = m["awayTeam"]["shortName"]
    home_score = m["score"]["fullTime"]["home"]
    away_score = m["score"]["fullTime"]["away"]
    is_home = (home == "Wolves")
    result = (
        "승" if (home_score > away_score and is_home)
        or (away_score > home_score and not is_home)
        else "무" if home_score == away_score else "패"
    )
    data.append({
        "날짜": m["utcDate"][:10],
        "상대팀": away if is_home else home,
        "득점": home_score if is_home else away_score,
        "실점": away_score if is_home else home_score,
        "결과": result
    })

df_matches = pd.DataFrame(data).sort_values("날짜", ascending=False)
st.subheader("📅 최근 경기 결과")
st.dataframe(df_matches, use_container_width=True)

# -------------------------------
# 3️⃣ 득점 추이 시각화
# -------------------------------
st.subheader("📈 득점 추이")
fig = px.line(df_matches.sort_values("날짜"), x="날짜", y="득점",
              markers=True, title="경기별 득점 추이", color_discrete_sequence=["#FDB913"])
st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 4️⃣ 뉴스 섹션 (BBC RSS)
# -------------------------------
st.subheader("📰 최신 뉴스")
rss_url = "https://feeds.bbci.co.uk/sport/football/teams/wolves/rss.xml"
feed = feedparser.parse(rss_url)
for entry in feed.entries[:5]:
    st.markdown(f"- [{entry.title}]({entry.link})")

st.write("---")
st.caption("© 2025 Wolverhampton Wanderers Dashboard | Powered by Football-Data.org & Streamlit 🐺")
