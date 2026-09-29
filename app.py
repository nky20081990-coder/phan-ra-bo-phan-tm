import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 1. Khởi tạo cấu hình trang rộng
st.set_page_config(layout="wide", page_title="Hệ Thống Phân Rã Phương Tiện Chuyên Ngành")

st.title("🚜 HỆ THỐNG PHÂN RÃ PHƯƠNG TIỆN CHUYÊN NGÀNH 3D")
st.caption("Ứng dụng Nghiên cứu Kỹ thuật cho Sinh viên | Phát triển bởi Tiến sĩ Nghiên cứu Phương tiện")

# 2. Hai hàm dựng hình học đa giác 3D bề mặt cong thực tế
def ve_banh_xe(cx, cy, cz, banh_kinh, be_day, mau, ten):
    u = np.linspace(0, 2 * np.pi, 25)
    v = np.linspace(-be_day/2, be_day/2, 5)
    U, V = np.meshgrid(u, v)
    X = cx + V
    Y = cy + banh_kinh * np.cos(U)
    Z = cz + banh_kinh * np.sin(U)
    return go.Mesh3d(x=X.flatten(), y=Y.flatten(), z=Z.flatten(), color=mau, opacity=0.95, name=ten, showscale=False)

def ve_than_vo(cx, cy, cz, r_x, r_y, r_z, mau, ten):
    u = np.linspace(0, 2 * np.pi, 25)
    v = np.linspace(-1, 1, 10)
    U, V = np.meshgrid(u, v)
    X = cx + r_x * np.cos(U) * (1 - 0.1 * V**2)
    Y = cy + r_y * V
    Z = cz + r_z * np.sin(U) * (1 - V**2) + (0.2 * V)
    return go.Mesh3d(x=X.flatten(), y=Y.flatten(), z=Z.flatten(), color=mau, opacity=0.9, name=ten, showscale=False)

# 3. Bản điều khiển Menu bên trái
st.sidebar.header("🕹️ DANH MỤC PHƯƠNG TIỆN")
xe_chon = st.sidebar.selectbox(
    "Chọn phương tiện nghiên cứu:",
    ["Xe Máy (Motorbike)", "Xe Ô Tô (Sport Car)", "Xe Tải (Heavy Truck)", "Xe Máy Đào (Excavator)"]
)

exp = st.sidebar.slider("Kéo XUỐNG để phân rã / Kéo LÊN để gộp lại:", min_value=0.0, max_value=1.0, value=0.0, step=0.05)
st.sidebar.info("💡 Mẹo: Giữ chuột trái vào mô hình để xoay 360 độ trong không gian.")

fig = go.Figure()
ten_bo_phan = []
mo_ta_bo_phan = []

# 4. Cấu trúc nạp dữ liệu phẳng tuyến tính cách ly hoàn toàn lỗi căn lề
if xe_chon == "Xe Máy (Motorbike)":
    ten_bo_phan = ["Khung Sườn", "Động Cơ Đơn Xilanh", "Bánh Trước", "Bánh Sau"]
    mo_ta_bo_phan = ["Hệ thống chịu lực chính kết nối càng trước và gắp sau.", "Động cơ 4 thì sinh công lực trực tiếp truyền tới xích tải.", "Bánh dẫn hướng hệ thống lái đi kèm lốp rãnh bám đường.", "Bánh chủ động nhận lực kéo tịnh tiến từ nhông sên dĩa."]
    fig.add_trace(ve_than_vo(0.0, 0.0, 0.3 + 2.0*exp, 0.15, 0.8, 0.4, "silver", "Khung Sườn"))
    fig.add_trace(ve_than_vo(0.0, 0.1, -0.1 + 1.0*exp, 0.2, 0.25, 0.25, "darkgray", "Động Cơ"))
    fig.add_trace(ve_banh_xe(0.0, 0.9 + 2.5*exp, -0.4, 0.45, 0.15, "#1C1A1A", "Bánh Trước"))
    fig.add_trace(ve_banh_xe(0.0, -0.9 - 2.5*exp, -0.4, 0.45, 0.18, "#1C1A1A", "Bánh Sau"))

if xe_chon == "Xe Ô Tô (Sport Car)":
    ten_bo_phan = ["Thân Vỏ Siêu Xe", "Khối Động Cơ V8", "Trục Bánh Trước", "Hệ Thống Cầu Sau"]
mo_ta_bo_phan = ["Vỏ khí động học bo tròn giúp tối ưu hóa hệ số cản gió đường bệ.", "Hệ thống xi-lanh chữ V cung cấp dải mô-men xoắn hiệu năng cao.", "Cụm bánh xe dẫn hướng đi kèm cơ cấu treo độc lập.", "Cầu truyền động sau tích hợp vi sai chia đều lực kéo."]
    fig.add_trace(ve_than_vo(0.0, 0.0, 0.2 + 2.5*exp, 0.9, 1.9, 0.4, "crimson", "Thân Vỏ"))
    fig.add_trace(ve_than_vo(0.0, 1.3, 0.3 + 3.5*exp, 0.3, 0.4, 0.3, "gold", "Động Cơ V8"))
    fig.add_trace(ve_banh_xe(0.0, 1.1 + 1.5*exp, -0.3 - 1.5*exp, 0.45, 2.2, "#1C1A1A", "Trục Bánh Trước"))
    fig.add_trace(ve_than_vo(0.0, -1.2 - 2.5*exp, -0.2, 0.9, 0.25, 0.2, "royalblue", "Cầu Sau"))

if xe_chon == "Xe Tải (Heavy Truck)":
    ten_bo_phan = ["Cabin Đầu Kéo", "Thùng Chứa Hàng", "Trục Bánh Tải Sau"]
    mo_ta_bo_phan = ["Không gian làm việc của tài xế, kết cấu thép cường độ cao bo góc vuông.", "Thùng thép tải trọng lớn liên kết chắc chắn trên thanh sát xi sắt.", "Cụm lốp kép chịu lực tải trọng nặng từ hàng hóa phía trên."]
    fig.add_trace(ve_than_vo(0.0, 1.2 + 2.5*exp, 0.8 + 1.0*exp, 1.1, 0.7, 0.7, "orange", "Cabin"))
    fig.add_trace(ve_than_vo(0.0, -0.6 - 2.5*exp, 0.6 + 2.0*exp, 1.1, 1.7, 0.6, "darkblue", "Thùng Xe"))
    fig.add_trace(ve_banh_xe(0.0, -0.8, -0.4 - 2.0*exp, 0.55, 2.4, "#1C1A1A", "Trục Bánh Sau"))

if xe_chon == "Xe Máy Đào (Excavator)":
    ten_bo_phan = ["Thân Máy Điều Khiển", "Cần Thủy Lực", "Gáo Múc Thép", "Hệ Xích Di Chuyển"]
    mo_ta_bo_phan = ["Mâm quay toa 360 độ chứa cabin vũ đài và động cơ diesel lực lưỡng.", "Cơ cấu tay cần vươn chịu áp suất dầu thủy lực cực lớn.", "Cơ cấu công tác răng thép chuyên dụng cào cuốc đất đá mỏ.", "Hệ băng xích thép chịu lực giúp di chuyển địa hình sình lầy."]
    fig.add_trace(ve_than_vo(0.0, 0.0, 0.5 + 2.5*exp, 1.0, 1.1, 0.5, "yellow", "Thân Trên Máy"))
    fig.add_trace(ve_than_vo(0.0, 1.5 + 3.0*exp, 1.0 + 1.5*exp, 0.15, 0.9, 0.2, "gray", "Cần Thủy Lực"))
    fig.add_trace(ve_than_vo(0.0, 2.6 + 4.5*exp, 0.6 + 0.5*exp, 0.3, 0.3, 0.3, "black", "Gáo Múc"))
    fig.add_trace(ve_banh_xe(0.0, 0.0, -0.5 - 2.0*exp, 0.5, 2.2, "dimgray", "Băng Xích Thép"))

# 5. Cấu hình trục không gian đồ họa 3D
fig.update_layout(scene=dict(xaxis=dict(range=[-6, 6]), yaxis=dict(range=[-6, 6]), zaxis=dict(range=[-6, 6]), aspectmode='cube'), margin=dict(r=0, l=0, b=0, t=20), height=600)

# 6. Bố cục hiển thị cột trên Website
col1, col2 = st.columns()
with col1:
    st.subheader(f"🌐 Mô phỏng cấu trúc: {xe_chon}")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📋 Từ Điển Chức Năng Bộ Phận Chuyên Ngành")
st.write("Sinh viên xem công năng chi tiết từng cấu kiện phương tiện dưới đây:")
    for i in range(len(ten_bo_phan)):
        with st.expander(f"🔍 {ten_bo_phan[i]}"):
            st.write(f"**Chức năng học thuật:** {mo_ta_bo_phan[i]}")
            st.write("*Trạng thái kết cấu:* `Độ phân giải đa giác cao (High-Poly Mesh)`")

st.markdown("---")
st.markdown("<center>Phòng Nghiên cứu Kỹ thuật Hệ thống Phương tiện Động lực Quốc gia © 2026</center>", unsafe_allow_html=True)
