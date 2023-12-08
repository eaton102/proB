from datetime import datetime, timedelta
import pandas as pd
import pytz
import streamlit as st
import streamlit_calendar as st_calendar

timezone = "Asia/Tokyo"
tz = pytz.timezone(timezone)

dt_now = datetime.now(tz)


def display_task_management_ui():
    st.title("タスク管理アプリ(仮)")

    initialize_session_state()

    col1, col2 = st.columns(2)

    with col1:
        add_task()

    with col2:
        remove_task()

    display_remaining_days()

    option = {"initialView": "multiMonthYear"}
    st_calendar.calendar(events=st.session_state["event_list"], options=option)


def initialize_session_state():
    if 'item_name_1' not in st.session_state:
        st.session_state.item_name_1 = ''

    if 'due_date_1' not in st.session_state:
        st.session_state.due_date_1 = ''

    if 'event_calc_list' not in st.session_state:
        st.session_state["event_calc_list"] = [[], []]

    if 'event_list' not in st.session_state:
        st.session_state["event_list"] = []


def add_task():
    st.session_state.item_name_1 = st.text_input("追加したい予定名", key='item1')
    if st.button('予定を追加', type='primary'):
        if st.session_state.item_name_1 == '':
            st.error('予定名を入力してください')
        else:
            st.session_state['event_calc_list'][0].append(str(st.session_state.item_name_1))
            st.session_state['event_calc_list'][1].append(st.session_state.due_date_1)
            event = {
                'id': '1',
                'title': str(st.session_state.item_name_1),
                'start': str(st.session_state.due_date_1),
            }
            st.session_state["event_list"].append(event)


def remove_task():
    st.session_state.due_date_1 = st.date_input("追加したい予定の期限日", key='limitd1')
    if st.button('予定を削除', type='primary'):
        try:
            event = {
                'id': '1',
                'title': str(st.session_state.item_name_1),
                'start': str(st.session_state.due_date_1),
            }
            st.session_state["event_list"].remove(event)
        except ValueError:
            st.warning('その予定は存在しません')
        else:
            st.session_state['event_calc_list'][0].remove(str(st.session_state.item_name_1))
            st.session_state['event_calc_list'][1].remove(st.session_state.due_date_1)


def display_remaining_days():
    for i in range(len(st.session_state['event_calc_list'][0])):
        date_string = str(st.session_state['event_calc_list'][1][i])
        date_event = datetime.strptime(date_string, '%Y-%m-%d').date()
        datetime_event = tz.localize(datetime.combine(date_event, datetime.min.time()))
        dt_calc = datetime_event - dt_now
        event_name_2 = st.session_state['event_calc_list'][0][i]
        st.sidebar.write(f'予定名:{event_name_2}\n残り日数:{str(dt_calc.days + 1)}')


if __name__ == "__main__":
    display_task_management_ui()
