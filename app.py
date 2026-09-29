import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Cấu hình trang Streamlit hiển thị rộng
st.set_page_config(layout="wide", page_title="Hệ Thống Phân Rã Phương Tiện 3D Nghiên Cứu")

st.title("🔬 HỆ THỐNG PHÂN RÃ PHƯƠNG TIỆN TRỰC QUAN 3D (3D VEHICLE EXPLODED VIEW)")
st.caption("Ứng dụng Nghiên cứu Kỹ thuật Phương tiện cho Sinh viên | Phát triển bởi Tiến sĩ Nghiên cứu Phương tiện")

# 1. Hàm bổ trợ tạo hình khối 3D thực tế (Mesh 3D) cho các bộ phận
def create_3d_box(center, size, color, name):
    """Tạo một khối hộp chữ nhật 3D thực tế"""
    cx, cy, cz = center
    dx, dy, dz = size[0]/2, size[1]/2, size[2]/2
    
    # 8 đỉnh của khối hộp
    x = [cx-dx, cx+dx, cx+dx, cx-dx, cx-dx, cx+dx, cx+dx, cx-dx]
    y = [cy-dy, cy-dy, cy+dy, cy+dy, cy-dy, cy-dy, cy+dy, cy+dy]
    z = [cz-dz, cz-dz, cz-dz, cz-dz, cz+dz, cz+dz, cz+dz, cz+dz]
    
    # Các mặt tam giác cấu thành khối hộp (Mesh3d)
    i = [0, 0, 4, 4, 0, 1, 2, 3, 0, 1, 4, 5]
    j = [1, 2, 5, 6, 1, 5, 6, 2, 3, 2, 7, 6]
    k = [2, 3, 6, 7, 4, 4, 5, 5, 7, 6, 5, 4]
    
    return go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, color=color, opacity=0.85, name=name, showscale=False)

def create_3d_cylinder(center, radius, height, color, name, orientation='Z'):
    """Tạo một khối trụ 3D thực tế phục vụ mô phỏng động cơ, bánh xe"""
    cx, cy, cz = center
    nb_steps = 20
    t = np.linspace(0, 2*np.pi, nb_steps)
    
    x, y, z = [], [], []
    # Tạo đường tròn đáy 1 và đáy 2
    for i in range(nb_steps):
        if orientation == 'Z':
            x.append(cx + radius * np.cos(t[i]))
            y.append(cy + radius * np.sin(t[i]))
            z.append(cz - height/2)
        elif orientation == 'X':
            x.append(cx - height/2)
            y.append(cy + radius * np.cos(t[i]))
            z.append(cz + radius * np.sin(t[i]))
            
    for i in range(nb_steps):
        if orientation == 'Z':
            x.append(cx + radius * np.cos(t[i]))
            y.append(cy + radius * np.sin(t[i]))
            z.append(cz + height/2)
        elif orientation == 'X':
            x.append(cx + height/2)
            y.append(cy + radius * np.cos(t[i]))
            z.append(cz + radius * np.sin(t[i]))

    # Tạo các mặt phẳng nối tam giác
    i_list, j_list, k_list = [], [], []
    for i in range(nb_steps - 1):
        i_list.extend([i, i, i + nb_steps])
        j_list.extend([i + 1, i + nb_steps, i + 1 + nb_steps])
        k_list.extend([i + nb_steps, i + 1, i + 1])
        
    return go.Mesh3d(x=x, y=y, z=z, i=i_list, j=j_list, k=k_list, color=color, opacity=0.9, name=name, showscale=False)

# 2. Cơ sở dữ liệu phương tiện hình học 3D hoàn chỉnh
VEHICLE_DB = {
    "Ô tô Động cơ đốt trong (ICE Car)": {
        "Chassis (Thân xe & Khung gầm)": {
"type": "box", "size": [2.0, 4.0, 1.0], "base_pos":, "dir":, "color": "darkgray",
            "desc": "Bộ khung chịu lực chính, bảo vệ hành khách và là nền tảng cốt lõi để gắn kết tất cả các hệ thống phụ trợ."
        },
        "Engine Block (Khối Động cơ V8)": {
            "type": "cylinder", "radius": 0.5, "height": 1.2, "orientation": "Z", "base_pos": [0, 1.5, 0.4], "dir": [0, 3.0, 0.8], "color": "crimson",
            "desc": "Nơi diễn ra quá trình đốt cháy hỗn hợp khí - nhiên liệu, chuyển hóa nhiệt năng thành cơ năng quay trục khuỷu."
        },
        "Front Wheels (Hệ thống bánh trước)": {
            "type": "cylinder", "radius": 0.4, "height": 2.4, "orientation": "X", "base_pos": [0, 1.2, -0.4], "dir": [0, 1.5, -2.0], "color": "black",
            "desc": "Đảm nhận vai trò dẫn hướng cho phương tiện và bám dính mặt đường thông qua hệ thống lốp cao su."
        },
        "Rear Drivetrain (Hệ thống truyền động sau)": {
            "type": "box", "size": [1.8, 0.6, 0.5], "base_pos": [0, -1.4, -0.3], "dir": [0, -3.0, -1.5], "color": "royalblue",
            "desc": "Bao gồm vi sai và trục các-đăng giúp truyền mô-men xoắn từ động cơ tới các bánh xe chủ động phía sau."
        }
    },
    "Máy bay Thương mại (Commercial Airplane)": {
        "Fuselage (Thân máy bay chính)": {
            "type": "cylinder", "radius": 0.6, "height": 5.0, "orientation": "Z", "base_pos":, "dir":, "color": "lightgray",
            "desc": "Thân chính dạng ống khí động học cao, chứa toàn bộ phi hành đoàn, hành khách và khoang hàng hóa áp suất."
        },
        "Main Wings (Cánh nâng khí động học)": {
            "type": "box", "size": [5.5, 1.2, 0.15], "base_pos": [0, -0.5, 0], "dir": [0, -1.0, 2.5], "color": "white",
            "desc": "Thiết kế biên dạng cánh đặc biệt tạo ra chênh lệch áp suất (lực nâng Bernoulli) để thắng trọng lực trái đất."
        },
        "Jet Turbine (Động cơ phản lực)": {
            "type": "cylinder", "radius": 0.35, "height": 0.9, "orientation": "Z", "base_pos": [0, 1.5, -0.4], "dir": [0, 4.0, -1.0], "color": "orangered",
            "desc": "Hút, nén, đốt cháy dòng khí tốc độ cao để tạo phản lực cực lớn đẩy máy bay tiến về phía trước."
        }
    }
}

# 3. Giao diện điều khiển (Sidebar)
st.sidebar.header("🕹️ BẢN ĐIỀU KHIỂN HỌC THUẬT")
selected_vehicle = st.sidebar.selectbox("Chọn phương tiện nghiên cứu:", list(VEHICLE_DB.keys()))

st.sidebar.subheader("🎛️ Cơ Chế Phân Rã (Exploded View)")
explode_factor = st.sidebar.slider(
    "Kéo XUỐNG để phân rã / Kéo LÊN để gộp lại:", 
    min_value=0.0, max_value=1.0, value=0.0, step=0.05
)
st.sidebar.info("💡 **Mẹo nghiên cứu:** Di chuột vào hình khối 3D để xem tên cấu kiện, hoặc xoay/phóng to thu nhỏ trực tiếp trên đồ thị.")

# 4. Xử lý đồ họa hình khối 3D động dựa trên cấu trúc phân rã
fig = go.Figure()
components = VEHICLE_DB[selected_vehicle]

for comp_name, info in components.items():
    # Tính toán vị trí tịnh tiến phân rã động bằng phương pháp nội suy tuyến tính
    base = np.array(info["base_pos"])
    direction = np.array(info["dir"])
    current_pos = base + (direction * explode_factor)
    
    # Dựng hình khối 3D thực tế tương ứng
    if info["type"] == "box":
        mesh = create_3d_box(current_pos, info["size"], info["color"], comp_name)
    elif info["type"] == "cylinder":
        mesh = create_3d_cylinder(current_pos, info["radius"], info["height"], info["color"], comp_name, info["orientation"])
        
    fig.add_trace(mesh)

# Thiết lập không gian 3D chuẩn phòng thí nghiệm
fig.update_layout(
    scene=dict(
        xaxis=dict(range=[-6, 6], title="Trục X"),
        yaxis=dict(range=[-6, 6], title="Trục Y"),
        zaxis=dict(range=[-6, 6], title="Trục Z"),
        aspectmode='cube'
    ),
    margin=dict(r=0, l=0, b=0, t=30),
    height=650,
    showlegend=True
)

# 5. Bố cục hiển thị Website
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("🌐 Mô Hình Học Thuật Kỹ Thuật 3D")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📋 Từ Điển Tra Cứu Chức Năng Bộ Phận")
    st.write("Sinh viên chọn từng mục dưới đây để phân tích sâu công năng chi tiết:")
    
    for comp_name, info in components.items():
        with st.expander(f"🔍 {comp_name}"):
            st.markdown(f"**Chức năng:** {info['desc']}")
            # Tính toán vị trí thời gian thực hiển thị tọa độ nghiên cứu kỹ thuật
            real_pos = np.array(info["base_pos"]) + (np.array(info["dir"]) * explode_factor)
            st.markdown(f"*Tọa độ khối tâm 3D hiện tại:* `X: {real_pos[0]:.2f} | Y: {real_pos[1]:.2f} | Z: {real_pos[2]:.2f}`")

st.markdown("---")
st.markdown("<center>Phòng Thí Nghiệm Cơ Khí Động Lực Học Quốc Gia © 2026</center>", unsafe_allow_html=True)
