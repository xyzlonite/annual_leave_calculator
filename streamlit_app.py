import datetime
import math

import pandas as pd
import streamlit as st


def calculate_fixed_leave(employment_years):
    # 연차 계산
    leave = 15 + min(10, (employment_years - 2) // 2)

    return leave


def print_leave_table(employment_date, start_year, end_year):
    # 연차 계산 및 DataFrame 생성
    data = []
    for i in range(start_year, end_year + 1):
        leave = calculate_fixed_leave(i)
        start_date_of_leave = datetime.date(employment_date.year + i, 1, 1)
        end_date_of_leave = datetime.date(employment_date.year + i, 12, 31)
        data.append({"년차": i + 1, "연차 시작일": start_date_of_leave, "연차개수": leave, "연차 만료일": end_date_of_leave})
    df = pd.DataFrame(data)

    # DataFrame을 HTML로 변환하고 모든 데이터를 가운데 정렬
    df_html = df.to_html(classes="table table-striped", index=False)
    df_html = df_html.replace("<table", '<table style="text-align:center;"')

    # DataFrame 출력
    st.markdown(df_html, unsafe_allow_html=True)


def print_leave(data):
    # DataFrame을 HTML로 변환하고 모든 데이터를 가운데 정렬
    data_html = data.to_html(classes="table table-striped", index=False)

    # HTML에서 td와 th 요소를 가운데 정렬하는 CSS 추가
    data_html = data_html.replace("<table", '<table style="text-align:center;"')

    # DataFrame 출력
    st.markdown(data_html, unsafe_allow_html=True)


def calculate_leave(employment_date):
    # 각 변수를 초기화
    today = datetime.date.today()
    employment_years = today.year - employment_date.year
    start_date = datetime.date(today.year, 1, 1)
    expiration_date = datetime.date(today.year, 12, 31)
    leave = 0

    # 각 년차에 따라 연차 계산
    if employment_years == 0:
        months_worked = (today.year - employment_date.year) * 12 + today.month - employment_date.month
        leave = min(11, months_worked)

        st.write(f"당신은 {employment_years + 1}년차이입니다.")
        # 연차 계산 결과를 DataFrame에 저장
        data = pd.DataFrame({"년차": [employment_years + 1], "월차 시작일": [employment_date], "월차개수": [leave], "월차만료일": [expiration_date]})
        st.text("[올해 사용가능한 연차]")
        print_leave(data)

    elif employment_years == 1:
        # last_date = datetime.date(start_date.year - 1, start_date.month, start_date.day)
        previous_year_leave = min(11, 12 - employment_date.month)
        current_year_leave = employment_date.month - 1
        end_date = datetime.date(employment_date.year, 12, 31)
        days_worked_previous_year = (end_date - employment_date).days + 1
        proportional_leave = math.ceil(round((days_worked_previous_year / 365) * 15, 1))

        leave = current_year_leave + proportional_leave

        st.write(f"당신은 {employment_years + 1}년차입니다.")

        data = pd.DataFrame({"년차": [employment_years], "월차 시작일": [employment_date], "월차개수": [previous_year_leave], "연차만료일": [expiration_date]})

        st.text("[올해 사용가능한 연차]")
        print_leave(data)

        data = pd.DataFrame({"년차": [employment_years + 1], "연차 시작일": [start_date], "연차개수": [leave], "연차만료일": [expiration_date]})

        print_leave(data)

    else:
        leave = 15 + min(10, (employment_years - 2) // 2)

        st.write(f"당신은 {employment_years + 1}년차입니다.")

        # 연차 계산 결과를 DataFrame에 저장
        data = pd.DataFrame({"년차": [employment_years + 1], "연차 시작일": [start_date], "연차개수": [leave], "연차만료일": [expiration_date]})

        print_leave(data)


st.title("이상한마케팅 연차 계산기")
st.text("")

employment_date = st.date_input("입사일을 입력해 주세요", datetime.date(2022, 1, 1))
st.markdown("***")

calculate_leave(employment_date)

st.markdown("***")
st.write("[연차 기준]")
st.write("- 연차 : 입사 1년차 미만의 월차 발생을 제외하고는 모두 1월 1일에 발생 / 당해 연도 12월 31일까지 사용가능")
st.write("- 월차 : 입사 1년차 미만의 입사일 기준 한 달 만근 시 월차 1일 발생 / 익년도(월차가 지급된 기준) 12월 31일까지 사용가능")

st.markdown("***")
st.write("[연차별 발생 기준]")
st.write("- 1년차의 경우 : 1달 만근 시 1개의 월차 생성(최대 11개)")
st.write("- 2년차의 경우 : 입사일 기준 1년까지 만근 시 월차 발생 + 비례연차 발생(전년도 근속일수 / 365 * 15 한 값에 소수점을 올림한 만큼 지급)")
st.write("- 3년차의 경우 : 입사일 기점으로 15개의 연차 부여")
st.write("- 4년차 이상의 경우 : 2년마다 1개의 연차가 추가(최대 25개까지 부여)")

st.markdown("***")
st.text("")

# 함수 호출: 3년차부터 10년차까지의 연차를 계산하고 출력
st.text("[앞으로 사용가능한 연차]")

print_leave_table(employment_date, 2, 30)
