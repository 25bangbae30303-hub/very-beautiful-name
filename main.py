import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import feedparser

# -------------------------------
# 1️⃣ 기본 설정
# -------------------------------
st.set_page_config(
    page_title="울버햄튼 데이터 대시보드",
    page_icon="🐺",
    layout="wide"
)
st.title("🐺 울버햄튼 원더러스 실시간 대시보드")

# -------------------------------
# 2️⃣ API 설정
# -------------------------------
API_KEY = st.secrets.get("FOOTBALL_DATA_API_KEY")
COMP_ID = 2021  # Premier League

if not API_KEY:
    st.error("⚠️ Streamlit Secrets에 FOOTBALL_DATA_API_KEY를 등록해주세요.")
    st.stop()

HEADERS = {"X-Auth-Token": API_KEY}

# -------------------------------
# 3️⃣ 팀 정보 가져오기
# -------------------------------
try:
    teams_resp = requests.get("https://api.football-data.org/v4/teams", headers=HEADERS, timeout=10)
    teams_resp.raise_for_status()
    teams_data = teams_resp.json()["teams"]
except Exception as e:
    st.error(f"팀 정보를 불러오지 못했습니다: {e}")
    st.stop()

# 울버햄튼 팀 찾기
wolves_team = next((t for t in teams_data if "Wolverhampton" in t["name"]), None)
if not wolves_team:
    st.error("울버햄튼 팀 정보를 찾을 수 없습니다.")
    st.stop()

TEAM_ID = wolves_team["id"]

st.sidebar.image(wolves_team["crest"], width=100)
st.sidebar.header(wolves_team["name"])
st.sidebar.write(f"경기장: {wolves_team.get('venue','N/A')}")
st.sidebar.write(f"창단: {wolves_team.get('founded','N/A')}")
st.sidebar.write(f"국가: {wolves_team['area']['name']}")

# -------------------------------
# 4️⃣ 최근 경기 가져오기
# -------------------------------
try:
    matches_resp = requests.get(
        f"https://api.football-data.org/v4/teams/{TEAM_ID}/matches?status=FINISHED&limit=10",
        headers=HEADERS,
        timeout=10
    )
    matches_resp.raise_for_status()
    matches_json = matches_resp.json()
    matches = matches_json.get("matches", [])
except Exception as e:
    st.error(f"경기 데이터를 불러오지 못했습니다: {e}")
    matches = []

if matches:
    match_list = []
    for m in matches:
        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]
        home_score = m["score"]["fullTime"]["home"]
        away_score = m["score"]["fullTime"]["away"]

        if home == wolves_team["name"]:
            is_home = True
            opponent = away
            goals_for = home_score
            goals_against = away_score
        else:
            is_home = False
            opponent = home
            goals_for = away_score
            goals_against = home_score

        if goals_for > goals_against:
            result = "승"
        elif goals_for == goals_against:
            result = "무"
        else:
            result = "패"

        match_list.append({
            "날짜": m["utcDate"][:10],
            "상대팀": opponent,
            "득점": goals_for,
            "실점": goals_against,
            "결과": result
        })

    df_matches = pd.DataFrame(match_list).sort_values("날짜", ascending=False)
    st.subheader("📅 최근 경기 결과")
    st.dataframe(df_matches, use_container_width=True)

    # -------------------------------
    # 5️⃣ 득점 추이 시각화
    # -------------------------------
    st.subheader("📈 경기별 득점 추이")
    fig = px.line(
        df_matches.sort_values("날짜"),
        x="날짜",
        y="득점",
        markers=True,
        title="경기별 득점 추이",
        color_discrete_sequence=["#FDB913"]
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("최근 경기 데이터가 없습니다.")

# -------------------------------
# 6️⃣ 최신 뉴스
# -------------------------------
st.subheader("📰 최신 팀 뉴스")
rss_url = "https://feeds.bbci.co.uk/sport/football/teams/wolves/rss.xml"
try:
    feed = feedparser.parse(rss_url)
    for entry in feed.entries[:5]:
        st.markdown(f"- [{entry.title}]({entry.link})")
except Exception as e:
    st.warning(f"뉴스를 불러오지 못했습니다: {e}")

# -------------------------------
# 7️⃣ 푸터
# -------------------------------
st.write("---")
st.caption("© 2025 Wolverhampton Wanderers Dashboard | Powered by Football-Data.org & Streamlit 🐺")
