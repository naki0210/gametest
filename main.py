import streamlit as st
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="Game Chấm Tròn - Điều khiển bằng chuột", layout="centered")
st.title("Game Chấm Tròn - Điều khiển bằng chuột")

CANVAS_SIZE = 500

if "player_x" not in st.session_state:
    st.session_state.player_x = CANVAS_SIZE // 2
    st.session_state.player_y = CANVAS_SIZE // 2
    st.session_state.player_size = 25
    st.session_state.score = 0
    st.session_state.foods = [
        {"x": random.randint(20, CANVAS_SIZE-20), "y": random.randint(20, CANVAS_SIZE-20)}
        for _ in range(10)
    ]

st.write(f"Điểm số: {st.session_state.score}")
st.write(f"Kích thước nhân vật: {st.session_state.player_size}")

# Vẽ game bằng matplotlib
fig, ax = plt.subplots(figsize=(5, 5))
ax.set_xlim(0, CANVAS_SIZE)
ax.set_ylim(0, CANVAS_SIZE)

# Vẽ mồi
for f in st.session_state.foods:
    food = plt.Circle((f["x"], f["y"]), 10, color="red")
    ax.add_patch(food)
# Vẽ nhân vật
player = plt.Circle((st.session_state.player_x, st.session_state.player_y), st.session_state.player_size, color="green")
ax.add_patch(player)
ax.axis("off")
st.write("Click vào bản đồ để di chuyển nhân vật đến vị trí chuột!")

# Nhận sự kiện click chuột
clicked = st.pyplot(fig, use_container_width=False)

# Hiện tại, Streamlit không hỗ trợ lắng nghe trực tiếp tọa độ click trên matplotlib.
# → Giải pháp: Dùng st.plotly_chart (Plotly) hoặc streamlit-drawable-canvas để lấy tọa độ click!

from streamlit_drawable_canvas import st_canvas

canvas_result = st_canvas(
    fill_color="rgba(0, 255, 0, 0.3)",
    stroke_width=1,
    background_color="#F6FBFF",
    update_streamlit=True,
    height=CANVAS_SIZE,
    width=CANVAS_SIZE,
    drawing_mode="point",
    key="canvas",
)

if canvas_result.json_data is not None:
    # Lấy điểm click cuối cùng
    if len(canvas_result.json_data["objects"]) > 0:
        last_point = canvas_result.json_data["objects"][-1]
        x = last_point["left"]
        y = last_point["top"]
        st.session_state.player_x = int(x)
        st.session_state.player_y = int(y)

# Kiểm tra ăn mồi
foods_left = []
for f in st.session_state.foods:
    dx = f["x"] - st.session_state.player_x
    dy = f["y"] - st.session_state.player_y
    dist = (dx ** 2 + dy ** 2) ** 0.5
    if dist < st.session_state.player_size + 10:
        st.session_state.player_size += 2
        st.session_state.score += 10
    else:
        foods_left.append(f)
while len(foods_left) < 10:
    foods_left.append({
        "x": random.randint(20, CANVAS_SIZE-20),
        "y": random.randint(20, CANVAS_SIZE-20)
    })
st.session_state.foods = foods_left
