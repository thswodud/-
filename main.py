import streamlit as st
from datetime import date, datetime

st.set_page_config(
    page_title="공부 계획 & 할 일 관리",
    page_icon="📚",
    layout="wide",
)

st.title("📚 공부 계획 및 할 일 관리")
st.caption("할 일을 정리하고, 완료 상태와 학습 진행률을 한눈에 확인하세요.")

# Streamlit 세션이 유지되는 동안 할 일 목록을 저장합니다.
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "next_task_id" not in st.session_state:
    st.session_state.next_task_id = 1

SUBJECTS = ["국어", "영어", "수학", "사회", "과학", "정보", "기타"]
PRIORITIES = ["높음", "보통", "낮음"]

# ---------- 새 할 일 등록 ----------
st.subheader("➕ 새 공부 계획 등록")

with st.form("add_task_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        task_title = st.text_input(
            "할 일 제목",
            placeholder="예: 수학 문제집 20문제 풀기",
            max_chars=100,
        )
    with col2:
        subject = st.selectbox("과목", SUBJECTS)

    col3, col4 = st.columns(2)
    with col3:
        due_date = st.date_input("마감일", value=date.today())
    with col4:
        priority = st.selectbox("우선순위", PRIORITIES, index=1)

    submitted = st.form_submit_button("할 일 추가", type="primary", use_container_width=True)

    if submitted:
        cleaned_title = task_title.strip()
        if not cleaned_title:
            st.error("할 일 제목을 입력해 주세요.")
        else:
            st.session_state.tasks.append(
                {
                    "id": st.session_state.next_task_id,
                    "title": cleaned_title,
                    "subject": subject,
                    "due_date": due_date,
                    "priority": priority,
                    "done": False,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
            )
            st.session_state.next_task_id += 1
            st.success("할 일이 추가되었습니다.")
            st.rerun()

st.divider()

# ---------- 통계 ----------
tasks = st.session_state.tasks
total_count = len(tasks)
done_count = sum(1 for task in tasks if task["done"])
remaining_count = total_count - done_count
progress = done_count / total_count if total_count else 0.0

metric1, metric2, metric3 = st.columns(3)
metric1.metric("전체 할 일", f"{total_count}개")
metric2.metric("완료한 할 일", f"{done_count}개")
metric3.metric("남은 할 일", f"{remaining_count}개")

st.write("**전체 학습 진행률**")
st.progress(progress)
st.caption(f"{progress * 100:.0f}% 완료")

st.divider()

# ---------- 목록 조회 및 필터 ----------
st.subheader("📝 내 공부 계획")

filter_col, sort_col = st.columns([1, 1])
with filter_col:
    status_filter = st.selectbox(
        "상태별 보기",
        ["전체", "미완료", "완료"],
    )
with sort_col:
    sort_option = st.selectbox(
        "정렬",
