import json
import os
import pathlib
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. Page Configuration (Mobile-first centered layout)
st.set_page_config(
    page_title="HKJC Quant V15 · 賽事量化終端",
    page_icon="🐎",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Custom iOS 18 Bento Theme CSS Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&display=swap');

    .stApp {
        background-color: #0E0F12;
        color: #FDFDFD;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang HK", sans-serif;
    }

    /* Top Status Bar */
    .top-status-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #000000;
        border: 1px solid rgba(216, 255, 154, 0.28);
        border-radius: 999px;
        padding: 6px 14px;
        margin-bottom: 14px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.6);
    }

    /* 3D Venue Hero Card */
    .hero-card {
        background: linear-gradient(165deg, #171E1B 0%, #101215 100%);
        border: 1px solid rgba(216, 255, 154, 0.35);
        border-radius: 24px;
        padding: 16px 18px;
        margin-bottom: 16px;
        box-shadow: 0 12px 36px rgba(0,0,0,0.6), 0 0 24px rgba(216, 255, 154, 0.08) inset;
    }

    .hero-title {
        font-size: 22px;
        font-weight: 800;
        color: #FDFDFD;
        margin-bottom: 2px;
    }

    .hero-subtitle {
        font-size: 11px;
        color: #D8FF9A;
        font-family: monospace;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    /* Glassmorphic Bento HUD */
    .bento-hud {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        background: rgba(18, 20, 24, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 10px;
        text-align: center;
    }

    .hud-label {
        font-size: 9.5px;
        color: #A1A1AA;
        margin-bottom: 2px;
    }

    .hud-val {
        font-size: 11.5px;
        font-weight: 800;
        font-family: monospace;
        color: #FDFDFD;
    }

    /* Highlighted Horse Cards (Strictly 2 per race) */
    .horse-card-bet1 {
        background: linear-gradient(95deg, rgba(216, 255, 154, 0.16) 0%, #1E2024 68%);
        border: 1.5px solid #D8FF9A !important;
        border-radius: 16px;
        padding: 12px 14px;
        margin-bottom: 10px;
        box-shadow: 0 6px 20px rgba(216, 255, 154, 0.12);
    }

    .horse-card-bet2 {
        background: linear-gradient(95deg, rgba(110, 231, 183, 0.14) 0%, #1E2024 68%);
        border: 1.5px solid #6EE7B7 !important;
        border-radius: 16px;
        padding: 12px 14px;
        margin-bottom: 10px;
        box-shadow: 0 6px 18px rgba(110, 231, 183, 0.10);
    }

    .horse-card-normal {
        background: #1A1B1F;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 12px 14px;
        margin-bottom: 10px;
    }

    .badge-bet1 {
        background: #D8FF9A;
        color: #111;
        font-size: 10px;
        font-weight: 800;
        padding: 2px 7px;
        border-radius: 6px;
        font-family: monospace;
    }

    .badge-bet2 {
        background: #6EE7B7;
        color: #111;
        font-size: 10px;
        font-weight: 800;
        padding: 2px 7px;
        border-radius: 6px;
        font-family: monospace;
    }

    .rank-pill {
        background: rgba(255, 255, 255, 0.08);
        color: #FDFDFD;
        font-size: 11px;
        font-weight: 900;
        padding: 3px 7px;
        border-radius: 7px;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# 3. Dynamic Data Ingestion with 60s Streamlit Auto-Cache Invalidation
@st.cache_data(ttl=60)
def load_all_races_data():
    base_dir = pathlib.Path(__file__).parent
    data_path = base_dir / "data.json"
    if not data_path.exists():
        data_path = pathlib.Path("data.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

races_data = load_all_races_data()

# 4. Top Status Banner
st.markdown("""
<div class="top-status-bar">
    <div style="display:flex; align-items:center; gap:8px;">
        <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#D8FF9A; box-shadow:0 0 8px #D8FF9A;"></span>
        <span style="font-size:11px; font-weight:700; color:#D8FF9A; font-family:monospace;">STAT-V3.3 物理底座已鎖定 · 雙軌實時流</span>
    </div>
    <span style="font-size:10px; color:#A1A1AA; font-family:monospace;">@st.cache 60s 自動輪詢</span>
</div>
""", unsafe_allow_html=True)

# 5. 3D Isometric Venue Hero Card
st.markdown("""
<div class="hero-card">
    <div class="hero-subtitle">📅 最近賽事 · 10月14日 跑馬地夜賽</div>
    <div class="hero-title">跑馬地夜賽 · HAPPY VALLEY</div>
    <div class="bento-hud">
        <div><div class="hud-label">跑道掛牌</div><div class="hud-val" style="color:#D8FF9A">好地 GOOD</div></div>
        <div><div class="hud-label">欄次與偏差</div><div class="hud-val">草地 A 欄 (+0.28β)</div></div>
        <div><div class="hud-label">天文台實測</div><div class="hud-val">27.9°C · 東風</div></div>
        <div><div class="hud-label">首場開跑</div><div class="hud-val" style="color:#6EE7B7">18:35</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. Race Selector
race_options = [
    f"R{r['r']} ({r['dist']})" + (" ★TOP 1" if r['confRank']==1 else (" ★TOP 2" if r['confRank']==2 else (" ★TOP 3" if r['confRank']==3 else ""))) 
    for r in races_data
]
selected_race_str = st.selectbox("👉 選擇賽事場次：", race_options, index=2) # Default to R3 (TOP 1)
selected_race_idx = race_options.index(selected_race_str)
cur_race = races_data[selected_race_idx]

# 7. Race Telemetry Metrics
c_m1, c_m2, c_m3 = st.columns(3)
with c_m1:
    st.metric("班次途程", f"{cur_race['cls']} · {cur_race['dist']}")
with c_m2:
    st.metric("策略模式", cur_race['regimeTag'])
with c_m3:
    st.metric("精準雙馬推薦", cur_race['betPairText'])

# 8. Interactive Multi-Dimension Sort Dropdown
sort_mode = st.selectbox(
    "📊 馬匹排序方式 (預設：物理名次)",
    [
        "物理名次 (預設 #1 ~ #12)",
        "最值得投注 2 馬置頂",
        "同程最佳時間 (最快優先)",
        "過往比賽名次 (近績最佳)",
        "檔位欄次 (1檔內欄起)",
        "獨贏賠率 (由熱至冷)",
        "安全期望值 EV (由高至低)"
    ],
    index=0
)

# Sorting Handler
runners = cur_race['runners'].copy()
if "物理名次" in sort_mode:
    runners.sort(key=lambda x: x['pureRank'])
elif "最值得投注" in sort_mode:
    runners.sort(key=lambda x: (x['betPriority'], x['pureRank']))
elif "同程最佳時間" in sort_mode:
    runners.sort(key=lambda x: x['bestSec'])
elif "過往比賽名次" in sort_mode:
    runners.sort(key=lambda x: x['formAvg'])
elif "檔位" in sort_mode:
    runners.sort(key=lambda x: x['draw'])
elif "獨贏賠率" in sort_mode:
    runners.sort(key=lambda x: x['odds'])
elif "安全期望值" in sort_mode:
    runners.sort(key=lambda x: x['ev'], reverse=True)

st.markdown(f"**本場全部 {len(runners)} 匹出賽馬匹完整列表 (精準高亮最值得投注 2 匹)**：")

# 9. Render Full-Field Horse Cards (Strictly 2 Highlighted)
primary_rival = runners[1] if len(runners) > 1 else runners[0]

for idx, h in enumerate(runners):
    card_class = "horse-card-normal"
    badge_html = ""
    if h['betRole'] == 'bet1':
        card_class = "horse-card-bet1"
        badge_html = f"<span class='badge-bet1'>{h['betBadge']}</span>"
    elif h['betRole'] == 'bet2':
        card_class = "horse-card-bet2"
        badge_html = f"<span class='badge-bet2'>{h['betBadge']}</span>"

    st.markdown(f"""
    <div class="{card_class}">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span class="rank-pill">物理 #{h['pureRank']}</span>
                <strong style="font-size:15.5px; margin-left:6px;">#{h['num']} {h['name']}</strong>
                <span style="font-size:11px; color:#A1A1AA; font-family:monospace;">({h['brand']})</span>
                {badge_html}
            </div>
            <div style="text-align:right;">
                <span style="font-size:15px; font-weight:800; font-family:monospace; color:#D8FF9A;">{h['odds']}x</span>
            </div>
        </div>
        <div style="font-size:11px; color:#A1A1AA; margin-top:4px;">
            {h['draw']}檔 · {h['wt']}磅 · 騎練: {h['j']} / {h['t']} · 評分: {h['rating']}
        </div>
        <div style="display:grid; grid-template-columns:repeat(5, 1fr); gap:5px; margin-top:8px; padding-top:6px; border-top:1px solid rgba(255,255,255,0.06); font-size:10px; text-align:center;">
            <div><span style="color:#71717A; font-size:8.8px;">物理純率</span><br><strong style="color:#D8FF9A;">{h['pModel']}%</strong></div>
            <div><span style="color:#71717A; font-size:8.8px;">同程最佳</span><br><strong style="color:#6EE7B7;">{h['bestTime']}</strong></div>
            <div><span style="color:#71717A; font-size:8.8px;">過往名次</span><br><strong>{h['last6']}</strong></div>
            <div><span style="color:#71717A; font-size:8.8px;">雙軌勝率</span><br><strong>{h['pBenter']}%</strong></div>
            <div><span style="color:#71717A; font-size:8.8px;">安全 EV</span><br><strong style="color:{'#D8FF9A' if h['ev']>0 else '#A1A1AA'};">{'+' if h['ev']>0 else ''}{h['ev']:.2f}</strong></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Expandable Dual-Chart Pod
    with st.expander(f"📊 展開 #{h['num']} {h['name']} 雙圖表 (六維雷達 + 落飛損益曲線)"):
        c1, c2 = st.columns(2)
        rival = primary_rival if h['num'] != primary_rival['num'] else runners[0]
        
        with c1:
            categories = ['速段', '負磅', '檔位', '步速', '騎練', '場地']
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=h['radar'] + [h['radar'][0]],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(216, 255, 154, 0.25)',
                line_color='#D8FF9A',
                name=f"#{h['num']} {h['name']}"
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=rival['radar'] + [rival['radar'][0]],
                theta=categories + [categories[0]],
                fill='none',
                line_color='#FDFDFD',
                line=dict(dash='dash'),
                name=f"#{rival['num']} {rival['name']}"
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=False, range=[30, 100]),
                    bgcolor='rgba(0,0,0,0.3)'
                ),
                showlegend=True,
                margin=dict(l=15, r=15, t=15, b=15),
                height=210,
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(font=dict(size=8.5, color="#A1A1AA"))
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            
        with c2:
            odds_range = np.linspace(1.5, 25.0, 50)
            ev_curve = (odds_range / h['cutOdds']) - 1.0
            fig_ev = go.Figure()
            fig_ev.add_trace(go.Scatter(
                x=odds_range, y=ev_curve,
                mode='lines', line=dict(color='#6EE7B7', width=2),
                name='EV 曲線'
            ))
            fig_ev.add_hline(y=0.0, line_dash="dash", line_color="rgba(255,255,255,0.3)")
            fig_ev.add_vline(x=h['cutOdds'], line_dash="dot", line_color="#D8FF9A", annotation_text=f"≥{h['cutOdds']}x")
            fig_ev.add_trace(go.Scatter(
                x=[h['odds']], y=[(h['odds']/h['cutOdds'])-1.0],
                mode='markers+text',
                marker=dict(size=9, color='#D8FF9A'),
                text=[f"{h['odds']}x"],
                textposition="top center",
                name="現時賠率"
            ))
            fig_ev.update_layout(
                xaxis_title="獨贏賠率",
                yaxis_title="EV",
                height=210,
                margin=dict(l=15, r=15, t=15, b=15),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0.3)',
                font=dict(size=8.5, color="#A1A1AA"),
                showlegend=False
            )
            st.plotly_chart(fig_ev, use_container_width=True)

# 10. Jockey King & Trainer King Section
st.markdown("---")
st.markdown("### 👑 騎師王 (JKC) & 🏆 練馬師王 (TNC)")
c_jk, c_tk = st.columns(2)
with c_jk:
    st.info("**潘頓 (Z. Purton)** · 26.7 pts (勝率 34.2%)\n- 全夜 8 駒出戰，R1/R3/R8 核心鐵膽")
with c_tk:
    st.success("**巫偉傑 (W. K. Mo)** · 18.0 pts (勝率 28.5%)\n- 全夜 6 駒參戰，R3/R4 雙主力佈局")

st.caption("HKJC Quant Stat-V3.3 · Decoupled Dual-Track Engine · Streamlit Cloud Ready")
