import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Phân rã phương tiện 2D",
    page_icon="🚗",
    layout="wide"
)

st.title("🔧 PHÂN RÃ PHƯƠNG TIỆN 2D")
st.write("Mô hình học tập về cấu tạo xe máy và ô tô")

# ==============================
# CHỌN PHƯƠNG TIỆN
# ==============================

vehicle = st.selectbox(
    "🚘 Chọn phương tiện",
    [
        "🏍️ Xe máy",
        "🚗 Ô tô"
    ]
)

# ==============================
# HTML
# ==============================

html = f"""
<!DOCTYPE html>
<html lang="vi">

<head>

<meta charset="UTF-8">

<style>

body {{
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f1f5f9;
}}

.container {{
    background: white;
    border-radius: 15px;
    padding: 20px;
}}

h2 {{
    text-align: center;
}}

#slider {{
    width: 100%;
}}

.percent {{
    text-align: center;
    font-size: 22px;
    font-weight: bold;
}}

button {{
    padding: 10px 15px;
    border: none;
    border-radius: 8px;
    margin: 5px;
    cursor: pointer;
}}

svg {{
    width: 100%;
    height: 500px;
    background: #e2e8f0;
    border-radius: 15px;
}}

.part {{
    cursor: pointer;
    transition: 0.2s;
}}

.part:hover {{
    opacity: 0.65;
}}

#info {{
    margin-top: 15px;
    padding: 15px;
    background: #eff6ff;
    border-radius: 10px;
    display: none;
}}

</style>

</head>

<body>

<div class="container">

<h2>{vehicle}</h2>

<svg
    id="vehicle"
    viewBox="0 0 1000 500"
>

<!-- ================================= -->
<!-- XE MÁY -->
<!-- ================================= -->

{"".join([]) if vehicle == "🏍️ Xe máy" else ""}

</svg>

<br>

<label>
🔧 Mức độ phân rã
</label>

<input
    id="slider"
    type="range"
    min="0"
    max="100"
    value="0"
>

<div class="percent">
    <span id="percent">0</span>%
</div>

<button onclick="explode(0)">
    🔄 Lắp hoàn chỉnh
</button>

<button onclick="explode(100)">
    🔧 Tháo hoàn toàn
</button>

<div id="info">

    <h3 id="partName"></h3>

    <p>
        <b>Hệ thống:</b>
        <span id="partSystem"></span>
    </p>

    <p>
        <b>Chức năng:</b>
        <span id="partFunction"></span>
    </p>

</div>

</div>


<script>

const slider =
document.getElementById("slider");

const percent =
document.getElementById("percent");


// =====================================
// DỮ LIỆU BỘ PHẬN
// =====================================

const parts = {{

    // ==========================
    // BỘ PHẬN XE MÁY
    // ==========================

    wheel1: {{
        name: "Bánh trước",
        system: "Hệ thống di chuyển",
        function: "Giúp xe di chuyển và thay đổi hướng.",
        x: 0,
        y: 0,
        z: -100
    }},

    wheel2: {{
        name: "Bánh sau",
        system: "Hệ thống di chuyển",
        function: "Nhận lực truyền động và giúp xe chuyển động.",
        x: 0,
        y: 0,
        z: 100
    }},

    engine: {{
        name: "Động cơ",
        system: "Hệ thống động lực",
        function: "Biến đổi năng lượng nhiên liệu thành cơ năng.",
        x: 0,
        y: 100,
        z: 0
    }},

    frame: {{
        name: "Khung xe",
        system: "Kết cấu",
        function: "Liên kết và nâng đỡ các bộ phận của xe.",
        x: 0,
        y: -100,
        z: 0
    }},

    tank: {{
        name: "Bình nhiên liệu",
        system: "Hệ thống nhiên liệu",
        function: "Chứa nhiên liệu cung cấp cho động cơ.",
        x: 0,
        y: -120,
        z: 0
    }},

    seat: {{
        name: "Ghế / Yên",
        system: "Thân xe",
        function: "Là nơi người điều khiển hoặc hành khách ngồi.",
        x: 0,
        y: 130,
        z: 0
    }},

    steering: {{
        name: "Hệ thống lái",
        system: "Hệ thống điều khiển",
        function: "Giúp điều khiển hướng chuyển động.",
        x: 120,
        y: 0,
        z: 0
    }},

    brake: {{
        name: "Hệ thống phanh",
        system: "Hệ thống an toàn",
        function: "Giúp giảm tốc độ hoặc dừng phương tiện.",
        x: -120,
        y: 0,
        z: 0
    }}

}};


// =====================================
// HIỂN THỊ THÔNG TIN
// =====================================

function showInfo(id) {{

    const p = parts[id];

    if (!p)
        return;

    document.getElementById(
        "info"
    ).style.display = "block";

    document.getElementById(
        "partName"
    ).innerText = p.name;

    document.getElementById(
        "partSystem"
    ).innerText = p.system;

    document.getElementById(
        "partFunction"
    ).innerText = p.function;
}}


// =====================================
// PHÂN RÃ
// =====================================

function explode(value) {{

    slider.value = value;

    percent.innerText = value;

    const amount =
        value / 100;

    document
        .querySelectorAll(".part")
        .forEach(function(part) {{

            const id =
                part.dataset.id;

            const data =
                parts[id];

            if (!data)
                return;

            const x =
                data.x * amount;

            const y =
                data.y * amount;

            part.setAttribute(
                "transform",
                "translate(" +
                x +
                "," +
                y +
                ")"
            );
        }});
}}


slider.addEventListener(
    "input",
    function() {{
        explode(this.value);
    }}
);

</script>

</body>
</html>
"""


# ==========================================================
# TẠO SVG XE MÁY / Ô TÔ
# ==========================================================

if vehicle == "🏍️ Xe máy":

    motorcycle_svg = """
    
    <!-- BÁNH TRƯỚC -->

    <g
        class="part"
        data-id="wheel1"
        onclick="showInfo('wheel1')"
    >

        <circle
            cx="230"
            cy="330"
            r="70"
            fill="#111827"
        />

        <circle
            cx="230"
            cy="330"
            r="35"
            fill="#cbd5e1"
        />

    </g>


    <!-- BÁNH SAU -->

    <g
        class="part"
        data-id="wheel2"
        onclick="showInfo('wheel2')"
    >

        <circle
            cx="750"
            cy="330"
            r="70"
            fill="#111827"
        />

        <circle
            cx="750"
            cy="330"
            r="35"
            fill="#cbd5e1"
        />

    </g>


    <!-- KHUNG -->

    <g
        class="part"
        data-id="frame"
        onclick="showInfo('frame')"
    >

        <line
            x1="230"
            y1="330"
            x2="450"
            y2="200"
            stroke="#334155"
            stroke-width="25"
        />

        <line
            x1="450"
            y1="200"
            x2="750"
            y2="330"
            stroke="#334155"
            stroke-width="25"
        />

    </g>


    <!-- ĐỘNG CƠ -->

    <g
        class="part"
        data-id="engine"
        onclick="showInfo('engine')"
    >

        <rect
            x="420"
            y="270"
            width="150"
            height="100"
            rx="20"
            fill="#64748b"
        />

        <circle
            cx="495"
            cy="320"
            r="35"
            fill="#1e293b"
        />

    </g>


    <!-- BÌNH XĂNG -->

    <g
        class="part"
        data-id="tank"
        onclick="showInfo('tank')"
    >

        <ellipse
            cx="500"
            cy="180"
            rx="120"
            ry="55"
            fill="#dc2626"
        />

    </g>


    <!-- YÊN -->

    <g
        class="part"
        data-id="seat"
        onclick="showInfo('seat')"
    >

        <rect
            x="560"
            y="120"
            width="170"
            height="35"
            rx="18"
            fill="#111827"
        />

    </g>


    <!-- TAY LÁI -->

    <g
        class="part"
        data-id="steering"
        onclick="showInfo('steering')"
    >

        <line
            x1="730"
            y1="190"
            x2="790"
            y2="100"
            stroke="#111827"
            stroke-width="15"
        />

        <line
            x1="760"
            y1="105"
            x2="840"
            y2="105"
            stroke="#111827"
            stroke-width="15"
        />

    </g>


    <!-- PHANH -->

    <g
        class="part"
        data-id="brake"
        onclick="showInfo('brake')"
    >

        <circle
            cx="750"
            cy="330"
            r="25"
            fill="#ef4444"
        />

    </g>


    <!-- ĐÈN -->

    <circle
        cx="790"
        cy="190"
        r="25"
        fill="#facc15"
    />

    """

    html = html.replace(
        '<svg\n id="vehicle"\n viewBox="0 0 1000 500"\n>',
        '<svg id="vehicle" viewBox="0 0 1000 500">' +
        motorcycle_svg
    )

else:

    car_svg = """

    <!-- BÁNH TRƯỚC -->

    <g
        class="part"
        data-id="wheel1"
        onclick="showInfo('wheel1')"
    >

        <circle
            cx="250"
            cy="350"
            r="65"
            fill="#111827"
        />

        <circle
            cx="250"
            cy="350"
            r="28"
            fill="#cbd5e1"
        />

    </g>


    <!-- BÁNH SAU -->

    <g
        class="part"
        data-id="wheel2"
        onclick="showInfo('wheel2')"
    >

        <circle
            cx="750"
            cy="350"
            r="65"
            fill="#111827"
        />

        <circle
            cx="750"
            cy="350"
            r="28"
            fill="#cbd5e1"
        />

    </g>


    <!-- KHUNG THÂN -->

    <g
        class="part"
        data-id="frame"
        onclick="showInfo('frame')"
    >

        <path
            d="
            M180 330
            L220 250
            L350 240
            L430 150
            L650 150
            L760 240
            L820 250
            L850 330
            Z
            "
            fill="#2563eb"
        />

    </g>


    <!-- KÍNH -->

    <path
        d="
        M370 235
        L440 165
        L635 165
        L700 235
        Z
        "
        fill="#93c5fd"
        opacity=".8"
    />


    <!-- GHẾ -->

    <g
        class="part"
        data-id="seat"
        onclick="showInfo('seat')"
    >

        <rect
            x="430"
            y="240"
            width="110"
            height="30"
            rx="10"
            fill="#111827"
        />

        <rect
            x="570"
            y="240"
            width="110"
            height="30"
            rx="10"
            fill="#111827"
        />

    </g>


    <!-- ĐỘNG CƠ -->

    <g
        class="part"
        data-id="engine"
        onclick="showInfo('engine')"
    >

        <rect
            x="500"
            y="285"
            width="160"
            height="60"
            rx="10"
            fill="#64748b"
        />

    </g>


    <!-- BÌNH NHIÊN LIỆU -->

    <g
        class="part"
        data-id="tank"
        onclick="showInfo('tank')"
    >

        <rect
            x="400"
            y="270"
            width="80"
            height="40"
            rx="8"
            fill="#ef4444"
        />

    </g>


    <!-- HỆ THỐNG LÁI -->

    <g
        class="part"
        data-id="steering"
        onclick="showInfo('steering')"
    >

        <line
            x1="760"
            y1="250"
            x2="820"
            y2="170"
            stroke="#111827"
            stroke-width="15"
        />

    </g>


    <!-- PHANH -->

    <g
        class="part"
        data-id="brake"
        onclick="showInfo('brake')"
    >

        <circle
            cx="750"
            cy="350"
            r="25"
            fill="#ef4444"
        />

    </g>

    """

    html = html.replace(
        '<svg\n id="vehicle"\n viewBox="0 0 1000 500"\n>',
        '<svg id="vehicle" viewBox="0 0 1000 500">' +
        car_svg
    )


components.html(
    html,
    height=750,
    scrolling=False
)


st.markdown("---")

st.info(
    "Đây là mô hình 2D phục vụ học tập. "
    "Kéo thanh trượt để quan sát các bộ phận tách ra và bấm vào bộ phận để xem chức năng."
)
