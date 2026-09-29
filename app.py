import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Phòng học 3D - Cấu tạo phương tiện",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 PHÒNG HỌC 3D - CẤU TẠO PHƯƠNG TIỆN")
st.caption(
    "Khám phá cấu tạo xe máy bằng mô hình 3D. "
    "Kéo thanh trượt để tháo/lắp các bộ phận."
)

# =========================================================
# HTML + THREE.JS
# =========================================================

html_code = r"""
<!DOCTYPE html>
<html lang="vi">

<head>
<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    overflow: hidden;
    font-family: Arial, sans-serif;
    background: #111827;
}

#viewer {
    position: relative;
    width: 100%;
    height: 760px;
    overflow: hidden;
}

#canvas {
    width: 100%;
    height: 100%;
    display: block;
}

#topbar {
    position: absolute;
    top: 15px;
    left: 15px;
    right: 15px;
    z-index: 10;

    background: rgba(15, 23, 42, 0.90);
    color: white;

    padding: 14px;
    border-radius: 12px;
}

.title {
    font-size: 21px;
    font-weight: bold;
}

.sub {
    font-size: 13px;
    color: #cbd5e1;
    margin-top: 5px;
}

#controls {
    position: absolute;
    left: 15px;
    bottom: 15px;
    z-index: 10;

    width: 310px;

    background: rgba(15, 23, 42, 0.94);
    color: white;

    padding: 18px;
    border-radius: 14px;
}

#controls label {
    font-weight: bold;
}

#explode {
    width: 100%;
    margin-top: 10px;
}

.percent {
    text-align: center;
    font-size: 20px;
    margin-top: 8px;
    font-weight: bold;
}

button {
    border: none;
    padding: 8px 12px;
    margin-top: 10px;
    margin-right: 5px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
}

#reset {
    background: #e5e7eb;
}

#full {
    background: #38bdf8;
}

#info {
    position: absolute;
    top: 105px;
    right: 15px;

    width: 300px;

    background: rgba(255,255,255,0.96);
    color: #111827;

    padding: 16px;
    border-radius: 14px;

    z-index: 10;

    display: none;
}

#info h3 {
    margin-top: 0;
}

#system {
    display: inline-block;
    padding: 5px 8px;
    background: #dbeafe;
    color: #1e40af;
    border-radius: 7px;
    font-size: 12px;
    font-weight: bold;
}

.help {
    font-size: 12px;
    color: #cbd5e1;
    line-height: 1.5;
    margin-top: 12px;
}

</style>
</head>

<body>

<div id="viewer">

    <div id="topbar">
        <div class="title">
            🏍️ MÔ HÌNH 3D - CẤU TẠO XE MÁY
        </div>

        <div class="sub">
            Kéo thanh trượt để tháo/lắp các bộ phận •
            Kéo chuột để xoay • Lăn chuột để phóng to/thu nhỏ •
            Bấm vào bộ phận để xem thông tin
        </div>
    </div>

    <div id="info">
        <h3 id="partName">Bộ phận</h3>
        <div id="system">Hệ thống</div>

        <p>
            <b>Chức năng:</b>
        </p>

        <p id="partFunction">
            -
        </p>
    </div>

    <div id="controls">

        <label>
            🔧 Mức độ tháo rã
        </label>

        <input
            id="explode"
            type="range"
            min="0"
            max="100"
            value="0"
        >

        <div class="percent">
            <span id="percent">0</span>%
        </div>

        <button id="reset">
            ↩ Lắp hoàn chỉnh
        </button>

        <button id="full">
            🔧 Tháo hoàn toàn
        </button>

        <div class="help">
            • 0%: xe lắp hoàn chỉnh<br>
            • 50%: tháo một phần<br>
            • 100%: các bộ phận tách xa nhau<br>
            • Có thể xoay mô hình bằng chuột
        </div>

    </div>

    <canvas id="canvas"></canvas>

</div>


<script type="module">

import * as THREE from
"https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js";

import { OrbitControls } from
"https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/controls/OrbitControls.js";


// =========================================================
// KHỞI TẠO
// =========================================================

const canvas = document.getElementById("canvas");

const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true
});

renderer.setPixelRatio(window.devicePixelRatio);

renderer.setSize(
    canvas.clientWidth,
    canvas.clientHeight,
    false
);

renderer.shadowMap.enabled = true;


// =========================================================
// CAMERA
// =========================================================

const camera = new THREE.PerspectiveCamera(
    45,
    canvas.clientWidth / canvas.clientHeight,
    0.1,
    1000
);

camera.position.set(
    8,
    5,
    10
);


// =========================================================
// SCENE
// =========================================================

const scene = new THREE.Scene();

scene.background = new THREE.Color(
    0x111827
);


// =========================================================
// ÁNH SÁNG
// =========================================================

const ambient = new THREE.AmbientLight(
    0xffffff,
    2
);

scene.add(ambient);


const directional = new THREE.DirectionalLight(
    0xffffff,
    3
);

directional.position.set(
    5,
    10,
    8
);

directional.castShadow = true;

scene.add(directional);


// =========================================================
// ĐIỀU KHIỂN CAMERA
// =========================================================

const controls = new OrbitControls(
    camera,
    renderer.domElement
);

controls.enableDamping = true;

controls.minDistance = 5;
controls.maxDistance = 30;


// =========================================================
// MẶT ĐẤT
// =========================================================

const groundGeometry =
    new THREE.PlaneGeometry(30, 30);

const groundMaterial =
    new THREE.MeshStandardMaterial({
        color: 0x1f2937
    });

const ground =
    new THREE.Mesh(
        groundGeometry,
        groundMaterial
    );

ground.rotation.x = -Math.PI / 2;

ground.position.y = -1.5;

scene.add(ground);


// =========================================================
// NHÓM BỘ PHẬN
// =========================================================

const parts = [];


// =========================================================
// HÀM TẠO BỘ PHẬN
// =========================================================

function addPart(
    name,
    system,
    functionText,
    mesh,
    explodeVector
) {

    mesh.userData.name = name;
    mesh.userData.system = system;
    mesh.userData.function = functionText;

    mesh.userData.originalPosition =
        mesh.position.clone();

    mesh.userData.explodeVector =
        explodeVector.clone();

    parts.push(mesh);

    scene.add(mesh);

    return mesh;
}


// =========================================================
// VẬT LIỆU
// =========================================================

const black =
    new THREE.MeshStandardMaterial({
        color: 0x111111,
        metalness: 0.5,
        roughness: 0.35
    });

const dark =
    new THREE.MeshStandardMaterial({
        color: 0x374151,
        metalness: 0.7,
        roughness: 0.3
    });

const metal =
    new THREE.MeshStandardMaterial({
        color: 0x9ca3af,
        metalness: 0.9,
        roughness: 0.2
    });

const red =
    new THREE.MeshStandardMaterial({
        color: 0xdc2626,
        metalness: 0.3,
        roughness: 0.35
    });

const yellow =
    new THREE.MeshStandardMaterial({
        color: 0xfacc15,
        metalness: 0.2,
        roughness: 0.3
    });


// =========================================================
// BÁNH TRƯỚC
// =========================================================

const wheelGeometry =
    new THREE.TorusGeometry(
        1.05,
        0.18,
        20,
        48
    );

const frontWheel =
    new THREE.Mesh(
        wheelGeometry,
        black
    );

frontWheel.rotation.y = Math.PI / 2;

frontWheel.position.set(
    3.0,
    0,
    0
);

addPart(
    "Bánh trước",
    "Hệ thống di chuyển",
    "Bánh trước tiếp xúc với mặt đường và giúp xe chuyển động, đồng thời hỗ trợ định hướng.",
    frontWheel,
    new THREE.Vector3(3.5, 0.8, 0)
);


// =========================================================
// BÁNH SAU
// =========================================================

const rearWheel =
    new THREE.Mesh(
        wheelGeometry,
        black
    );

rearWheel.rotation.y = Math.PI / 2;

rearWheel.position.set(
    -2.5,
    0,
    0
);

addPart(
    "Bánh sau",
    "Hệ thống di chuyển",
    "Bánh sau nhận lực truyền động từ động cơ thông qua hệ thống truyền động.",
    rearWheel,
    new THREE.Vector3(-3.5, -0.8, 0)
);


// =========================================================
// KHUNG XE
// =========================================================

const frameGeometry =
    new THREE.BoxGeometry(
        4.5,
        0.3,
        0.35
    );

const frame =
    new THREE.Mesh(
        frameGeometry,
        dark
    );

frame.position.set(
    0,
    0.9,
    0
);

addPart(
    "Khung xe",
    "Khung và kết cấu",
    "Khung xe liên kết các bộ phận chính và chịu tải trong quá trình xe hoạt động.",
    frame,
    new THREE.Vector3(0, 2.2, 0)
);


// =========================================================
// ĐỘNG CƠ
// =========================================================

const engineGeometry =
    new THREE.BoxGeometry(
        1.8,
        1.3,
        1.1
    );

const engine =
    new THREE.Mesh(
        engineGeometry,
        metal
    );

engine.position.set(
    -0.2,
    -0.2,
    0
);

addPart(
    "Động cơ",
    "Hệ thống động lực",
    "Động cơ biến đổi năng lượng của nhiên liệu thành cơ năng để tạo ra công suất cho xe.",
    engine,
    new THREE.Vector3(0, -2.5, 0)
);


// =========================================================
// BÌNH NHIÊN LIỆU
// =========================================================

const tankGeometry =
    new THREE.SphereGeometry(
        1.1,
        24,
        16
    );

const tank =
    new THREE.Mesh(
        tankGeometry,
        red
    );

tank.scale.set(
    1.5,
    0.65,
    0.8
);

tank.position.set(
    0.3,
    1.5,
    0
);

addPart(
    "Bình nhiên liệu",
    "Hệ thống nhiên liệu",
    "Bình nhiên liệu chứa nhiên liệu cung cấp cho động cơ.",
    tank,
    new THREE.Vector3(0, 3, 0)
);


// =========================================================
// YÊN XE
// =========================================================

const seatGeometry =
    new THREE.BoxGeometry(
        2.4,
        0.25,
        0.9
    );

const seat =
    new THREE.Mesh(
        seatGeometry,
        black
    );

seat.position.set(
    -1.3,
    1.45,
    0
);

addPart(
    "Yên xe",
    "Thân xe",
    "Yên xe là vị trí người điều khiển ngồi trong quá trình sử dụng xe.",
    seat,
    new THREE.Vector3(-1.5, 3, 0)
);


// =========================================================
// TAY LÁI
// =========================================================

const handleGeometry =
    new THREE.CylinderGeometry(
        0.08,
        0.08,
        2.0,
        16
    );

const handle =
    new THREE.Mesh(
        handleGeometry,
        dark
    );

handle.rotation.z =
    Math.PI / 2;

handle.position.set(
    2.0,
    2.0,
    0
);

addPart(
    "Tay lái",
    "Hệ thống điều khiển",
    "Tay lái giúp người điều khiển thay đổi hướng chuyển động của xe.",
    handle,
    new THREE.Vector3(2.5, 3.5, 0)
);


// =========================================================
// PHUỘC TRƯỚC
// =========================================================

const forkGeometry =
    new THREE.CylinderGeometry(
        0.10,
        0.10,
        2.5,
        16
    );

const fork =
    new THREE.Mesh(
        forkGeometry,
        metal
    );

fork.rotation.z =
    -0.25;

fork.position.set(
    2.55,
    0.9,
    0
);

addPart(
    "Phuộc trước",
    "Hệ thống treo",
    "Phuộc trước hấp thụ dao động từ mặt đường và giúp bánh trước hoạt động ổn định.",
    fork,
    new THREE.Vector3(3.5, 2.5, 0)
);


// =========================================================
// ỐNG XẢ
// =========================================================

const exhaustGeometry =
    new THREE.CylinderGeometry(
        0.22,
        0.22,
        2.5,
        20
    );

const exhaust =
    new THREE.Mesh(
        exhaustGeometry,
        dark
    );

exhaust.rotation.z =
    Math.PI / 2;

exhaust.position.set(
    -1.1,
    -0.8,
    0.7
);

addPart(
    "Ống xả",
    "Hệ thống xả",
    "Ống xả dẫn khí thải từ động cơ ra ngoài và góp phần giảm tiếng ồn của dòng khí.",
    exhaust,
    new THREE.Vector3(-2, -2, 2)
);


// =========================================================
// ĐÈN TRƯỚC
// =========================================================

const lampGeometry =
    new THREE.SphereGeometry(
        0.4,
        20,
        20
    );

const lamp =
    new THREE.Mesh(
        lampGeometry,
        yellow
    );

lamp.position.set(
    3.1,
    1.5,
    0
);

addPart(
    "Đèn trước",
    "Hệ thống điện",
    "Đèn trước chiếu sáng phía trước xe và giúp tăng khả năng quan sát.",
    lamp,
    new THREE.Vector3(4, 3, 0)
);


// =========================================================
// XÍCH
// =========================================================

const chainGeometry =
    new THREE.TorusGeometry(
        0.55,
        0.06,
        8,
        32
    );

const chain =
    new THREE.Mesh(
        chainGeometry,
        dark
    );

chain.rotation.y =
    Math.PI / 2;

chain.position.set(
    -1.7,
    -0.1,
    0.65
);

addPart(
    "Xích truyền động",
    "Hệ thống truyền động",
    "Xích truyền mô-men xoắn từ động cơ đến bánh sau.",
    chain,
    new THREE.Vector3(-3, -1, 2)
);


// =========================================================
// GƯƠNG
// =========================================================

const mirrorGeometry =
    new THREE.SphereGeometry(
        0.3,
        16,
        16
    );

const mirror1 =
    new THREE.Mesh(
        mirrorGeometry,
        black
    );

mirror1.position.set(
    1.8,
    2.8,
    0.7
);

addPart(
    "Gương chiếu hậu",
    "Hệ thống an toàn",
    "Gương chiếu hậu giúp người điều khiển quan sát phía sau xe.",
    mirror1,
    new THREE.Vector3(2, 4, 2)
);


// =========================================================
// HỆ THỐNG PHANH
// =========================================================

const brakeGeometry =
    new THREE.CylinderGeometry(
        0.25,
        0.25,
        0.15,
        20
    );

const brake =
    new THREE.Mesh(
        brakeGeometry,
        metal
    );

brake.rotation.z =
    Math.PI / 2;

brake.position.set(
    3.0,
    0,
    0.2
);

addPart(
    "Cụm phanh",
    "Hệ thống phanh",
    "Hệ thống phanh tạo lực cản để giảm tốc độ hoặc dừng xe.",
    brake,
    new THREE.Vector3(4, -1, 1)
);


// =========================================================
// HIỂN THỊ THÔNG TIN
// =========================================================

const info =
    document.getElementById("info");

const partName =
    document.getElementById("partName");

const partSystem =
    document.getElementById("system");

const partFunction =
    document.getElementById("partFunction");


// =========================================================
// SLIDER THÁO RÃ
// =========================================================

const slider =
    document.getElementById("explode");

const percent =
    document.getElementById("percent");

function updateExplosion(value) {

    const amount =
        Number(value) / 100;

    percent.textContent =
        value;

    parts.forEach(part => {

        const original =
            part.userData.originalPosition;

        const explode =
            part.userData.explodeVector;

        part.position.x =
            original.x +
            explode.x * amount;

        part.position.y =
            original.y +
            explode.y * amount;

        part.position.z =
            original.z +
            explode.z * amount;

    });
}


slider.addEventListener(
    "input",
    () => {
        updateExplosion(
            slider.value
        );
    }
);


// =========================================================
// NÚT LẮP HOÀN CHỈNH
// =========================================================

document
.getElementById("reset")
.addEventListener(
    "click",
    () => {

        slider.value = 0;

        updateExplosion(0);

    }
);


// =========================================================
// NÚT THÁO HOÀN TOÀN
// =========================================================

document
.getElementById("full")
.addEventListener(
    "click",
    () => {

        slider.value = 100;

        updateExplosion(100);

    }
);


// =========================================================
// CLICK VÀO BỘ PHẬN
// =========================================================

const raycaster =
    new THREE.Raycaster();

const mouse =
    new THREE.Vector2();


renderer.domElement.addEventListener(
    "pointerdown",
    function(event) {

        const rect =
            renderer.domElement.getBoundingClientRect();

        mouse.x =
            ((event.clientX - rect.left)
            / rect.width) * 2 - 1;

        mouse.y =
            -((event.clientY - rect.top)
            / rect.height) * 2 + 1;

        raycaster.setFromCamera(
            mouse,
            camera
        );

        const hits =
            raycaster.intersectObjects(
                parts
            );

        if (hits.length > 0) {

            const selected =
                hits[0].object;

            partName.textContent =
                selected.userData.name;

            partSystem.textContent =
                selected.userData.system;

            partFunction.textContent =
                selected.userData.function;

            info.style.display =
                "block";
        }

    }
);


// =========================================================
// RESPONSIVE
// =========================================================

function resize() {

    const width =
        canvas.clientWidth;

    const height =
        canvas.clientHeight;

    camera.aspect =
        width / height;

    camera.updateProjectionMatrix();

    renderer.setSize(
        width,
        height,
        false
    );
}


window.addEventListener(
    "resize",
    resize
);


// =========================================================
// ANIMATION
// =========================================================

function animate() {

    requestAnimationFrame(
        animate
    );

    controls.update();

    renderer.render(
        scene,
        camera
    );
}


resize();

animate();

</script>

</body>
</html>
"""

components.html(
    html_code,
    height=780,
    scrolling=False
)


st.markdown("---")

st.subheader("📚 Hướng dẫn sử dụng")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        **🔧 Tháo rã**

        Kéo thanh **Mức độ tháo rã**
        sang phải để tách các bộ phận.
        """
    )

with col2:
    st.markdown(
        """
        **🔄 Lắp ráp**

        Kéo thanh về **0%**
        để đưa các bộ phận trở về vị trí ban đầu.
        """
    )

with col3:
    st.markdown(
        """
        **👆 Tìm hiểu**

        Bấm vào một bộ phận
        để xem tên, hệ thống và chức năng.
        """
    )

st.info(
    "Phiên bản hiện tại là mô hình 3D học tập. "
    "Có thể mở rộng thêm ô tô, xe tải, máy đào và các hệ thống chi tiết hơn."
)
