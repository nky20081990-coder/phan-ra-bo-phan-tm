
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from math import sin, cos, pi

st.set_page_config(
    page_title="3D Vehicle Engineering Lab",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# STYLE
# =========================
st.markdown("""
<style>
:root { --blue:#168cff; --panel:#0b1422; --panel2:#101d2e; }
.stApp { background: radial-gradient(circle at 50% 10%, #122238 0%, #07101b 48%, #040a12 100%); color:#eaf3ff; }
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
.block-container { padding-top: 1rem; padding-bottom: 1rem; }
h1,h2,h3 { color:#eaf3ff !important; }
div[data-testid="stMetric"] { background:#0b1726; border:1px solid #20344c; padding:8px; border-radius:10px; }
div[data-testid="stExpander"] { background:#0b1726; border:1px solid #20344c; border-radius:10px; }
.small-note { color:#91a8c2; font-size:0.82rem; }
.tech-card { background:#0b1726; border:1px solid #20344c; border-radius:12px; padding:14px; margin-bottom:10px; }
.badge { display:inline-block; padding:3px 8px; border-radius:999px; background:#12345a; color:#8fc7ff; font-size:12px; }
</style>
""", unsafe_allow_html=True)

# =========================
# GEOMETRY HELPERS
# =========================
def box(center, size, color, name, opacity=0.92):
    cx,cy,cz = center
    dx,dy,dz = np.array(size)/2
    x=[cx-dx,cx+dx,cx+dx,cx-dx,cx-dx,cx+dx,cx+dx,cx-dx]
    y=[cy-dy,cy-dy,cy+dy,cy+dy,cy-dy,cy-dy,cy+dy,cy+dy]
    z=[cz-dz,cz-dz,cz-dz,cz-dz,cz+dz,cz+dz,cz+dz,cz+dz]
    i=[0,0,4,4,0,1,2,3,0,3,1,2]
    j=[1,2,5,6,4,5,6,7,3,7,2,6]
    k=[2,3,6,7,5,1,7,4,4,4,5,5]
    return go.Mesh3d(x=x,y=y,z=z,i=i,j=j,k=k,color=color,
                     opacity=opacity,name=name,hovertemplate=f"<b>{name}</b><extra></extra>")

def cylinder(center, radius, height, color, name, axis="Y", opacity=0.95, n=28):
    cx,cy,cz=center
    t=np.linspace(0,2*pi,n)
    if axis=="Y":
        x1=cx+radius*np.cos(t); z1=cz+radius*np.sin(t); y1=np.full(n,cy-height/2)
        x2=cx+radius*np.cos(t); z2=cz+radius*np.sin(t); y2=np.full(n,cy+height/2)
    elif axis=="X":
        y1=cy+radius*np.cos(t); z1=cz+radius*np.sin(t); x1=np.full(n,cx-height/2)
        y2=cy+radius*np.cos(t); z2=cz+radius*np.sin(t); x2=np.full(n,cx+height/2)
    else:
        x1=cx+radius*np.cos(t); y1=cy+radius*np.sin(t); z1=np.full(n,cz-height/2)
        x2=cx+radius*np.cos(t); y2=cy+radius*np.sin(t); z2=np.full(n,cz+height/2)
    x=np.r_[x1,x2]; y=np.r_[y1,y2]; z=np.r_[z1,z2]
    ii=[];jj=[];kk=[]
    for q in range(n-1):
        ii += [q,q+n]; jj += [q+1,q+1+n]; kk += [q+n,q+1]
    # close side
    ii += [n-1,2*n-1]; jj += [0,n]; kk += [n,0]
    # caps as triangles around first vertex
    for q in range(1,n-1):
        ii.append(0); jj.append(q+1); kk.append(q)
        ii.append(n); jj.append(n+q); kk.append(n+q+1)
    return go.Mesh3d(x=x,y=y,z=z,i=ii,j=jj,k=kk,color=color,
                     opacity=opacity,name=name,hovertemplate=f"<b>{name}</b><extra></extra>")

def torus(center, major, minor, color, name, axis="Y", n=32, m=10):
    cx,cy,cz=center
    u=np.linspace(0,2*pi,n)
    v=np.linspace(0,2*pi,m)
    U,V=np.meshgrid(u,v,indexing="ij")
    # Torus initially around Y axis
    X=(major+minor*np.cos(V))*np.cos(U)
    Z=(major+minor*np.cos(V))*np.sin(U)
    Y=minor*np.sin(V)
    if axis=="Y":
        X=X+cx; Y=Y+cy; Z=Z+cz
    elif axis=="X":
        oldX=X.copy()
        X=Y+cx; Y=oldX+cy; Z=Z+cz
    verts=np.arange(n*m).reshape(n,m)
    ii=[];jj=[];kk=[]
    for a in range(n):
        for b in range(m):
            a2=(a+1)%n; b2=(b+1)%m
            p=verts[a,b]; q=verts[a2,b]; r=verts[a2,b2]; s=verts[a,b2]
            ii += [p,p]; jj += [q,s]; kk += [r,r]
    return go.Mesh3d(x=X.ravel(),y=Y.ravel(),z=Z.ravel(),
                     i=ii,j=jj,k=kk,color=color,opacity=0.98,name=name,
                     hovertemplate=f"<b>{name}</b><extra></extra>")

def line3d(points, color, name, width=5):
    p=np.array(points)
    return go.Scatter3d(x=p[:,0],y=p[:,1],z=p[:,2],mode="lines",
                        line=dict(color=color,width=width),
                        name=name,hovertemplate=f"<b>{name}</b><extra></extra>")

# =========================
# VEHICLE DATABASE
# Coordinate convention:
# X = width, Y = length (front +), Z = height
# =========================
PARTS = []

def add(name, category, kind, center, size=None, radius=None, height=None,
        axis="Y", color="#7c8794", mass=0, desc="", material=""):
    PARTS.append(dict(
        name=name, category=category, kind=kind, center=np.array(center,dtype=float),
        size=size, radius=radius, height=height, axis=axis, color=color,
        mass=mass, desc=desc, material=material
    ))

# 1 Chassis / structure
add("Khung gầm (Chassis)","Kết cấu","box",[0,-0.05,0.10],[1.70,4.10,0.25],color="#48515c",mass=180,
    desc="Kết cấu chịu lực chính liên kết hệ thống treo, động cơ, thân xe và khoang hành khách.",material="Thép cường độ cao")
add("Sàn xe (Floor Pan)","Kết cấu","box",[0,-0.15,0.28],[1.55,3.15,0.12],color="#68717c",mass=55,
    desc="Tấm sàn tạo mặt nền cho khoang hành khách và góp phần tăng độ cứng xoắn.",material="Thép dập")
add("Cản trước (Front Bumper)","Thân vỏ","box",[0,2.35,0.55],[1.78,0.20,0.42],color="#aab3bd",mass=8,
    desc="Cản trước hấp thụ một phần năng lượng va chạm và tích hợp vùng lắp cảm biến.",material="Nhựa PP")
add("Cản sau (Rear Bumper)","Thân vỏ","box",[0,-2.38,0.55],[1.78,0.20,0.42],color="#aab3bd",mass=8,
    desc="Cản sau bảo vệ phần đuôi xe và hỗ trợ thiết kế khí động học.",material="Nhựa PP")

# 5 Engine / powertrain
add("Động cơ I4 (Engine)","Động lực","box",[0,1.35,0.70],[0.95,1.15,0.72],color="#c62828",mass=145,
    desc="Nguồn công suất chính của xe ICE; biến đổi năng lượng hóa học của nhiên liệu thành công cơ học.",material="Hợp kim nhôm + gang")
add("Hộp số (Transmission)","Động lực","box",[0,0.25,0.48],[0.82,0.95,0.48],color="#2869b8",mass=55,
    desc="Thay đổi tỷ số truyền và truyền mô-men xoắn từ động cơ tới vi sai.",material="Hợp kim nhôm")
add("Vi sai (Differential)","Động lực","box",[0,-1.15,0.34],[0.72,0.55,0.40],color="#3d7fba",mass=25,
    desc="Phân phối mô-men tới hai bánh chủ động và cho phép hai bánh quay với tốc độ khác nhau khi vào cua.",material="Thép + nhôm")
add("Trục truyền động (Driveshaft)","Động lực","cylinder",[0,-0.42,0.38],radius=0.09,height=1.15,axis="Y",color="#7e8790",mass=7,
    desc="Truyền mô-men từ hộp số tới cụm vi sai.",material="Thép hợp kim")

# 9 cooling / fuel / electrical
add("Két nước (Radiator)","Làm mát","box",[0,2.00,0.65],[1.18,0.12,0.58],color="#6fa8dc",mass=10,
    desc="Trao đổi nhiệt giữa nước làm mát và không khí để kiểm soát nhiệt độ động cơ.",material="Nhôm")
add("Bình nhiên liệu (Fuel Tank)","Nhiên liệu","box",[0,-1.20,0.12],[0.95,0.95,0.30],color="#4c5966",mass=10,
    desc="Chứa nhiên liệu cho hệ thống cung cấp nhiên liệu của động cơ đốt trong.",material="Thép/nhựa")
add("Ắc quy 12V (Battery)","Điện","box",[-0.55,0.85,0.42],[0.42,0.55,0.34],color="#242a31",mass=14,
    desc="Cung cấp điện khi khởi động và ổn định nguồn điện cho các hệ thống phụ tải.",material="Chì-axit")
add("Hệ thống xả (Exhaust)","Xả","cylinder",[0.42,-1.75,0.22],radius=0.07,height=1.65,axis="Y",color="#b17b43",mass=18,
    desc="Dẫn khí thải qua bộ xử lý khí thải và giảm tiếng ồn trước khi thoát ra ngoài.",material="Thép không gỉ")

# 13 suspension 4 corners
for x,side in [(-0.86,"Trái"),(0.86,"Phải")]:
    for y,pos in [(1.45,"Trước"),(-1.45,"Sau")]:
        add(f"Giảm xóc {pos} {side}","Treo","cylinder",[x,y,0.00],radius=0.09,height=0.55,axis="Z",color="#2e8b57",mass=4,
            desc="Bộ phận đàn hồi và giảm chấn giúp kiểm soát dao động thân xe, tăng độ bám đường.",material="Thép + cao su")

# 17 wheels / brakes
for x,side in [(-0.95,"Trái"),(0.95,"Phải")]:
    for y,pos in [(1.42,"Trước"),(-1.42,"Sau")]:
        add(f"Bánh xe {pos} {side}","Bánh xe","wheel",[x,y,-0.18],radius=0.38,height=0.22,axis="X",color="#14181d",mass=17,
            desc="Lốp và vành tạo liên kết ma sát với mặt đường, đồng thời truyền lực kéo và lực phanh.",material="Cao su + hợp kim")
        add(f"Phanh đĩa {pos} {side}","Phanh","disc",[x,y,-0.18],radius=0.25,height=0.08,axis="X",color="#d44747",mass=4,
            desc="Đĩa phanh kết hợp với cùm phanh để tạo mô-men hãm tại bánh xe.",material="Gang")

# 25 steering
add("Cơ cấu lái (Steering Rack)","Điều khiển","box",[0,0.85,0.18],[1.30,0.18,0.16],color="#355c8a",mass=8,
    desc="Biến chuyển động quay của vô lăng thành chuyển động ngang điều khiển bánh trước.",material="Thép")
# 26 interior / seats
add("Nội thất & ghế (Interior)","Nội thất","box",[0,-0.20,0.78],[1.35,1.75,0.72],color="#252b33",mass=75,
    desc="Cụm ghế, bảng điều khiển và các thành phần nội thất trong khoang hành khách.",material="Thép + foam + da/vải")

# Body panels as a grouped visual component, added separately for richer detail
add("Mui xe (Hood)","Thân vỏ","box",[0,1.48,1.16],[1.55,1.05,0.10],color="#bfc7d0",mass=14,
    desc="Tấm che khoang động cơ, đồng thời tạo hình khí động học cho phần đầu xe.",material="Thép/nhôm")
add("Mái xe (Roof)","Thân vỏ","box",[0,-0.25,1.45],[1.52,1.75,0.10],color="#aeb7c1",mass=18,
    desc="Bao che khoang hành khách và là một phần của kết cấu an toàn cabin.",material="Thép")
add("Kính chắn gió (Windshield)","Thân vỏ","box",[0,0.72,1.23],[1.48,0.08,0.48],color="#4e8ca8",mass=8,
    desc="Tấm kính an toàn phía trước, hỗ trợ tầm nhìn và khí động học.",material="Kính dán an toàn")
add("Cụm đèn trước (Headlights)","Điện","box",[-0.57,2.20,0.82],[0.30,0.16,0.16],color="#e9f6ff",mass=2,
    desc="Chiếu sáng phía trước và cung cấp tín hiệu nhận diện cho các phương tiện khác.",material="Polycarbonate")
add("Cụm đèn sau (Tail Lights)","Điện","box",[0.57,-2.20,0.82],[0.30,0.16,0.16],color="#d62f3f",mass=2,
    desc="Đèn vị trí, phanh và tín hiệu phía sau.",material="Polycarbonate")

# We now have 32 visual parts. UI calls this detailed mode.
TOTAL_MASS = sum(p["mass"] for p in PARTS)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🚗 BẢN ĐIỀU KHIỂN")
st.sidebar.caption("Phòng thí nghiệm mô phỏng cơ khí 3D")

mode = st.sidebar.radio(
    "Chế độ hiển thị",
    ["Tổng thể", "Phân rã Exploded View", "Theo cụm kỹ thuật"],
    index=1
)

explode = st.sidebar.slider(
    "Mức độ phân rã",
    0.0, 1.0, 0.38, 0.02,
    help="0 = gộp hoàn toàn; 1 = phân rã tối đa."
)

category = st.sidebar.selectbox(
    "Lọc cụm kỹ thuật",
    ["Tất cả"] + sorted(list(dict.fromkeys(p["category"] for p in PARTS)))
)

show_labels = st.sidebar.checkbox("Hiện tên bộ phận", True)
show_grid = st.sidebar.checkbox("Hiện khung lưới", True)
auto_rotate = st.sidebar.checkbox("Tự động xoay", False)

if st.sidebar.button("↩️ Đưa mô hình về vị trí ban đầu", use_container_width=True):
    st.rerun()

# =========================
# HEADER
# =========================
st.title("🚗 HỆ THỐNG PHÂN RÃ Ô TÔ 3D NGHIÊN CỨU")
st.caption("Mô phỏng cấu tạo và chức năng các hệ thống chính của ô tô động cơ đốt trong — phục vụ học tập và nghiên cứu kỹ thuật.")

# =========================
# BUILD FIGURE
# =========================
fig = go.Figure()

# Exploded displacement by category
cat_dir = {
    "Kết cấu": np.array([0,0,0.0]),
    "Động lực": np.array([0,1.35,0.85]),
    "Làm mát": np.array([0,2.0,0.75]),
    "Nhiên liệu": np.array([0,-1.8,-0.45]),
    "Điện": np.array([-1.25,0.0,0.85]),
    "Xả": np.array([1.15,-1.55,0.15]),
    "Treo": np.array([1.15,0.0,-0.65]),
    "Bánh xe": np.array([1.45,0.0,-0.85]),
    "Phanh": np.array([1.45,0.0,-0.85]),
    "Điều khiển": np.array([-1.0,0.85,0.25]),
    "Nội thất": np.array([0,-0.25,1.15]),
    "Thân vỏ": np.array([0,0,1.75]),
}

visible = [p for p in PARTS if category == "Tất cả" or p["category"] == category]

# In grouped mode, selected category is exploded more strongly
for p in visible:
    if mode == "Tổng thể":
        factor = 0.0
    elif mode == "Theo cụm kỹ thuật":
        factor = explode if p["category"] == category else 0.10 * explode
    else:
        factor = explode

    pos = p["center"] + cat_dir.get(p["category"], np.zeros(3)) * factor

    if p["kind"] == "box":
        fig.add_trace(box(pos,p["size"],p["color"],p["name"]))
    elif p["kind"] == "cylinder":
        fig.add_trace(cylinder(pos,p["radius"],p["height"],p["color"],p["name"],p["axis"]))
    elif p["kind"] == "wheel":
        fig.add_trace(torus(pos, p["radius"]*0.78, p["radius"]*0.22, p["color"], p["name"], axis="X"))
        fig.add_trace(cylinder(pos, p["radius"]*0.52, p["height"], "#252a30", p["name"]+" - Vành", "X", opacity=1.0))
    elif p["kind"] == "disc":
        fig.add_trace(cylinder(pos,p["radius"],p["height"],p["color"],p["name"],p["axis"],opacity=0.95))

# Axles
if category == "Tất cả":
    fig.add_trace(line3d([[-0.95,1.42,-0.18],[0.95,1.42,-0.18]],"#69737e","Cầu trước",3))
    fig.add_trace(line3d([[-0.95,-1.42,-0.18],[0.95,-1.42,-0.18]],"#69737e","Cầu sau",3))

# Labels as scatter
if show_labels:
    lp = []
    lt = []
    for p in visible:
        factor = 0 if mode=="Tổng thể" else explode
        if mode=="Theo cụm kỹ thuật":
            factor = explode if p["category"]==category else 0.10*explode
        pos = p["center"] + cat_dir.get(p["category"],np.zeros(3))*factor
        lp.append(pos + np.array([0,0,0.28]))
        lt.append(p["name"])
    if lp:
        lp=np.array(lp)
        fig.add_trace(go.Scatter3d(
            x=lp[:,0],y=lp[:,1],z=lp[:,2],
            mode="text", text=lt,
            textfont=dict(size=9,color="#d9ecff"),
            name="Nhãn bộ phận",
            hoverinfo="skip"
        ))

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=700,
    margin=dict(l=0,r=0,t=5,b=0),
    showlegend=False,
    scene=dict(
        xaxis=dict(title="X — chiều rộng", range=[-4.5,4.5], showgrid=show_grid, zeroline=False),
        yaxis=dict(title="Y — chiều dài", range=[-5.0,5.0], showgrid=show_grid, zeroline=False),
        zaxis=dict(title="Z — chiều cao", range=[-3.0,4.2], showgrid=show_grid, zeroline=False),
        aspectmode="manual",
        aspectratio=dict(x=1.0,y=1.25,z=0.72),
        camera=dict(eye=dict(x=1.65,y=1.75,z=1.25))
    )
)

# =========================
# MAIN LAYOUT
# =========================
left, right = st.columns([2.75, 1.0], gap="medium")

with left:
    st.subheader("🌐 Mô hình ô tô 3D")
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "responsive": True,
            "scrollZoom": True,
            "modeBarButtonsToRemove": ["lasso2d","select2d"]
        }
    )

    st.markdown("### 📊 Tổng quan phương tiện")
    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("Bộ phận mô phỏng", len(PARTS))
    m2.metric("Khối lượng ước tính", f"{TOTAL_MASS:.0f} kg")
    m3.metric("Chiều dài", "4.80 m")
    m4.metric("Chiều rộng", "1.85 m")
    m5.metric("Chiều cao", "1.45 m")

    st.markdown("### 🧩 Các cụm kỹ thuật")
    cats = sorted(list(dict.fromkeys(p["category"] for p in PARTS)))
    cat_cols = st.columns(min(6,len(cats)))
    for i,c in enumerate(cats):
        count=sum(1 for p in PARTS if p["category"]==c)
        with cat_cols[i%len(cat_cols)]:
            st.markdown(f'<div class="tech-card"><span class="badge">{c}</span><br><b>{count} bộ phận</b></div>',unsafe_allow_html=True)

with right:
    st.subheader("🔧 Thông tin kỹ thuật")
    st.markdown(f'<div class="tech-card"><b>Chế độ:</b> {mode}<br><b>Mức phân rã:</b> {explode:.0%}<br><b>Bộ lọc:</b> {category}</div>',unsafe_allow_html=True)

    search = st.text_input("🔎 Tìm bộ phận", placeholder="Ví dụ: động cơ, phanh, bánh xe...")
    results = visible
    if search.strip():
        q=search.lower()
        results=[p for p in visible if q in p["name"].lower() or q in p["category"].lower()]

    st.markdown(f"**DANH SÁCH BỘ PHẬN ({len(results)})**")
    for p in results:
        with st.expander(f"🔩 {p['name']}"):
            st.markdown(f"**Nhóm:** {p['category']}")
            st.markdown(f"**Chức năng:** {p['desc']}")
            st.markdown(f"**Vật liệu:** {p['material']}")
            st.markdown(f"**Khối lượng ước tính:** {p['mass']} kg")
            st.code(
                f"X = {p['center'][0]:.2f} m\n"
                f"Y = {p['center'][1]:.2f} m\n"
                f"Z = {p['center'][2]:.2f} m",
                language="text"
            )

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#7890aa'>"
    "PHÒNG THÍ NGHIỆM CƠ KHÍ ĐỘNG LỰC HỌC • MÔ PHỎNG HỌC THUẬT 3D • 2026"
    "</div>",
    unsafe_allow_html=True
)
