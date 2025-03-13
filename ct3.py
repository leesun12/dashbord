import streamlit as st
import pandas as pd
import numpy as np
import json

# 페이지 설정
st.set_page_config(
    page_title="학생 성적 관리 대시보드",
    page_icon="📚",
    layout="wide"
)

# 앱 제목
st.title("📚 학생 성적 관리 대시보드")
st.markdown("학생들의 성적을 관리하고 분석하는 대시보드입니다.")

# 학생 데이터프레임 생성 (요구사항 1)
@st.cache_data
def create_student_data():
    data = {
        '학생 이름': ['김민준', '이서연', '박지호', '최수아', '정도윤', '한예은', '황현우', '송지은'],
        '학년': [1, 2, 3, 1, 2, 3, 2, 1],
        '국어': [85, 92, 78, 96, 88, 77, 82, 94],
        '영어': [92, 88, 76, 94, 85, 75, 79, 91],
        '수학': [78, 95, 65, 92, 90, 68, 85, 79],
        '과학': [90, 84, 72, 88, 95, 70, 78, 86]
    }
    
    # 데이터프레임 생성
    df = pd.DataFrame(data)
    
    # 총점과 평균 점수 계산 (요구사항 3)
    df['총점'] = df['국어'] + df['영어'] + df['수학'] + df['과학']
    df['평균'] = df['총점'] / 4
    
    return df

# 데이터프레임 로드
df = create_student_data()

# 사이드바 - 검색 및 필터링 옵션 (도전 과제)
st.sidebar.header("검색 및 필터링")

# 학생 검색 기능 (도전 과제)
search_name = st.sidebar.text_input("학생 이름 검색")

# 과목 필터링 (도전 과제)
st.sidebar.subheader("과목별 필터링")
selected_subject = st.sidebar.selectbox("과목 선택", ['국어', '영어', '수학', '과학'])

# 평균 기준 필터링 (도전 과제)
filter_option = st.sidebar.radio(
    "필터링 기준",
    ["전체 학생", f"{selected_subject} 평균 이상", f"{selected_subject} 평균 이하"]
)

# 학년 필터링
selected_grade = st.sidebar.multiselect("학년 선택", [1, 2, 3], default=[1, 2, 3])

# 데이터 필터링 적용
filtered_df = df.copy()

# 학년 필터 적용
filtered_df = filtered_df[filtered_df['학년'].isin(selected_grade)]

# 이름 검색 필터 적용
if search_name:
    filtered_df = filtered_df[filtered_df['학생 이름'].str.contains(search_name)]

# 과목 평균 필터 적용
if filter_option != "전체 학생":
    subject_avg = df[selected_subject].mean()
    if "이상" in filter_option:
        filtered_df = filtered_df[filtered_df[selected_subject] >= subject_avg]
    else:
        filtered_df = filtered_df[filtered_df[selected_subject] < subject_avg]

# 메인 컨텐츠 탭 나누기
tabs = st.tabs(["📋 학생 성적", "📊 데이터 분석"])

with tabs[0]:
    # 기본 데이터프레임 표시 (요구사항 2)
    st.subheader("학생 성적 데이터")
    
    # 정렬 옵션
    sort_options = st.radio(
        "정렬 기준",
        ["정렬 없음", "평균 높은 순", "평균 낮은 순"],
        horizontal=True
    )
    
    # 데이터 정렬 (요구사항 4)
    display_df = filtered_df.copy()
    if sort_options == "평균 높은 순":
        display_df = display_df.sort_values(by='평균', ascending=False)
    elif sort_options == "평균 낮은 순":
        display_df = display_df.sort_values(by='평균', ascending=True)
    
    # 데이터프레임 표시
    st.dataframe(display_df, use_container_width=True)
    
    # 필터링 결과 요약
    if len(filtered_df) < len(df):
        st.info(f"검색 결과: 총 {len(filtered_df)}명의 학생이 필터링 조건에 일치합니다.")
    
    # 메트릭 표시 (요구사항 5)
    st.subheader("주요 지표")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="전체 평균 점수",
            value=f"{df['평균'].mean():.2f}"
        )
    
    with col2:
        st.metric(
            label="가장 높은 평균 점수",
            value=f"{df['평균'].max():.2f}",
            delta=f"+ {df['평균'].max() - df['평균'].mean():.2f}"
        )
    
    with col3:
        st.metric(
            label="가장 낮은 평균 점수",
            value=f"{df['평균'].min():.2f}",
            delta=f"- {df['평균'].mean() - df['평균'].min():.2f}"
        )
    
    with col4:
        st.metric(
            label=f"{selected_subject} 과목 평균",
            value=f"{df[selected_subject].mean():.2f}"
        )
    
    # 학생별 총점 데이터 표시 (요구사항 6)
    st.subheader("학생별 총점 데이터")
    
    # 총점 데이터용 데이터프레임 생성
    total_scores_df = df[['학생 이름', '학년', '총점', '평균']].copy()
    
    # 평균 점수 소수점 두 자리까지 표시
    total_scores_df['평균'] = total_scores_df['평균'].round(2)
    
    # 데이터프레임을 테이블로 표시
    st.dataframe(
        total_scores_df,
        column_config={
            "학생 이름": st.column_config.TextColumn("학생 이름"),
            "학년": st.column_config.NumberColumn("학년", format="%d학년"),
            "총점": st.column_config.NumberColumn("총점", format="%d점"),
            "평균": st.column_config.NumberColumn("평균", format="%.2f점"),
        },
        use_container_width=True,
        hide_index=True
    )
    
    # JSON 형식으로도 볼 수 있는 옵션 제공
    with st.expander("JSON 형식으로 보기"):
        total_scores = []
        for index, row in df.iterrows():
            total_scores.append({
                "id": f"student_{index}",
                "name": row['학생 이름'],
                "grade": int(row['학년']),
                "total_score": int(row['총점']),
                "average": float(row['평균'])
            })
        st.json(total_scores)

with tabs[1]:
    st.subheader("성적 분석")
    
    # 과목별 평균 점수
    st.subheader("과목별 평균 점수")
    subject_means = pd.DataFrame({
        '과목': ['국어', '영어', '수학', '과학'],
        '평균 점수': [
            df['국어'].mean(),
            df['영어'].mean(),
            df['수학'].mean(),
            df['과학'].mean()
        ]
    })
    st.bar_chart(subject_means.set_index('과목'), use_container_width=True)
    
    # 학년별 평균 분석
    st.subheader("학년별 평균 성적")
    grade_analysis = df.groupby('학년')[['국어', '영어', '수학', '과학', '평균']].mean().reset_index()
    st.dataframe(grade_analysis.style.highlight_max(axis=0), use_container_width=True)
    
    # 학년별 평균 점수 차트
    st.line_chart(grade_analysis.set_index('학년')[['국어', '영어', '수학', '과학']], use_container_width=True)
    
    # 성적 분포 히스토그램
    st.subheader("성적 분포")
    hist_subject = st.selectbox("과목 선택", ['평균', '국어', '영어', '수학', '과학'])
    
    # 점수 범위를 나누어 히스토그램 데이터 생성 (matplotlib 없이)
    score_ranges = ["0-59", "60-69", "70-79", "80-89", "90-100"]
    score_counts = []
    
    # 각 점수 범위에 속하는 학생 수 계산
    for score_range in score_ranges:
        if score_range == "0-59":
            count = len(df[df[hist_subject] < 60])
        elif score_range == "60-69":
            count = len(df[(df[hist_subject] >= 60) & (df[hist_subject] < 70)])
        elif score_range == "70-79":
            count = len(df[(df[hist_subject] >= 70) & (df[hist_subject] < 80)])
        elif score_range == "80-89":
            count = len(df[(df[hist_subject] >= 80) & (df[hist_subject] < 90)])
        else:  # "90-100"
            count = len(df[df[hist_subject] >= 90])
        score_counts.append(count)
    
    # 히스토그램 표시 (streamlit의 차트 사용)
    hist_df = pd.DataFrame({
        '점수 범위': score_ranges,
        '학생 수': score_counts
    })
    st.bar_chart(hist_df.set_index('점수 범위'))
    
    # 성적 구간별 학생 수
    st.subheader("성적 구간별 학생 수")
    
    # 성적 구간 분류
    def get_grade(score):
        if score >= 90:
            return 'A (90-100)'
        elif score >= 80:
            return 'B (80-89)'
        elif score >= 70:
            return 'C (70-79)'
        elif score >= 60:
            return 'D (60-69)'
        else:
            return 'F (0-59)'
    
    # 각 과목별 성적 등급 계산
    grade_counts = {}
    for subject in ['국어', '영어', '수학', '과학']:
        grade_counts[subject] = df[subject].apply(get_grade).value_counts().to_dict()
    
    # 평균 성적 등급
    grade_counts['평균'] = df['평균'].apply(get_grade).value_counts().to_dict()
    
    # 과목 선택
    grade_subject = st.selectbox("과목 선택", ['평균', '국어', '영어', '수학', '과학'], key='grade_chart')
    
    # 성적 등급 차트 데이터 준비
    grade_labels = ['A (90-100)', 'B (80-89)', 'C (70-79)', 'D (60-69)', 'F (0-59)']
    grade_data = []
    
    for label in grade_labels:
        if label in grade_counts[grade_subject]:
            grade_data.append(grade_counts[grade_subject][label])
        else:
            grade_data.append(0)
    
    # 차트 표시
    grade_chart_data = pd.DataFrame({
        '등급': grade_labels,
        '학생 수': grade_data
    })
    st.bar_chart(grade_chart_data.set_index('등급'), use_container_width=True)

# 푸터
st.markdown("---")
st.caption("© 2023 학생 성적 관리 대시보드 | Streamlit으로 제작되었습니다")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 페이지 설정
st.set_page_config(
    page_title="판매 데이터 시각화",
    page_icon="📊",
    layout="wide"
)

# 앱 제목
st.title("📊 월별 판매 데이터 시각화")
st.markdown("다양한 차트를 통해 판매 데이터를 시각화하는 앱입니다.")

# 1. 데이터프레임 생성 (요구사항 1)
@st.cache_data
def generate_sales_data():
    # 랜덤 시드 설정으로 일관된 데이터 생성
    np.random.seed(42)
    
    # 월별 데이터 생성
    months = [f"{i}월" for i in range(1, 13)]
    
    # 무작위 판매량 생성 (50~200 사이)
    product_a = np.random.randint(50, 201, size=12)
    product_b = np.random.randint(50, 201, size=12)
    product_c = np.random.randint(50, 201, size=12)
    
    # 데이터프레임 생성
    df = pd.DataFrame({
        '월': months,
        '상품A': product_a,
        '상품B': product_b,
        '상품C': product_c
    })
    
    # 무작위 위치 데이터 생성 (한국 지역 위주)
    locations = pd.DataFrame({
        '지역': ['서울', '부산', '인천', '대구', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남'],
        'lat': [37.5665, 35.1796, 37.4563, 35.8714, 35.1595, 36.3504, 35.5384, 36.4800, 37.4138, 37.8228, 36.6357, 36.6588],
        'lon': [126.9780, 129.0756, 126.7052, 128.6014, 126.8526, 127.3845, 129.3114, 127.2890, 127.5183, 128.1555, 127.4914, 126.8000],
        '판매량': np.random.randint(100, 1001, size=12)
    })
    
    return df, locations

# 데이터 생성
sales_df, locations_df = generate_sales_data()

# 사이드바 - 필터링 및 옵션
st.sidebar.header("데이터 필터 및 옵션")

# 제품 선택 (도전 과제)
selected_products = st.sidebar.multiselect(
    "시각화할 제품 선택",
    ["상품A", "상품B", "상품C"],
    default=["상품A", "상품B", "상품C"]
)

# 월 범위 선택 (도전 과제)
months_range = st.sidebar.slider(
    "월 범위 선택",
    1, 12, (1, 12),
    step=1
)

# 선택된 월 범위에 따라 데이터 필터링
filtered_df = sales_df.iloc[(months_range[0]-1):months_range[1]]

# 선택된 제품만 포함하는 데이터프레임 생성
filtered_products_df = filtered_df[['월'] + selected_products]

# 데이터 탭과 시각화 탭 생성
tab1, tab2 = st.tabs(["📋 데이터", "📊 시각화"])

with tab1:
    st.header("판매 데이터")
    st.dataframe(filtered_products_df, use_container_width=True)
    
    # 데이터 요약 정보
    st.subheader("데이터 요약")
    
    # 총 판매량 계산
    total_sales = {}
    for product in selected_products:
        total_sales[product] = filtered_df[product].sum()
    
    # 총 판매량 표시
    col1, col2, col3 = st.columns(3)
    
    for i, (product, sales) in enumerate(total_sales.items()):
        if i == 0:
            col1.metric(f"{product} 총 판매량", f"{sales:,}개")
        elif i == 1:
            col2.metric(f"{product} 총 판매량", f"{sales:,}개")
        else:
            col3.metric(f"{product} 총 판매량", f"{sales:,}개")
    
    # 월별 총 판매량 계산
    filtered_df['월별 총 판매량'] = filtered_df[selected_products].sum(axis=1)
    
    # 상위 판매월 표시
    st.subheader("상위 판매월")
    top_months = filtered_df[['월', '월별 총 판매량']].sort_values('월별 총 판매량', ascending=False).head(3)
    st.dataframe(top_months, use_container_width=True)

with tab2:
    st.header("판매 데이터 시각화")
    
    # 2. 월별 판매량 막대 그래프 (요구사항 2)
    st.subheader("월별 판매량 막대 그래프")
    
    bar_fig = px.bar(
        filtered_products_df, 
        x='월', 
        y=selected_products,
        title='월별 제품 판매량',
        labels={'월': '월', 'value': '판매량', 'variable': '제품'},
        barmode='group'
    )
    
    st.plotly_chart(bar_fig, use_container_width=True)
    
    # 3. 총 판매량 파이 차트 (요구사항 3)
    st.subheader("제품별 총 판매량 파이 차트")
    
    # 총 판매량 계산
    total_by_product = {}
    for product in selected_products:
        total_by_product[product] = filtered_df[product].sum()
    
    # 파이 차트 생성
    pie_fig = px.pie(
        values=list(total_by_product.values()),
        names=list(total_by_product.keys()),
        title='제품별 총 판매량 비중',
        hole=0.3,
    )
    
    st.plotly_chart(pie_fig, use_container_width=True)
    
    # 4. 월별 판매 트렌드 선 그래프 (요구사항 4)
    st.subheader("월별 판매 트렌드")
    
    line_fig = px.line(
        filtered_products_df, 
        x='월', 
        y=selected_products,
        title='월별 판매 추이',
        labels={'월': '월', 'value': '판매량', 'variable': '제품'},
        markers=True,
        line_shape='linear'
    )
    
    st.plotly_chart(line_fig, use_container_width=True)
    
    # 5. 제품 간 상관관계 산점도 (요구사항 5)
    if len(selected_products) >= 2:
        st.subheader("제품 간 상관관계 산점도")
        
        # 산점도에 사용할 두 제품 선택
        scatter_col1, scatter_col2 = st.columns(2)
        
        with scatter_col1:
            x_product = st.selectbox("X축 제품", selected_products, index=0)
        
        with scatter_col2:
            # x_product와 다른 제품을 y축 기본값으로 설정
            default_y_index = 1 if selected_products[0] == x_product else 0
            y_product = st.selectbox("Y축 제품", selected_products, index=default_y_index)
        
        # 산점도 생성
        scatter_fig = px.scatter(
            filtered_df, 
            x=x_product, 
            y=y_product,
            trendline="ols",  # 추세선 추가
            title=f'{x_product}와 {y_product} 판매량 상관관계',
            labels={x_product: f'{x_product} 판매량', y_product: f'{y_product} 판매량'},
            hover_data=['월']  # 호버 시 월 정보 표시
        )
        
        # 상관계수 계산
        correlation = filtered_df[x_product].corr(filtered_df[y_product])
        scatter_fig.add_annotation(
            x=0.95, y=0.05,
            xref="paper", yref="paper",
            text=f"상관계수: {correlation:.2f}",
            showarrow=False,
            font=dict(size=12),
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="black",
            borderwidth=1,
            borderpad=4
        )
        
        st.plotly_chart(scatter_fig, use_container_width=True)
    else:
        st.warning("산점도를 표시하려면 최소 2개 이상의 제품을 선택하세요.")
    
    # 6. 판매 위치 지도 시각화 (요구사항 6)
    st.subheader("지역별 판매 위치")
    
    map_fig = px.scatter_mapbox(
        locations_df, 
        lat="lat", 
        lon="lon", 
        hover_name="지역", 
        size="판매량",
        color="판매량",
        color_continuous_scale=px.colors.cyclical.IceFire,
        zoom=6,
        mapbox_style="carto-positron",
        title="지역별 판매량"
    )
    
    st.plotly_chart(map_fig, use_container_width=True)

# 추가 분석 - 제품 비교 히트맵
st.header("추가 분석: 월별 제품 판매 비교")

if len(selected_products) >= 2:
    # 히트맵 생성
    heatmap_data = filtered_df.pivot_table(
        index='월', 
        values=selected_products
    )
    
    heatmap_fig = px.imshow(
        heatmap_data,
        title="월별 제품 판매량 히트맵",
        labels=dict(x="제품", y="월", color="판매량"),
        color_continuous_scale="Viridis",
        aspect="auto"
    )
    
    st.plotly_chart(heatmap_fig, use_container_width=True)
else:
    st.warning("히트맵을 표시하려면 최소 2개 이상의 제품을 선택하세요.")

# 푸터
st.markdown("---")
st.caption("© 멋쟁이사자처럼")   
