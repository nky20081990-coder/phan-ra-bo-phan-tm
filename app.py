import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Mô hình xe máy 3D",
    page_icon="🏍️",
    layout="wide"
)

st.title("🏍️ MÔ HÌNH XE MÁY 3D")
st.write(
    "Xoay, phóng to và kéo thanh trượt để quan sát quá trình tháo rã."
)

html = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">

<style>
html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #101827;
    font-family: Arial, sans-serif;
}

#app {
    position: relative;
    width: 100%;
    height: 780px;
}

canvas {
    display: block;
    width: 100%;
    height: 100%;
}

#panel {
    position: absolute;
    left: 15px;
    bottom: 15px;
    z-index: 20;

    width: 310px;
    padding: 18px;

    background: rgba(15, 23, 42, .94);
    color: white;

    border-radius: 14px;
}

#panel h2 {
    margin-top: 0;
    font-size: 20px;
}

#slider {
    width: 100%;
}

#value {
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    margin: 8px;
}

button {
    padding: 9px 12px;
    border: 0;
    border-radius: 8px;
    cursor: pointer;
    margin-right: 5px;
    margin-top: 5px;
}

#info {
    position: absolute;
    top: 20px;
    right: 20px;
    z-index: 20;

    width: 280px;

    background: rgba(255,255,255,.96);
    color: #111827;

    padding: 16px;
    border-radius: 14px;

    display: none;
}

#info h3 {
    margin-top: 0;
}

.badge {
    display: inline-block;
    padding: 5px 8px;
    border-radius: 6px;
    background: #dbeafe;
    color: #1e40af;
    font-size: 12px;
    font-weight: bold;
}
</style>

<!-- IMPORTMAP QUAN TRỌNG -->
<script type="importmap">
{
    "imports": {
        "three":
        "https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js",

        "three/addons/":
        "https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/"
    }
}
</script>

</head>

<body>

<div id="app">

    <div id="panel">

        <h2>🔧 Tháo / lắp xe máy</h2>

        <input
            id="slider"
            type="range"
            min="0"
            max="100"
            value="0"
        >

        <div id="value">0%</div>

        <button onclick="setExplosion(0)">
            🔄 Lắp hoàn chỉnh
        </button>

        <button onclick="setExplosion(100)">
            🔧 Tháo hoàn toàn
        </button>

        <p>
            0% = lắp hoàn chỉnh<br>
            100% = tháo rã
        </p>

        <small>
            🖱️ Kéo chuột để xoay<br>
            🔍 Cuộn chuột để phóng to<br>
            👆 Bấm vào bộ phận để xem thông tin
        </small>

    </div>

    <div id="info">

        <h3 id="name">Bộ phận</h3>

        <span
            id="system"
            class="badge"
        >
        </span>

        <p>
            <b>Chức năng:</b>
        </p>

        <p id="function">
        </p>

    </div>

</div>
