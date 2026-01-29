import streamlit as st
from datetime import datetime, timedelta
import time

# --- Danh sách tài khoản ---
accounts = {
    "vsak.scnu": {"password": "1234", "role": "player", "members": {"Quang": "Leader", "Lan": "Support"}},
    "vsak.scnu1": {"password": "1234", "role": "player", "members": {"Hùng": "Leader", "Mai": "Support"}},
    "admin": {"password": "admin123", "role": "admin"}
}

# --- Nhiệm vụ ---
tasks = {
    "Nhiệm vụ 1": {"question": "Thủ đô của Việt Nam là gì?", "answer": "Hà Nội", "code": "CODE123"},
    "Nhiệm vụ 2": {"question": "2 + 2 = ?", "answer": "4", "code": "CODE456"},
    "Nhiệm vụ 3": {"question": "SCNU viết tắt của gì?", "answer": "South China Normal University", "code": "CODE789"}
}

# --- Session state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None
if "codes" not in st.session_state:
    st.session_state.codes = []

# --- Đăng nhập ---
if not st.session_state.logged_in:
    st.title("🎮 Game Event - Đăng nhập")

    username = st.text_input("Tên đăng nhập")
    password = st.text_input("Mật khẩu", type="password")

    if st.button("Vào game"):
        if username in accounts and accounts[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.role = accounts[username]["role"]
            st.session_state.start_time = datetime.now()
            st.success("Đăng nhập thành công!")
        else:
            st.error("Sai tài khoản hoặc mật khẩu")

# --- Trang chủ ---
if st.session_state.logged_in:
    st.title("🏫 Game Event - Trang chủ")
    st.image("campus_map.jpg", caption="Bản đồ khuôn viên trường", width=800)

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    # Nút 1: Tiến trình
    if col1.button("Tiến trình 🎯"):
        st.subheader("Tiến trình nhiệm vụ")
        if st.session_state.codes:
            for code in st.session_state.codes:
                st.write(f"Đã nhận mã: {code}")
        else:
            st.write("Chưa có mã nào, hãy hoàn thành nhiệm vụ!")

    # Nút 2: Danh sách nhiệm vụ
    if col2.button("Danh sách nhiệm vụ 📋"):
        st.subheader("Danh sách nhiệm vụ")
        for name, info in tasks.items():
            st.write(f"{name}: {info['question']}")
            answer = st.text_input(f"Trả lời cho {name}", key=name)
            if answer:
                if answer.strip().lower() == info["answer"].lower():
                    if info["code"] not in st.session_state.codes:
                        st.session_state.codes.append(info["code"])
                    st.success(f"✅ Chính xác! Bạn nhận được mã số: {info['code']}")
                else:
                    st.error("❌ Sai rồi, thử lại nhé!")

    # Nút 3: Danh sách thành viên
    if col3.button("Danh sách thành viên 👥"):
        st.subheader("Thành viên")
        if st.session_state.role == "player":
            members = accounts[st.session_state.user]["members"]
            for name, role in members.items():
                st.write(f"{name} - {role}")
        else:
            st.write("Quản trị viên không có danh sách thành viên riêng.")

    # Nút 4: Giải thưởng
    if col4.button("Giải thưởng 🏅"):
        st.subheader("Thông tin giải thưởng")
        st.write("🥇 Giải nhất: Voucher 1 triệu")
        st.write("🥈 Giải nhì: Sách + Quà lưu niệm")

    # Nút 5: Liên lạc khẩn cấp
    if col5.button("Liên lạc khẩn cấp 📞"):
        st.subheader("Thông tin liên lạc")
        st.write("Hotline: 0123-456-789")
        st.write("Email: event@school.edu")

    # Nút 6: Thời gian
    if col6.button("Thời gian ⏳"):
        st.subheader("Thời gian còn lại")
        deadline = st.session_state.start_time + timedelta(minutes=30)
        placeholder = st.empty()
        progress_bar = st.progress(0)

        total_seconds = int((deadline - st.session_state.start_time).total_seconds())

        while True:
            remaining = deadline - datetime.now()
            if remaining.total_seconds() <= 0:
                placeholder.write("⏰ Hết giờ! Trò chơi kết thúc.")
                progress_bar.progress(100)
                break
            minutes, seconds = divmod(int(remaining.total_seconds()), 60)
            placeholder.write(f"Còn lại: {minutes} phút {seconds} giây")

            elapsed = total_seconds - int(remaining.total_seconds())
            progress = int((elapsed / total_seconds) * 100)
            progress_bar.progress(progress)

            time.sleep(1)

    # Nút Kho báu
    if st.button("Kho báu 🗝️"):
        st.subheader("Mở kho báu cuối cùng")
        code_input = st.text_input("Nhập tất cả mã số (cách nhau bằng dấu phẩy)")
        if code_input:
            codes_entered = [c.strip() for c in code_input.split(",")]
            all_codes = [info["code"] for info in tasks.values()]
            if set(codes_entered) == set(all_codes):
                st.success("🎉 Chúc mừng! Bạn đã mở kho báu thành công!")
            else:
                st.warning("⚠️ Mã số chưa đủ hoặc sai, hãy hoàn thành tất cả nhiệm vụ.")

        # Nút Quản trị (chỉ admin thấy)
    if st.session_state.role == "admin":
        if st.button("Quản trị 🛠️"):
            st.subheader("Tiến độ các đội")

            # Giả sử ta lưu tiến độ của từng đội trong session_state
            # Ở đây demo đơn giản: mỗi đội có danh sách mã số đã nhận
            if "team_progress" not in st.session_state:
                st.session_state.team_progress = {
                    "vsak.scnu": [],
                    "vsak.scnu1": []
                }

            # Hiển thị tiến độ từng đội
            for user, info in accounts.items():
                if info["role"] == "player":
                    codes = st.session_state.team_progress.get(user, [])
                    st.write(f"Đội {user}: đã nhận {len(codes)} mã số")
                    if codes:
                        st.write("Mã số:", ", ".join(codes))
                    else:
                        st.write("Chưa có mã số nào")

            st.info("Quản trị viên có thể theo dõi tiến độ các đội tại đây.")