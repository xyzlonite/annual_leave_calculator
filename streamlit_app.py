import datetime
import math

import streamlit as st


def calculate_previous_year_days(start_date):
    # 해당 연도의 마지막 날을 구함
    end_date = datetime.date(start_date.year, 12, 31)

    # 전년도의 마지막 날과 전년도의 첫 날 (또는 입사일) 사이의 일수를 계산
    days_worked_previous_year = (end_date - start_date).days + 1

    print(days_worked_previous_year)

    return days_worked_previous_year


def calculate_leave(start_date):
    today = datetime.date.today()
    employment_years = today.year - start_date.year
    expiration_date = datetime.date(today.year, 12, 31)

    if employment_years == 0:
        # 0년차 연차 계산: 입사 첫 해의 경우, 다음해까지 월차 누적 계산
        months_worked = (today.year - start_date.year) * 12 + today.month - start_date.month
        leave = min(11, months_worked)
        st.write(f"입사 {employment_years + 1}년차이고")
        st.write(f"오늘({today}) 기준 월차 개수는 {leave}일입니다.")
        st.write("해당 월차는 입사 다음년도 12월 31일까지 사용하실 수 있습니다.")
    # elif employment_years == 1:
    #     # 1년차 연차 계산: 해가 바뀌면 1년치만 계산
    #     proportional_leave = math.ceil(((start_date.replace(year=start_date.year + 1) - start_date).days / 365) * 15)
    #     leave = proportional_leave
    #     st.write(f"당신은 {employment_years + 1}년차이고, 연차 개수는 {leave}일 입니다.")
    elif employment_years == 1:
        # 2년차 연차 계산
        # 1년차 연차 계산: 이전해의 월차와 비례 연차가 함께 계산
        previous_year_leave = min(11, 12 - start_date.month)
        current_year_leave = start_date.month - 1
        end_date = datetime.date(start_date.year, 12, 31)
        # 전년도의 마지막 날과 전년도의 첫 날 (또는 입사일) 사이의 일수를 계산
        days_worked_previous_year = (end_date - start_date).days + 1
        proportional_leave = math.ceil(round((days_worked_previous_year / 365) * 15), 1)

        leave = previous_year_leave + current_year_leave + proportional_leave
        st.write(f"당신은 {employment_years + 1}년차이고")
        st.write(f"오늘({today}) 기준 이전해 월차 {previous_year_leave}일, 올해 월차 {current_year_leave}일, 올해 비례 연차 {proportional_leave}일로")
        st.write(f"올해 총 연차는 {leave}일 입니다.")
        st.write(f"연차 만료일은 {expiration_date}입니다.")
        st.markdown("***")
        st.write("비례연차 계산 공식 (전년도 근속일수 / 365 )* 15 한 값에 소수점을 올림한 만큼 지급")
        st.write(
            f"\t전년도 근속일수는 {days_worked_previous_year}일 ({days_worked_previous_year} / 365) * 15 = {round((days_worked_previous_year / 365) * 15, 1)} => {proportional_leave}일"
        )

    else:
        # 3년차 이상 연차 계산: 2년마다 1개의 연차가 추가
        leave = 15 + min(10, (employment_years - 2) // 2)
        st.write(f"당신은 {employment_years + 1}년차이고")
        st.write(f"오늘({today}) 기준 연차 개수는 {leave}일입니다.")
        st.write(f"연차 만료일은 {expiration_date}입니다.")


st.title("이상한마케팅 연차 계산기")
st.text("")

start_date = st.date_input("입사일을 입력해 주세요", datetime.date(2019, 7, 6))
st.markdown("***")

calculate_leave(start_date)
