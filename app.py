import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Cấu hình trang hiển thị giao diện rộng
st.set_page_config(layout="wide", page_title="Hệ Thống Phân Rã Phương Tiện Chuyên Ngành")

st.title("🚜 HỆ THỐNG PHÂN RÃ PHƯƠNG TIỆN CHUYÊN NGÀNH 3D")
st.caption("Ứng dụng Nghiên cứu Kỹ thuật cho Sinh viên | Tiến sĩ Nghiên cứu Phương tiện")

# 1. Hàm tạo mô hình bánh xe/trục quay tròn (Khối trụ mượt)
def ve_banh_xe(cx, cy, cz, banh_kinh, be_day, mau, ten):
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(-be_day/2, be_day/2, 10)
    U, V = np.meshgrid(u, v)
    X = cx + V
    Y = cy + banh_kinh * np.cos(U)
    Z = cz + banh_kinh * np.sin(U)
    return go.Mesh3d(x=X.flatten(), y=Y.flatten(), z=Z.flatten(), color=mau, opacity=0.95, name=ten, showscale=False)

# 2. Hàm tạo mô hình thân vỏ/cabin (Khối bề mặt cong thực tế)
def ve_than_vo(cx, cy, cz, r_x, r_y, r_z, mau, ten, kieu="xe_con"):
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(-1, 1, 20)
    U, V = np.meshgrid(u, v)
    if kieu == "xe_con":
        X = cx + r_x * np.cos(U) * (1 - 0.1 * V**2)
        Y = cy + r_y * V
        Z = cz + r_z * np.sin(U) * (1 - V**2) + (0.2 * V)
    else:
        X = cx + r_x * np.cos(U)
        Y = cy + r_y * v
        Z = cz + r_z * np.sin(U)
    return go.Mesh3d(x=X.flatten(), y=Y.flatten(), z=Z.flatten(), color=mau, opacity=0.9, name=ten, showscale=False)

# 3. Bản điều khiển chọn phương tiện
st.sidebar.header("🕹️ DANH MỤC PHƯƠNG TIỆN")
xe_chon = st.sidebar.selectbox(
    "Chọn phương tiện nghiên cứu:",
    ["1. Xe Máy (Motorbike)", "2. Xe Ô Tô (Sport Car)", "3. Xe Tải (Heavy Truck)", "4. Xe Máy Đào (Excavator)"]
)

explode = st.sidebar.slider("Kéo XUỐNG để phân rã / Kéo LÊN để gộp lại:", min_value=0.0, max_value=1.0, value=0.0, step=0.05)
st.sidebar.info("💡 **Mẹo:** Dùng chuột xoay 3D mô hình để nhìn rõ các góc bóc tách cơ khí.")

fig = go.Figure()
MoTaCacBoPhan = {}

# 4. Logic xử lý hình thể 3D hoàn chỉnh cho từng loại xe cụ thể
if xe_chon == "1. Xe Máy (Motorbike)":
    MoTaCacBoPhan = {
        "Khung Sườn": "Hệ thống chịu lực chính kết nối càng trước và gắp sau.",
        "Động Cơ Đơn Xilanh": "Động cơ 4 thì sinh công lực trực tiếp truyền tới xích tải.",
        "Bánh Trước": "Bánh dẫn hướng hệ thống lái đi kèm lốp rãnh bám đường.",
        "Bánh Sau": "Bánh chủ động nhận lực kéo tịnh tiến từ nhông sên dĩa."
    }
    fig.add_trace(ve_than_vo(0.0, 0.0, 0.3 + 2.0*explode, 0.15, 0.8, 0.4, "silver", "Khung Sườn", "khac"))
    fig.add_trace(ve_than_vo(0.0, 0.1, -0.1 + 1.0*explode, 0.2, 0.25, 0.25, "darkgray", "Động Cơ"))
    fig.add_trace(ve_banh_xe(0.0, 0.9 + 2.5*explode, -0.4, 0.45, 0.15, "#1C1A1A", "Bánh Trước"))
fig.add_trace(ve_banh_xe(0.0, -0.9 - 2.5*explode, -0.4, 0.45, 0.18, "#1C1A1A", "Bánh Sau"))

elif xe_chon == "2. Xe Ô Tô (Sport Car)":
    MoTaCacBoPhan = {
        "Thân Vỏ Siêu Xe": "Vỏ khí động học bo tròn giúp tối ưu hóa hệ số cản gió đường bệ.",
        "Khối Động Cơ V8": "Hệ thống xi-lanh chữ V cung cấp dải mô-men xoắn hiệu năng cao.",
        "Trục Bánh Trước": "Cụm bánh xe dẫn hướng đi kèm cơ cấu treo độc lập.",
        "Hệ Thống Cầu Sau": "Cầu truyền động sau tích hợp vi sai chia đều lực kéo."
    }
    fig.add_trace(ve_than_vo(0.0, 0.0, 0.2 + 2.5*explode, 0.9, 1.9, 0.4, "crimson", "Thân Vỏ"))
    fig.add_trace(ve_than_vo(0.0, 1.3, 0.3 + 3.5*explode, 0.3, 0.4, 0.3, "gold", "Động Cơ V8"))
    fig.add_trace(ve_banh_xe(0.0, 1.1 + 1.5*explode, -0.3 - 1.5*explode, 0.45, 2.2, "#1C1A1A", "Trục Bánh Trước"))
    fig.add_trace(ve_than_vo(0.0, -1.2 - 2.5*explode, -0.2, 0.9, 0.25, 0.2, "royalblue", "Cầu Sau"))

elif xe_chon == "3. Xe Tải (Heavy Truck)":
    MoTaCacBoPhan = {
        "Cabin Đầu Kéo": "Không gian làm việc của tài xế, kết cấu thép cường độ cao bo góc vuông.",
        "Thùng Chứa Hàng": "Thùng thép tải trọng lớn liên kết chắc chắn trên thanh sát xi sắt.",
        "Trục Bánh Tải Sau": "Cụm lốp kép chịu lực tải trọng nặng từ hàng hóa phía trên."
    }
    fig.add_trace(ve_than_vo(0.0, 1.2 + 2.5*explode, 0.8 + 1.0*explode, 1.1, 0.7, 0.7, "orange", "Cabin"))
    fig.add_trace(ve_than_vo(0.0, -0.6 - 2.5*explode, 0.6 + 2.0*explode, 1.1, 1.7, 0.6, "darkblue", "Thùng Xe"))
    fig.add_trace(ve_banh_xe(0.0, -0.8, -0.4 - 2.0*explode, 0.55, 2.4, "#1C1A1A", "Trục Bánh Sau"))

elif xe_chon == "4. Xe Máy Đào (Excavator)":
    MoTaCacBoPhan = {
        "Thân Máy Điều Khiển": "Mâm quay toa 360 độ chứa cabin vũ đài và động cơ diesel lực lưỡng.",
        "Cần Thủy Lực": "Cơ cấu tay cần vươn chịu áp suất dầu thủy lực cực lớn.",
        "Gáo Múc Thép": "Cơ cấu công tác răng thép chuyên dụng cào cuốc đất đá mỏ.",
        "Hệ Xích Di Chuyển": "Hệ băng xích thép chịu lực giúp di chuyển địa hình sình lầy."
    }
    fig.add_trace(ve_than_vo(0.0, 0.0, 0.5 + 2.5*explode, 1.0, 1.1, 0.5, "yellow", "Thân Trên Máy"))
    fig.add_trace(ve_than_vo(0.0, 1.5 + 3.0*explode, 1.0 + 1.5*explode, 0.15, 0.9, 0.2, "gray", "Cần Thủy Lực"))
    fig.add_trace(ve_than_vo(0.0, 2.6 + 4.5*explode, 0.6 + 0.5*explode, 0.3, 0.3, 0.3, "black", "Gáo Múc"))
    fig.add_trace(ve_banh_xe(0.0, 0.0, -0.5 - 2.0*explode, 0.5, 2.2, "dimgray", "Băng Xích Thép"))

# Cấu hình khung nhìn đồ họa 3D không gian
fig.update_layout(
    scene=dict(
        xaxis=dict(range=[-6, 6], title="Trục X"),
        yaxis=dict(range=[-6, 6], title="Trục Y"),
zaxis=dict(range=[-6, 6], title="Trục Z"),
        aspectmode='cube'
    ),
    margin=dict(r=0, l=0, b=0, t=20),
    height=650
)

# 5. Hiển thị thông tin lên Website
col1, col2 = st.columns()

with col1:
    st.subheader("🌐 Không Gian Phân Rã Hình Thể 3D")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📋 Từ Điển Chức Năng Bộ Phận Chuyên Ngành")
    st.write("Sinh viên xem công năng chi tiết từng cấu kiện phương tiện dưới đây:")
    
    for ten_bo_phan, mo_ta in MoTaCacBoPhan.items():
        with st.expander(f"🔍 {ten_bo_phan}"):
            st.markdown(f"**Chức năng học thuật:** {mo_ta}")
            st.markdown("*Trạng thái kết cấu:* `Độ phân giải bề mặt cong (High-Poly Mesh)`")

st.markdown("---")
st.markdown("<center>Phòng Nghiên cứu Kỹ thuật Hệ thống Phương tiện Động lực Quốc gia © 2026</center>", unsafe_allow_html=True)
