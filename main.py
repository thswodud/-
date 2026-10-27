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
        ["마감일 빠른 순", "우선순위 높은 순", "최근 등록 순"],
    )

visible_tasks = tasks[:]
if status_filter == "미완료":
    visible_tasks = [task for task in visible_tasks if not task["done"]]
elif status_filter == "완료":
    visible_tasks = [task for task in visible_tasks if task["done"]]

priority_rank = {"높음": 0, "보통": 1, "낮음": 2}
if sort_option == "마감일 빠른 순":
    visible_tasks.sort(key=lambda task: (task["due_date"], task["done"], task["id"]))
elif sort_option == "우선순위 높은 순":
    visible_tasks.sort(key=lambda task: (priority_rank[task["priority"]], task["due_date"]))
else:
    visible_tasks.sort(key=lambda task: task["id"], reverse=True)

if not tasks:
    st.info("아직 등록된 할 일이 없습니다. 위에서 첫 번째 공부 계획을 추가해 보세요.")
elif not visible_tasks:
    st.info("선택한 조건에 해당하는 할 일이 없습니다.")
else:
    today = date.today()

    for task in visible_tasks:
        with st.container(border=True):
            left, middle, right = st.columns([0.12, 3, 1.1])

            with left:
                new_done = st.checkbox(
                    "완료",
                    value=task["done"],
                    key=f"done_{task['id']}",
                    label_visibility="collapsed",
                )
                if new_done != task["done"]:
                    task["done"] = new_done
                    st.rerun()

            with middle:
                if task["done"]:
                    st.markdown(f"~~**{task['title']}**~~")
                else:
                    st.markdown(f"**{task['title']}**")

                st.caption(
                    f"과목: {task['subject']}  ·  마감일: {task['due_date'].strftime('%Y-%m-%d')}  ·  우선순위: {task['priority']}"
                )

                if not task["done"] and task["due_date"] < today:
                    st.warning("마감일이 지났습니다.")
                elif not task["done"] and task["due_date"] == today:
                    st.info("오늘 마감입니다.")

            with right:
                if st.button("🗑️ 삭제", key=f"delete_{task['id']}", use_container_width=True):
                    st.session_state.tasks = [
                        item for item in st.session_state.tasks if item["id"] != task["id"]
                    ]
                    st.rerun()

# ---------- 안내 ----------
with st.expander("ℹ️ 사용 안내 및 데이터 저장 안내"):
    st.markdown(
        """
        1. 제목, 과목, 마감일, 우선순위를 입력한 뒤 **할 일 추가**를 누르세요.
        2. 할 일 왼쪽의 체크박스를 선택하면 완료 상태가 바뀝니다.
        3. 상태별 보기와 정렬 기능으로 목록을 확인할 수 있습니다.
        4. 삭제 버튼을 누르면 해당 할 일이 목록에서 제거됩니다.

        **주의:** 현재 버전은 `st.session_state`를 사용하므로 세션이 초기화되거나 앱이 다시 시작되면 데이터가 사라질 수 있습니다.
        장기간 기록을 보존하려면 파일이나 데이터베이스 저장 기능을 추가해야 합니다.
        """
    )
