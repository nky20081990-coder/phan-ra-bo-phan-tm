import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide", page_title="Hệ Thống Phân Rã Phương Tiện 3D")

st.title("🔬 HỆ THỐNG PHÂN RÃ PHƯƠNG TIỆN TRỰC QUAN 3D (3D VEHICLE EXPLODED VIEW)")
st.caption("Ứng dụng Nghiên cứu Kỹ thuật cho Sinh viên | Phát triển bởi Tiến sĩ Nghiên cứu Phương tiện")

def create_3d_box(center, size, color, name):
    cx, cy, cz = center
    dx, dy, dz = size[0]/2, size[1]/2, size[2]/2
    x = [cx-dx, cx+dx, cx+dx, cx-dx, cx-dx, cx+dx, cx+dx, cx-dx]
    y = [cy-dy, cy-dy, cy+dy, cy+dy, cy-dy, cy-dy, cy+dy, cy+dy]
    z = [cz-dz, cz-dz, cz-dz, cz-dz, cz+dz, cz+dz, cz+dz, cz+dz]
    i = [0, 0, 4, 4, 0, 1, 2, 3, 0, 1, 1, 2]
    j = [1, 2, 5, 6, 4, 5, 6, 7, 3, 2, 5, 6]
    k = [2, 3, 6, 7, 7, 4, 5, 6, 4, 5, 6, 7]
    return go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, color=color, opacity=0.85, name=name, showscale=False)

def create_3d_cylinder(center, radius, height, color, name, orientation='Z'):
    cx, cy, cz = center
    nb_steps = 20
    t = np.linspace(0, 2*np.pi, nb_steps)
    x, y, z = [], [], []
    for i in range(nb_steps):
        if orientation == 'Z':
            x.append(cx + radius * np.cos(t[i])); y.append(cy + radius * np.sin(t[i])); z.append(cz - height/2)
        elif orientation == 'X':
            x.append(cx - height/2); y.append(cy + radius * np.cos(t[i])); z.append(cz + radius * np.sin(t[i]))
    for i in range(nb_steps):
        if orientation == 'Z':
            x.append(cx + radius * np.cos(t[i])); y.append(cy + radius * np.sin(t[i])); z.append(cz + height/2)
        elif orientation == 'X':
            x.append(cx + height/2); y.append(cy + radius * np.cos(t[i])); z.append(cz + radius * np.sin(t[i]))
    i_list, j_list, k_list = [], [], []
    for i in range(nb_steps - 1):
        i_list.extend([i, i, i + nb_steps])
        j_list.extend([i + 1, i + nb_steps, i + 1 + nb_steps])
        k_list.extend([i + nb_steps, i + 1, i + 1])
    return go.Mesh3d(x=x, y=y, z=z, i=i_list, j=j_list, k=k_list, color=color, opacity=0.9, name=name, showscale=False)

VEHICLE_DB = {
    "Ô tô Động cơ đốt trong (ICE Car)": {
        "Chassis (Thân xe & Khung gầm)": {"type": "box", "size": [2.0, 4.0, 1.0], "base_pos":, "dir":, "color": "darkgray", "desc": "Bộ khung chịu lực chính, bảo vệ hành khách."},
        "Engine Block (Khối Động cơ V8)": {"type": "cylinder", "radius": 0.5, "height": 1.2, "orientation": "Z", "base_pos": [0, 1.5, 0.4], "dir": [0, 3.0, 0.8], "color": "crimson", "desc": "Nơi diễn ra quá trình đốt cháy sinh công lực."},
        "Front Wheels (Hệ thống bánh trước)": {"type": "cylinder", "radius": 0.4, "height": 2.4, "orientation": "X", "base_pos": [0, 1.2, -0.4], "dir": [0, 1.5, -2.0], "color": "black", "desc": "Đảm nhận vai trò dẫn hướng cho phương tiện."},
"Rear Drivetrain (Hệ thống truyền động sau)": {"type": "box", "size": [1.8, 0.6, 0.5], "base_pos": [0, -1.4, -0.3], "dir": [0, -3.0, -1.5], "color": "royalblue", "desc": "Bao gồm vi sai và trục các-đăng truyền mô-men xoắn."}
    },
    "Máy bay Thương mại (Commercial Airplane)": {
        "Fuselage (Thân máy bay chính)": {"type": "cylinder", "radius": 0.6, "height": 5.0, "orientation": "Z", "base_pos":, "dir":, "color": "lightgray", "desc": "Thân chính chứa hành khách và hàng hóa."},
        "Main Wings (Cánh nâng khí động học)": {"type": "box", "size": [5.5, 1.2, 0.15], "base_pos": [0, -0.5, 0], "dir": [0, -1.0, 2.5], "color": "white", "desc": "Tạo ra lực nâng khí động học giúp máy bay bay lên."},
        "Jet Turbine (Động cơ phản lực)": {"type": "cylinder", "radius": 0.35, "height": 0.9, "orientation": "Z", "base_pos": [0, 1.5, -0.4], "dir": [0, 4.0, -1.0], "color": "orangered", "desc": "Tạo ra lực đẩy phản lực cực lớn về phía sau."}
    }
}

selected_vehicle = st.sidebar.selectbox("Chọn phương tiện nghiên cứu:", list(VEHICLE_DB.keys()))
explode_factor = st.sidebar.slider("Kéo XUỐNG để phân rã / Kéo LÊN để gộp lại:", min_value=0.0, max_value=1.0, value=0.0, step=0.05)

fig = go.Figure()
components = VEHICLE_DB[selected_vehicle]

for comp_name, info in components.items():
    current_pos = np.array(info["base_pos"]) + (np.array(info["dir"]) * explode_factor)
    if info["type"] == "box":
        mesh = create_3d_box(current_pos, info["size"], info["color"], comp_name)
    elif info["type"] == "cylinder":
        mesh = create_3d_cylinder(current_pos, info["radius"], info["height"], info["color"], comp_name, info["orientation"])
    fig.add_trace(mesh)

fig.update_layout(scene=dict(xaxis=dict(range=[-6, 6]), yaxis=dict(range=[-6, 6]), zaxis=dict(range=[-6, 6]), aspectmode='cube'), margin=dict(r=0, l=0, b=0, t=30), height=600)

col1, col2 = st.columns([2, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.subheader("📋 Từ Điển Tra Cứu Chức Năng")
    for comp_name, info in components.items():
        with st.expander(f"🔍 {comp_name}"):
            st.write(info['desc'])
