import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 전처리: Pandas 내장 .str 메서드를 사용하여 문자열 안전하게 분리
    df['genre'] = df['genre'].astype(str).str.split('|').str[0].str.strip()
    
    # 개봉일(openDt)에서 개봉 월 추출 (예: 20230115 -> 1월)
    df['open_month'] = pd.to_datetime(df['openDt'].astype(str), format='%Y%m%d', errors='coerce').dt.month
    return df

df = load_data()

# 앱 제목
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown("---")

# ---------------------------------------------------------
# 1. 장르별 영화 편수 (도넛 그래프)
# ---------------------------------------------------------
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 영화 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

# Plotly 도넛 그래프 생성
fig1 = px.pie(
    genre_counts,
    names='genre',
    values='count',
    hole=0.4,
    title="장르별 영화 비율 및 편수"
)

# 마우스 오버 시 편수와 비율이 함께 표시되도록 설정
fig1.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>장르: %{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}"
)

# 그래프 출력
st.plotly_chart(fig1, use_container_width=True)

# 그래프 해석 안내 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 특정 장르가 전체 개봉 영화 중 어느 정도의 비중을 차지하며, 가장 제작 및 개봉이 활발한 주요 장르가 무엇인지 한눈에 파악할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 2. 장르 및 영화별 총 관객 수 (트리맵)
# ---------------------------------------------------------
st.subheader("2. 장르-영화별 총 관객 수 구조")

# 트리맵 오류 방지를 위한 데이터 재그룹화 (장르, 영화명 기준 합계)
treemap_df = df.groupby(['genre', 'movieNm'], as_index=False)['total_audi'].sum()

# Plotly 트리맵 그래프 생성
fig2 = px.treemap(
    treemap_df,
    path=['genre', 'movieNm'],
    values='total_audi',
    title="장르 및 영화별 총 관객 수 분포",
    color='genre'
)

# 마우스 오버 시 영화명과 총 관객 수가 보이도록 설정
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,.0f}명"
)

# 그래프 출력
st.plotly_chart(fig2, use_container_width=True)

# 그래프 해석 안내 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 장르별 전체 흥행 파이의 크기와 함께, 특정 장르 내에서 흥행을 견인한 대표 개별 영화가 무엇인지 비교 분석할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 3. 총 관객 수 분포 (히스토그램)
# ---------------------------------------------------------
st.subheader("3. 총 관객 수 분포")

# 히스토그램 생성
fig3 = px.histogram(
    df,
    x='total_audi',
    nbins=30,
    title="총 관객 수 분포 히스토그램",
    labels={'total_audi': '총 관객 수 (명)'}
)

fig3.update_traces(
    hovertemplate="<b>관객 수 구간: %{x:,.0f}명</b><br>영화 수: %{y}편"
)

fig3.update_layout(
    yaxis_title="영화 수 (편)"
)

# 그래프 출력
st.plotly_chart(fig3, use_container_width=True)

# 데이터 기반 문구 자동 계산
max_audi_row = df.loc[df['total_audi'].idxmax()]
top_movie_name = max_audi_row['movieNm']
top_movie_audi = max_audi_row['total_audi']

# 그래프 해석 및 주요 분석 문구 출력
st.info(
    f"💡 **이 그래프로 알 수 있는 것:** 대부분의 영화는 관객 수가 적은 구간(하위 구간)에 집중되어 있는 오른쪽으로 긴 꼬리를 가진(Right-skewed) 분포를 보입니다.\n\n"
    f"🏆 **가장 관객 수가 많은 영화:** **'{top_movie_name}'** ({top_movie_audi:,.0f}명)"
)

st.markdown("---")

# ---------------------------------------------------------
# 4. 개봉일 스크린수와 총 관객 수의 관계 (산점도)
# ---------------------------------------------------------
st.subheader("4. 개봉일 스크린수 vs 총 관객 수")

# 산점도 생성
fig4 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린수와 총 관객 수의 상관관계",
    labels={
        'first_scrn': '개봉일 스크린수 (개)',
        'total_audi': '총 관객 수 (명)',
        'genre': '장르'
    }
)

fig4.update_traces(
    hovertemplate="<b>영화명: %{hovertext}</b><br>개봉일 스크린수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명"
)

# 그래프 출력
st.plotly_chart(fig4, use_container_width=True)

# 그래프 해석 안내 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 초기 스크린 확보 수와 최종 총 관객 수 간의 양의 상관관계를 확인할 수 있으며, 초기 스크린수 대비 뛰어난 흥행을 기록한 효율적인 영화들도 파악할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 5. 주요 장르별 총 관객 수 분포 (박스플롯)
# ---------------------------------------------------------
st.subheader("5. 주요 장르별 총 관객 수 분포 (영화 10편 이상)")

# 영화 수 10편 이상인 장르 필터링
genre_counts_series = df['genre'].value_counts()
top_genres = genre_counts_series[genre_counts_series >= 10].index
filtered_df = df[df['genre'].isin(top_genres)]

# 박스플롯 생성
fig5 = px.box(
    filtered_df,
    x='genre',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    points="outliers",  # 이상치(outlier) 점만 표시
    title="주요 장르별 총 관객 수 분포 비교",
    labels={
        'genre': '장르',
        'total_audi': '총 관객 수 (명)'
    }
)

fig5.update_traces(
    hovertemplate="<b>영화명: %{hovertext}</b><br>총 관객 수: %{y:,.0f}명"
)

# 그래프 출력
st.plotly_chart(fig5, use_container_width=True)

# 그래프 해석 안내 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 주요 장르별 관객 수의 중앙값과 편차를 비교할 수 있으며, 박스 밖으로 튀어나온 이상치(Outlier) 점을 통해 장르 평균을 훨씬 뛰어넘은 괄목할 만한 흥행작을 확인할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 6. 스크린수, 총 관객 수, 첫 주 관객 수 (버블 차트)
# ---------------------------------------------------------
st.subheader("6. 개봉일 스크린수 vs 총 관객 수 (원 크기: 첫 주 관객 수)")

# 버블 차트 생성
fig6 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='genre',
    hover_name='movieNm',
    size_max=50,  # 버블 최대 크기 지정
    title="개봉일 스크린수, 총 관객 수 및 첫 주 관객 수의 다차원 관계",
    labels={
        'first_scrn': '개봉일 스크린수 (개)',
        'total_audi': '총 관객 수 (명)',
        'first_week_audi': '개봉 첫 주 관객 수 (명)',
        'genre': '장르'
    }
)

fig6.update_traces(
    hovertemplate="<b>영화명: %{hovertext}</b><br>개봉일 스크린수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명<br>첫 주 관객 수: %{marker.size:,.0f}명"
)

# 그래프 출력
st.plotly_chart(fig6, use_container_width=True)

# 그래프 해석 안내 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린수와 총 관객 수 외에도, 버블 크기(첫 주 관객 수)를 추가하여 초반 흥행 선전 여부와 장기 흥행(입소문 효과)에 성공한 영화의 차이를 종합적으로 비교해 볼 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 7. 국가 및 장르별 영화 편수 (선버스트 차트)
# ---------------------------------------------------------
st.subheader("7. 국가-장르별 영화 편수 구조")

# 선버스트 차트에 사용할 편수 데이터 집계
sunburst_df = df.groupby(['nation', 'genre']).size().reset_index(name='count')

# 선버스트 차트 생성
fig7 = px.sunburst(
    sunburst_df,
    path=['nation', 'genre'],
    values='count',
    title="제작 국가 및 장르별 영화 편수 비율",
    color='nation'
)

fig7.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편"
)

# 그래프 출력
st.plotly_chart(fig7, use_container_width=True)

# 그래프 해석 안내 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 국가별 전체 영화 제작 비중과 더불어 각 국가 내부에서 어떤 장르가 주를 이루는지 계층 구조 형태로 직관적 파악이 가능합니다.")

st.markdown("---")

# ---------------------------------------------------------
# 8. 개봉 월별 평균 10위권 체류 일수 (막대그래프)
# ---------------------------------------------------------
st.subheader("8. 개봉 월에 따라 10위권에 오래 머무는 기간이 달라질까?")

# 개봉 월별 평균 10위권 체류 일수 집계
month_df = df.dropna(subset=['open_month']).groupby('open_month', as_index=False)['days_in_top10'].mean()
month_df['open_month'] = month_df['open_month'].astype(int).astype(str) + "월"

# 막대그래프 생성
fig8 = px.bar(
    month_df,
    x='open_month',
    y='days_in_top10',
    title="개봉 월에 따라 10위권에 오래 머무는 기간이 달라질까?",
    labels={
        'open_month': '개봉 월',
        'days_in_top10': '평균 10위권 체류 일수 (일)'
    },
    color='days_in_top10',
    color_continuous_scale='Viridis'
)

fig8.update_traces(
    hovertemplate="<b>개봉 월: %{x}</b><br>평균 10위권 체류 일수: %{y:.1f}일"
)

fig8.update_layout(
    xaxis={'categoryorder': 'array', 'categoryarray': [f"{i}월" for i in range(1, 13)]}
)

# 그래프 출력
st.plotly_chart(fig8, use_container_width=True)

# 그래프 해석 안내 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 영화가 개봉한 월(계절성)에 따라 박스오피스 상위권(10위권)을 오랫동안 유지하며 장기 흥행하는 경향이 달라지는지 확인할 수 있습니다.")

st.markdown("---")
