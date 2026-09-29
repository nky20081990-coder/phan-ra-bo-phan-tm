import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Phân rã phương tiện 2D",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 PHÂN RÃ PHƯƠNG TIỆN 2D")

vehicle = st.selectbox(
    "Chọn phương tiện",
    ["🏍️ Xe máy", "🚗 Ô tô"]
)

# =========================================================
# MÔ HÌNH XE MÁY
# =========================================================

motorcycle = r"""
<g id="motorcycle">

    <!-- BÁNH TRƯỚC -->
    <g class="part"
       data-name="Bánh trước"
       data-system="Hệ thống di chuyển"
       data-function="Giúp xe chuyển động và thay đổi hướng."
       data-x="0"
       data-y="-150">

        <circle cx="760" cy="350" r="75"
                fill="#111827"
                stroke="#000"
                stroke-width="8"/>

        <circle cx="760" cy="350" r="35"
                fill="#94a3b8"/>

        <circle cx="760" cy="350" r="10"
                fill="#475569"/>

    </g>


    <!-- BÁNH SAU -->
    <g class="part"
       data-name="Bánh sau"
       data-system="Hệ thống di chuyển"
       data-function="Nhận lực từ hệ thống truyền động và tạo chuyển động."
       data-x="0"
       data-y="150">

        <circle cx="250" cy="350" r="75"
                fill="#111827"
                stroke="#000"
                stroke-width="8"/>

        <circle cx="250" cy="350" r="35"
                fill="#94a3b8"/>

        <circle cx="250" cy="350" r="10"
                fill="#475569"/>

    </g>


    <!-- KHUNG XE -->
    <g class="part"
       data-name="Khung xe"
       data-system="Kết cấu"
       data-function="Liên kết và nâng đỡ các bộ phận chính của xe."
       data-x="0"
       data-y="170">

        <line x1="250" y1="350"
              x2="470" y2="190"
              stroke="#334155"
              stroke-width="28"/>

        <line x1="470" y1="190"
              x2="760" y2="350"
              stroke="#334155"
              stroke-width="28"/>

        <line x1="470" y1="190"
              x2="380" y2="350"
              stroke="#334155"
              stroke-width="25"/>

    </g>


    <!-- ĐỘNG CƠ -->
    <g class="part"
       data-name="Động cơ"
       data-system="Hệ thống động lực"
       data-function="Biến đổi năng lượng của nhiên liệu thành cơ năng."
       data-x="0"
       data-y="230">

        <rect x="390"
              y="250"
              width="170"
              height="120"
              rx="20"
              fill="#64748b"
              stroke="#1e293b"
              stroke-width="8"/>

        <circle cx="475"
                cy="310"
                r="40"
                fill="#1e293b"/>

        <circle cx="475"
                cy="310"
                r="18"
                fill="#cbd5e1"/>

    </g>


    <!-- BÌNH XĂNG -->
    <g class="part"
       data-name="Bình nhiên liệu"
       data-system="Hệ thống nhiên liệu"
       data-function="Chứa nhiên liệu cung cấp cho động cơ."
       data-x="0"
       data-y="-170">

        <path d="
            M390 190
            Q480 120 590 190
            L560 260
            L410 260
            Z"
            fill="#dc2626"
            stroke="#7f1d1d"
            stroke-width="8"/>

    </g>


    <!-- YÊN -->
    <g class="part"
       data-name="Yên xe"
       data-system="Thân xe"
       data-function="Là nơi người điều khiển ngồi."
       data-x="-80"
       data-y="-210">

        <rect x="500"
              y="125"
              width="220"
              height="45"
              rx="20"
              fill="#111827"/>

    </g>


    <!-- TAY LÁI -->
    <g class="part"
       data-name="Tay lái"
       data-system="Hệ thống điều khiển"
       data-function="Giúp người điều khiển thay đổi hướng chuyển động."
       data-x="170"
       data-y="-220">

        <line x1="710"
              y1="190"
              x2="770"
              y2="90"
              stroke="#111827"
              stroke-width="18"/>

        <line x1="740"
              y1="100"
              x2="850"
              y2="100"
              stroke="#111827"
              stroke-width="18"/>

    </g>


    <!-- PHUỘC -->
    <g class="part"
       data-name="Phuộc trước"
       data-system="Hệ thống treo"
       data-function="Hấp thụ dao động và giữ bánh trước ổn định."
       data-x="200"
       data-y="80">

        <line x1="680"
              y1="180"
              x2="760"
              y2="350"
              stroke="#94a3b8"
              stroke-width="15"/>

        <line x1="710"
              y1="180"
              x2="760"
              y2="350"
              stroke="#64748b"
              stroke-width="15"/>

    </g>


    <!-- ỐNG XẢ -->
    <g class="part"
       data-name="Ống xả"
       data-system="Hệ thống xả"
       data-function="Dẫn khí thải từ động cơ ra ngoài."
       data-x="-150"
       data-y="230">

        <rect x="260"
              y="410"
              width="330"
              height="35"
              rx="18"
              fill="#475569"/>

        <circle cx="585"
                cy="427"
                r="25"
                fill="#111827"/>

    </g>


    <!-- ĐÈN -->
    <g class="part"
       data-name="Đèn trước"
       data-system="Hệ thống điện"
       data-function="Chiếu sáng phía trước xe."
       data-x="230"
       data-y="-100">

        <circle cx="790"
                cy="185"
                r="32"
                fill="#facc15"
                stroke="#ca8a04"
                stroke-width="7"/>

    </g>


    <!-- XÍCH -->
    <g class="part"
       data-name="Xích truyền động"
       data-system="Hệ thống truyền động"
       data-function="Truyền chuyển động từ động cơ đến bánh sau."
       data-x="-180"
       data-y="100">

        <ellipse cx="330"
                 cy="350"
                 rx="90"
                 ry="40"
                 fill="none"
                 stroke="#111827"
                 stroke-width="12"/>

    </g>

</g>
"""


# =========================================================
# MÔ HÌNH Ô TÔ
# =========================================================

car = r"""
<g id="car">

    <!-- BÁNH TRƯỚC -->
    <g class="part"
       data-name="Bánh trước"
       data-system="Hệ thống di chuyển"
       data-function="Giúp ô tô di chuyển và thay đổi hướng."
       data-x="0"
       data-y="-150">

        <circle cx="250"
                cy="360"
                r="70"
                fill="#111827"
                stroke="#000"
                stroke-width="8"/>

        <circle cx="250"
                cy="360"
                r="30"
                fill="#94a3b8"/>

    </g>


    <!-- BÁNH SAU -->
    <g class="part"
       data-name="Bánh sau"
       data-system="Hệ thống di chuyển"
       data-function="Truyền lực xuống mặt đường và giúp xe chuyển động."
       data-x="0"
       data-y="150">

        <circle cx="750"
                cy="360"
                r="70"
                fill="#111827"
                stroke="#000"
                stroke-width="8"/>

        <circle cx="750"
                cy="360"
                r="30"
                fill="#94a3b8"/>

    </g>


    <!-- THÂN XE -->
    <g class="part"
       data-name="Thân xe"
       data-system="Kết cấu"
       data-function="Bao bọc và liên kết các hệ thống của ô tô."
       data-x="0"
       data-y="170">

        <path d="
            M160 330
            L220 250
            L370 230
            L450 150
            L650 150
            L730 230
            L830 250
            L860 330
            Z"
            fill="#2563eb"
            stroke="#1e3a8a"
            stroke-width="8"/>

    </g>


    <!-- KÍNH -->
    <g class="part"
       data-name="Kính xe"
       data-system="Thân xe"
       data-function="Giúp người ngồi bên trong quan sát bên ngoài."
       data-x="0"
       data-y="-170">

        <path d="
            M390 225
            L455 165
            L640 165
            L700 225
            Z"
            fill="#93c5fd"
            stroke="#1e40af"
            stroke-width="6"/>

    </g>


    <!-- ĐỘNG CƠ -->
    <g class="part"
       data-name="Động cơ"
       data-system="Hệ thống động lực"
       data-function="Tạo công suất để ô tô chuyển động."
       data-x="0"
       data-y="230">

        <rect x="520"
              y="275"
              width="170"
              height="80"
              rx="15"
              fill="#64748b"
              stroke="#1e293b"
              stroke-width="8"/>

    </g>


    <!-- GHẾ -->
    <g class="part"
       data-name="Ghế xe"
       data-system="Nội thất"
       data-function="Là nơi người lái và hành khách ngồi."
       data-x="0"
       data-y="-220">

        <rect x="400"
              y="240"
              width="100"
              height="35"
              rx="10"
              fill="#111827"/>

        <rect x="540"
              y="240"
              width="100"
              height="35"
              rx="10"
              fill="#111827"/>

    </g>


    <!-- BÌNH NHIÊN LIỆU -->
    <g class="part"
       data-name="Bình nhiên liệu"
       data-system="Hệ thống nhiên liệu"
       data-function="Chứa nhiên liệu cung cấp cho động cơ."
       data-x="-150"
       data-y="100">

        <rect x="350"
              y="300"
              width="100"
              height="60"
              rx="12"
              fill="#dc2626"/>

    </g>


    <!-- HỆ THỐNG PHANH -->
    <g class="part"
       data-name="Phanh"
       data-system="Hệ thống an toàn"
       data-function="Giúp giảm tốc độ và dừng xe."
       data-x="170"
       data-y="150">

        <circle cx="750"
                cy="360"
                r="28"
                fill="#ef4444"/>

    </g>


    <!-- ĐÈN -->
    <g class="part"
       data-name="Đèn trước"
       data-system="Hệ thống điện"
       data-function="Chiếu sáng phía trước xe."
       data-x="230"
       data-y="-100">

        <rect x="820"
              y="260"
              width="35"
              height="55"
              rx="10"
              fill="#facc15"/>

    </g>


    <!-- HỆ THỐNG LÁI -->
    <g class="part"
       data-name="Hệ thống lái"
       data-system="Hệ thống điều khiển"
       data-function="Điều khiển hướng chuyển động của ô tô."
       data-x="180"
       data-y="-250">

        <line x1="760"
              y1="260"
              x2="810"
              y2="180"
              stroke="#111827"
              stroke-width="15"/>

    </g>

</g>
"""


# =========================================================
# CHỌN MÔ HÌNH
# =========================================================

model = motorcycle if vehicle == "🏍️ Xe máy" else car


# =========================================================
# HTML
# =========================================================

html = f"""
<!DOCTYPE html>

<html lang="vi">

<head>

<meta charset="UTF-8">

<style>

body {{
    margin: 0;
    background: #e2e8f0;
    font-family: Arial;
}}

#box {{
    background: white;
    padding: 20px;
    border-radius: 15px;
}}

svg {{
    width: 100%;
    height: 520px;
    background: #f8fafc;
    border-radius: 15px;
}}

.part {{
    cursor: pointer;

    transition:
        transform 0.08s linear,
        opacity 0.2s;
}}

.part:hover {{
    opacity: 0.65;
}}

#slider {{
    width: 100%;
}}

#percent {{
    text-align: center;
    font-size: 25px;
    font-weight: bold;
    margin: 10px;
}}

button {{
    border: 0;
    padding: 10px 15px;
    border-radius: 8px;
    margin: 5px;
    cursor: pointer;
}}

#info {{
    display: none;
    background: #eff6ff;
    border-left: 5px solid #2563eb;
    padding: 15px;
    margin-top: 15px;
    border-radius: 8px;
}}

</style>

</head>


<body>

<div id="box">

<h2>
{vehicle}
</h2>

<p>
<strong>
Kéo thanh trượt để phân tách / lắp ráp phương tiện
</strong>
</p>


<svg
    id="model"
    viewBox="0 0 1000 500"
>

{model}

</svg>


<br>


<input
    id="slider"
    type="range"
    min="0"
    max="100"
    value="0"
>


<div id="percent">
0%
</div>


<button onclick="setValue(0)">
🔄 LẮP HOÀN CHỈNH
</button>


<button onclick="setValue(100)">
🔧 THÁO HOÀN TOÀN
</button>


<div id="info">

<h3 id="name"></h3>

<p>
<b>Hệ thống:</b>
<span id="system"></span>
</p>

<p>
<b>Chức năng:</b>
<span id="function"></span>
</p>

</div>

</div>


<script>


// ===============================================
// LẤY CÁC BỘ PHẬN
// ===============================================

const parts =
document.querySelectorAll(".part");

const slider =
document.getElementById("slider");

const percent =
document.getElementById("percent");


// ===============================================
// PHÂN TÁCH
// ===============================================

function update(value) {{

    const amount =
        Number(value) / 100;


    percent.innerText =
        value + "%";


    parts.forEach(
        function(part) {{

            const x =
                Number(
                    part.dataset.x
                );

            const y =
                Number(
                    part.dataset.y
                );


            const moveX =
                x * amount;

            const moveY =
                y * amount;


            part.setAttribute(
                "transform",
                "translate(" +
                moveX +
                "," +
                moveY +
                ")"
            );

        }}
    );

}}


// ===============================================
// KÉO THANH TRƯỢT
// ===============================================

slider.addEventListener(
    "input",
    function() {{

        update(
            this.value
        );

    }}
);


// ===============================================
// NÚT
// ===============================================

function setValue(value) {{

    slider.value =
        value;

    update(value);

}}


// ===============================================
// THÔNG TIN
// ===============================================

parts.forEach(
    function(part) {{

        part.addEventListener(
            "click",
            function() {{

                document
                    .getElementById(
                        "info"
                    )
                    .style.display =
                    "block";


                document
                    .getElementById(
                        "name"
                    )
                    .innerText =
                    this.dataset.name;


                document
                    .getElementById(
                        "system"
                    )
                    .innerText =
                    this.dataset.system;


                document
                    .getElementById(
                        "function"
                    )
                    .innerText =
                    this.dataset.function;

            }}
        );

    }
);


// ===============================================
// KHỞI TẠO
// ===============================================

update(0);

</script>

</body>

</html>
"""


components.html(
    html,
    height=760,
    scrolling=False
)


st.markdown("---")

st.success(
    "0% = phương tiện nguyên chiếc → "
    "100% = các bộ phận được phân tách. "
    "Kéo ngược thanh trượt để lắp lại."
)
