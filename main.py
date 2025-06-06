import streamlit as st
import requests

# ===== 1. 初始化设置 =====
st.set_page_config(page_title="AI辩论大师", layout="wide")

# 初始化 Session State (用于存储会话数据)
if 'generated_count' not in st.session_state:
    st.session_state.generated_count = 0

DEEPSEEK_API_KEY = st.secrets["DEEPSEEK_API_KEY"]  # 安全存储密钥
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # DeepSeek API 端点

# ===== 2. 炫酷视觉特效 =====
with st.sidebar:
    # st.image("https://i.imgur.com/7W84Kvn.png", width=200)  # 自定义Logo
    # st.markdown("**⚡ 技术栈**  \n`GPT-3.5 · Streamlit · WordCloud`") # 移除技术栈标题和内容
    st.divider()
    # st.caption("明日升级预告：\n- 历史辩论存档  \n- 观众投票功能")
    
    # ===== 使用说明或小贴士 =====
    st.markdown("**💡 使用小贴士**")
    st.info("1. 输入辩题后选择立场和犀利度。\n2. 点击'生成观点'按钮。\n3. AI会生成3个观点。\n4. 调整犀利度可影响观点风格。")
    st.divider()
    
    # ===== 趣味统计 =====
    st.markdown("**📊 会话统计**")
    st.write(f"已生成观点次数： {st.session_state.generated_count}")
    st.divider()

# ===== 3. 核心功能加强版 =====
st.title("🎤 AI奇葩说观点生成器")
col1, col2 = st.columns([1, 2])

with col1:
    # 3.1 输入控件组
    with st.form(key='debate_form'):
        topic = st.text_input("辩题（例：熬夜是现代人的自由）",
                              placeholder="输入你感兴趣的争议话题...")
        position = st.radio("选择立场", ["正方", "反方"], index=0, horizontal=True)
        intensity = st.slider("观点犀利度", 1, 5, 3, help="数值越高观点越尖锐")
        submitted = st.form_submit_button('生成观点', use_container_width=True)

with col2:
    # 3.2 动态演示区
    if submitted:
        with st.spinner(f"AI {position}辩手正在思考..."):
            
            # 检查辩题是否已输入
            if not topic:
                st.warning("请输入辩题！")
                st.stop()
                
            # 3.3 智能prompt工程
            prompt = f"作为{position}辩手，关于'{topic}'，生成3个最具杀伤力的观点。\
                      要求：用生活化例子佐证，语言风格像《奇葩说》选手，犀利程度{intensity}级"

            # 3.4 加入重试机制防API失败
            for _ in range(3):
                try:
                    headers = {
                        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                        "Content-Type": "application/json"
                    }
                    
                    data = {
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 800
                    }
                    
                    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
                    response.raise_for_status()
                    result = response.json()
                    arguments = result["choices"][0]["message"]["content"]
                    
                    # 成功生成观点后，增加计数器
                    st.session_state.generated_count += 1
                    
                    break
                except Exception as e:
                    st.warning(f"API调用出现错误: {str(e)}")
                    time.sleep(2)
            else:
                st.error("AI辩手罢工了，请稍后重试！")
                st.stop()

            # 3.5 显示核心论点文本
            st.subheader(f"🔥 {position}核心论点")
            st.success(arguments)

# ===== 4. 添加社交裂变设计 =====
st.divider()
st.caption("分享你的AI辩论结果 →")
share_cols = st.columns(5)
# with share_cols[0]: st.button("📋 复制文字", use_container_width=True) # 移除复制文字按钮
# with share_cols[1]: st.button("🖼 保存图片", use_container_width=True) # 移除保存图片按钮