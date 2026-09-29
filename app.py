import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Cấu hình trang Streamlit hiển thị rộng
st.set_page_config(layout="wide", page_title="Hệ Thống Phân Rã Phương Tiện Chuyên Ngành")

st.title("🚜 HỆ THỐNG PHÂN RÃ PHƯƠNG TIỆN CHUYÊN NGÀNH 3D")
st.caption("Ứng dụng Nghiên cứu Kỹ thuật cho Sinh viên | Phát triển bởi Tiến sĩ Nghiên cứu Phương tiện")

# 1. Các hàm toán học tạo lưới bề mặt cong thực tế cho cấu kiện (High-Poly Mesh)
def generate_cylinder_mesh(center, radius, height, color, name, orientation='X'):
    """Tạo khối trụ tròn thực tế cho bánh xe, trục động cơ"""
    cx, cy, cz = center
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(-height/2, height/2, 10)
    U, V = np.meshgrid(u, v)
    
    if orientation == 'X':
        X = cx + V
        Y = cy + radius * np.cos(U)
        Z = cz + radius * np.sin(U)
    elif orientation == 'Y':
        X = cx + radius * np.cos(U)
        Y = cy + V
        Z = cz + radius * np.sin(U)
    else:
        X = cx + radius * np.cos(U)
        Y = cy + radius * np.sin(U)
        Z = cz + V
        
    return go.Mesh3d(x=X.flatten(), y=Y.flatten(), z=Z.flatten(), color=color, opacity=0.9, name=name, showscale=False)

def generate_curved_body(center, size, color, name, type_shape="car"):
    """Tạo thân vỏ bo góc khí động học hoàn chỉnh tùy theo loại xe"""
    cx, cy, cz = center
    dx, dy, dz = size[0]/2, size[1]/2, size[2]/2
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(-1, 1, 20)
    U, V = np.meshgrid(u, v)
    
    if type_shape == "car": # Thân vỏ ô tô thuôn mượt
        X = cx + dx * np.cos(U) * (1 - 0.1 * V**2)
        Y = cy + dy * V
        Z = cz + dz * np.sin(U) * (1 - V**2) + (0.2 * V)
    elif type_shape == "truck_cabin": # Cabin xe tải vuông bo góc
        X = cx + dx * np.sign(np.cos(U)) * (np.abs(np.cos(U))**0.5)
        Y = cy + dy * V
        Z = cz + dz * np.sin(U)
    else: # Thân xe máy đào hoặc lốc máy xe máy
        X = cx + dx * np.cos(U)
        Y = cy + dy * V
        Z = cz + dz * np.sin(U)
        
    return go.Mesh3d(x=X.flatten(), y=Y.flatten(), z=Z.flatten(), color=color, opacity=0.9, name=name, showscale=False)

# 2. Cơ sở dữ liệu cấu trúc phân rã 4 loại phương tiện theo yêu cầu
VEHICLE_DB = {
    "1. Xe Máy (Motorbike)": {
        "Khung Sườn & Gá Động Cơ": {"func": generate_curved_body, "args": [[0, 0, 0.3], [0.3, 1.6, 0.8], "silver", "Khung xe", "excavator"], "dir": [0, 0, 2.0], "desc": "Hệ thống chịu lực chính kết nối càng trước và gắp sau."},
        "Khối Động Cơ Đơn Xilanh": {"func": generate_curved_body, "args": [[0, 0.1, -0.1], [0.4, 0.5, 0.5], "darkgray", "Động cơ", "excavator"], "dir": [0, 1.5, 0], "desc": "Động cơ 4 thì, trục cam đơn sinh công lực truyền tới xích."},
"Bánh Xe Trước & Phanh Đĩa": {"func": generate_cylinder_mesh, "args": [[0, 0.9, -0.4], 0.45, 0.15, "#1C1A1A", "Bánh Trước", "X"], "dir": [0, 2.5, -0.5], "desc": "Bánh dẫn hướng tích hợp phanh đĩa thủy lực an toàn."},
        "Bánh Xe Sau & Bộ Truyền Xích": {"func": generate_cylinder_mesh, "args": [[0, -0.9, -0.4], 0.45, 0.18, "#1C1A1A", "Bánh Sau", "X"], "dir": [0, -2.5, -0.5], "desc": "Bánh chủ động nhận lực kéo trực tiếp từ nhông xích xe."}
    },
    "2. Xe Ô Tô (Sport Car)": {
        "Thân Vỏ Khí Động Học": {"func": generate_curved_body, "args": [[0, 0, 0.2], [1.8, 3.8, 0.8], "crimson", "Thân Xe", "car"], "dir": [0, 0, 2.5], "desc": "Vỏ xe tối ưu lực cản gió và tạo lực ép xuống mặt đường."},
        "Khối Động Cơ V8": {"func": generate_cylinder_mesh, "args": [[0, 1.3, 0.3], 0.4, 0.8, "gold", "Động cơ V8", "Z"], "dir": [0, 2.5, 0.5], "desc": "Trái tim hiệu năng cao cung cấp mô-men xoắn lớn cho siêu xe."},
        "Hệ Thống Bánh Trước": {"func": generate_cylinder_mesh, "args": [[0, 1.1, -0.3], 0.45, 2.2, "#1C1A1A", "Cụm Bánh Trước", "X"], "dir": [0, 1.0, -2.0], "desc": "Cụm bánh xe dẫn hướng đi kèm thước lái cơ cấu độc lập."},
        "Hệ Thống Trục Truyền Động Sau": {"func": generate_curved_body, "args": [[0, -1.2, -0.2], [1.8, 0.5, 0.4], "royalblue", "Trục Sau", "excavator"], "dir": [0, -2.5, -1.5], "desc": "Cầu sau tích hợp vi sai phân phối lực kéo ra hai bánh."}
    },
    "3. Xe Tải (Heavy Truck)": {
        "Cabin Xe Tải": {"func": generate_curved_body, "args": [[0, 1.2, 0.8], [2.2, 1.4, 1.4], "orange", "Cabin", "truck_cabin"], "dir": [0, 2.5, 1.5], "desc": "Không gian làm việc của tài xế, thiết kế giảm chấn thủy lực."},
        "Sát Xi & Thùng Xe Tải": {"func": generate_curved_body, "args": [[0, -0.6, 0.6], [2.2, 3.4, 1.2], "darkblue", "Thùng Xe", "excavator"], "dir": [0, -2.5, 2.0], "desc": "Thùng chịu tải trọng lớn liên kết trực tiếp trên hai thanh sát xi sắt."},
        "Hệ Thống Cầu Chịu Lực & Lốp Kép": {"func": generate_cylinder_mesh, "args": [[0, -0.8, -0.4], 0.55, 2.4, "#1C1A1A", "Trục Bánh Sau", "X"], "dir": [0, 0, -2.0], "desc": "Hệ thống cầu xe tải lớn chịu lực kéo tải trọng nặng."}
    },
    "4. Xe Máy Đào (Excavator)": {
        "Thân Trên & Động Cơ Quay": {"func": generate_curved_body, "args": [[0, 0, 0.5], [2.0, 2.2, 1.0], "yellow", "Thân Máy Đào", "excavator"], "dir": [0, 0, 2.5], "desc": "Cabin điều khiển và cụm động cơ diesel quay 360 độ."},
"Cần Thủy Lực (Boom & Arm)": {"func": generate_curved_body, "args": [[0, 1.5, 1.0], [0.3, 1.8, 0.4], "darkgray", "Cần Máy Đào", "excavator"], "dir": [0, 3.0, 1.5], "desc": "Hệ thống cần vươn điều khiển động lực học bằng áp suất dầu thủy lực."},
        "Gáo Múc Cơ Khí (Bucket)": {"func": generate_curved_body, "args": [[0, 2.6, 0.6], [0.6, 0.6, 0.6], "black", "Gáo Múc", "car"], "dir": [0, 4.5, 0.5], "desc": "Cơ cấu công tác trực tiếp dùng để đào, cào múc đất đá."},
        "Hệ Thống Xích Di Chuyển (Crawler)": {"func": generate_cylinder_mesh, "args": [[0, 0, -0.5], 0.5, 2.2, "dimgray", "Hệ Xích Di Chuyển", "X"], "dir": [0, 0, -2.0], "desc": "Hệ thống dải xích thép giúp máy đào di chuyển địa hình phức tạp."}
    }
}

# 3. Giao diện điều khiển bên trái (Sidebar)
st.sidebar.header("🕹️ DANH MỤC PHƯƠNG TIỆN")
selected_vehicle = st.sidebar.selectbox("Chọn phương tiện nghiên cứu kỹ thuật:", list(VEHICLE_DB.keys()))

st.sidebar.subheader("🎛️ Cơ Chế Phân Rã (Exploded View)")
explode_factor = st.sidebar.slider(
    "Kéo XUỐNG để phân rã / Kéo LÊN để gộp lại:", 
    min_value=0.0, max_value=1.0, value=0.0, step=0.05
)
st.sidebar.info("💡 **Gợi ý học tập:** Giữ chuột trái vào mô hình để xoay, con lăn chuột để phóng to thu nhỏ chi tiết xe.")

# 4. Tính toán và vẽ mô hình đa giác 3D động
fig = go.Figure()
components = VEHICLE_DB[selected_vehicle]

for comp_name, info in components.items():
    # Tính ma trận tịnh tiến phân rã nội suy động
    direction = np.array(info["dir"]) * explode_factor
    
    # Lấy hàm sinh cấu kiện tương ứng và cộng thêm độ tịnh tiến phân rã
    args = info["args"].copy()
    args[0] = (np.array(args[0]) + direction).tolist() # Cập nhật tâm khối mới cho hình học
    
    # Thực thi vẽ mesh cấu kiện hoàn chỉnh
    mesh_trace = info["func"](*args)
    fig.add_trace(mesh_trace)

# Thiết lập không gian 3D tiêu chuẩn
fig.update_layout(
    scene=dict(
        xaxis=dict(range=[-6, 6], title="Trục X (Ngang)"),
        yaxis=dict(range=[-6, 6], title="Trục Y (Dọc)"),
        zaxis=dict(range=[-6, 6], title="Trục Z (Cao)"),
        aspectmode='cube'
    ),
    margin=dict(r=0, l=0, b=0, t=20),
    height=650
)

# 5. Phân bổ bố cục trang web hiển thị
col1, col2 = st.columns()

with col1:
    st.subheader(f"🌐 Mô hình 3D hoàn chỉnh: {selected_vehicle[3:]}")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📋 Từ Điển Chức Năng Cấu Kiện Chuyên Ngành")
    st.write("Sinh viên bấm vào từng mục dưới đây để nghiên cứu công năng cơ khí:")
    
    for comp_name, info in components.items():
        with st.expander(f"🔍 {comp_name}"):
st.markdown(f"**Chức năng học thuật:** {info['desc']}")
            st.markdown(f"*Trạng thái cơ cấu:* `Độ phân giải đa giác cao (High-Poly Mesh)`")

st.markdown("---")
st.markdown("<center>Phòng Nghiên cứu Kỹ thuật Hệ thống Phương tiện Động lực Quốc gia © 2026</center>", unsafe_allow_html=True)
