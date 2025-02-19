import streamlit as st
import json
import os

# 데이터 저장할 파일 경로
DATA_FILE = "students.json"

# 파일에서 데이터 불러오기
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# 파일에 데이터 저장하기
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 세션 상태에 학생 리스트 로드
if "students" not in st.session_state:
    st.session_state["students"] = load_data()

st.info("명령어 양식: '/[추가,제거,변경].[이름].[보충수업 ex/ -3, +1]'")

chat = st.chat_input("명령어를 입력하세요")

if chat:
    commend = chat.split(".")
    
    if len(commend) == 3:
        action, name, time = commend
        try:
            time = int(time)
        except ValueError:
            st.error("보충시간은 숫자로 입력해야 합니다.")
        else:
            if action == "/추가":
                # 중복 확인
                existing_student = next((s for s in st.session_state["students"] if s["이름"] == name), None)
                if existing_student:
                    st.warning(f"{name} 학생은 이미 존재합니다. '/변경'을 사용하세요.")
                else:
                    st.session_state["students"].append({"이름": name, "보충시간": time})
                    save_data(st.session_state["students"])  # 변경사항 저장
                    st.success(f"{name} 학생이 추가되었습니다! (보충시간: {time}시간)")

            elif action == "/변경":
                found = False
                for student in st.session_state["students"]:
                    if student["이름"] == name:
                        student["보충시간"] += time
                        found = True
                        save_data(st.session_state["students"])  # 변경사항 저장
                        st.success(f"{name} 학생의 보충시간이 변경되었습니다! (현재: {student['보충시간']}시간)")
                        break
                if not found:
                    st.warning(f"{name} 학생을 찾을 수 없습니다. '/추가'로 등록하세요.")

            elif action == "/제거":
                original_length = len(st.session_state["students"])
                st.session_state["students"] = [s for s in st.session_state["students"] if s["이름"] != name]

                # 데이터 변경 후 저장
                if len(st.session_state["students"]) < original_length:
                    save_data(st.session_state["students"])  # 변경사항 저장
                    st.success(f"{name} 학생이 제거되었습니다!")
                else:
                    st.warning(f"{name} 학생을 찾을 수 없습니다.")

            else:
                st.error("알 수 없는 명령어입니다. '/추가', '/변경', '/제거'만 사용 가능합니다.")
    else:
        st.error("올바른 형식으로 입력하세요: '/추가.이름.보충시간'")

# 학생 목록 출력
if st.session_state["students"]:
    st.write("### 학생 목록")
    st.table(st.session_state["students"])
else:
    st.write("학생 목록이 비어 있습니다.")
