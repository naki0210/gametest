import streamlit as st
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="Game Chấm Tròn - Streamlit", layout="centered")
st.title("Game Chấm Tròn (Agar.io mini demo)")

if "player_size" not in st.session_state:
    st.session_state.player_size = 25
    st.session_state.score = 0
    st.session_state.foods = [
        {"x": random.randint(10, 90), "y": random.randint(10, 90)} for _ in range(10)
    ]
    st.session_state.player_skin = "dot"
    st.session_state.player_x = 50
    st.session_state.player_y = 50

skin = st.radio("Chọn skin nhân vật", ["Chấm tròn", "Cá sấu mini"])
if skin == "Chấm tròn":
    st.session_state.player_skin = "dot"
else:
    st.session_state.player_skin = "crocodile"

st.write(f"Điểm số: {st.session_state.score}")
st.write(f"Kích thước nhân vật: {st.session_state.player_size}")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬆️"):
        st.session_state.player_y = max(5, st.session_state.player_y - 5)
with col2:
    st.write("")
with col3:
    if st.button("⬇️"):
        st.session_state.player_y = min(95, st.session_state.player_y + 5)
col4, col5, col6 = st.columns(3)
with col4:
    if st.button("⬅️"):
        st.session_state.player_x = max(5, st.session_state.player_x - 5)
with col5:
    st.write("")
with col6:
    if st.button("➡️"):
        st.session_state.player_x = min(95, st.session_state.player_x + 5)

foods_left = []
for f in st.session_state.foods:
    dx = f["x"] - st.session_state.player_x
    dy = f["y"] - st.session_state.player_y
    dist = (dx ** 2 + dy ** 2) ** 0.5
    if dist < st.session_state.player_size / 4 + 2:
        st.session_state.player_size += 2
        st.session_state.score += 10
    else:
        foods_left.append(f)
while len(foods_left) < 10:
    foods_left.append({"x": random.randint(10, 90), "y": random.randint(10, 90)})
st.session_state.foods = foods_left

fig, ax = plt.subplots(figsize=(5, 5))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
if st.session_state.player_skin == "dot":
    player_circle = plt.Circle(
        (st.session_state.player_x, st.session_state.player_y),
        st.session_state.player_size / 4,
        color="green",
        zorder=2,
    )
    ax.add_patch(player_circle)
    ax.text(
        st.session_state.player_x,
        st.session_state.player_y,
        "naki",
        ha="center",
        va="center",
        color="white",
        fontsize=10,
        zorder=3,
        weight="bold",
    )
else:
    crocodile = plt.Rectangle(
        (st.session_state.player_x - st.session_state.player_size / 4, st.session_state.player_y - st.session_state.player_size / 8),
        st.session_state.player_size / 2,
        st.session_state.player_size / 4,
        color="darkgreen",
        zorder=2,
    )
    ax.add_patch(crocodile)
    ax.text(
        st.session_state.player_x,
        st.session_state.player_y,
        "🐊",
        ha="center",
        va="center",
        color="white",
        fontsize=12,
        zorder=3,
        weight="bold",
    )
for f in st.session_state.foods:
    food = plt.Circle((f["x"], f["y"]), 2, color="red", zorder=1)
    ax.add_patch(food)
ax.axis("off")
st.pyplot(fig)
