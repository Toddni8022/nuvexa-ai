import streamlit as st
from datetime import datetime
import json
import random
from config import APP_NAME, APP_TAGLINE, MODES, AVATAR_STYLES
from database import NuvexaDB
from assistant import NuvexaAssistant
from shopping import ShoppingEngine

st.set_page_config(page_title=APP_NAME, page_icon="🤖", layout="wide", initial_sidebar_state="auto")

st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="NUVEXA">
<meta name="mobile-web-app-capable" content="yes">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    * {
        font-family: 'Inter', sans-serif;
        -webkit-tap-highlight-color: rgba(0,0,0,0);
        -webkit-touch-callout: none;
    }
    html, body {
        overscroll-behavior: none;
        -webkit-overflow-scrolling: touch;
    }
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        min-height: 100vh;
    }
    .main-header {
        font-size: clamp(2rem, 8vw, 4rem);
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: -2px;
        animation: glow 2s ease-in-out infinite alternate;
        padding: 10px;
    }
    @keyframes glow {
        from { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.5)); }
        to { filter: drop-shadow(0 0 30px rgba(118, 75, 162, 0.8)); }
    }
    .tagline {
        text-align: center;
        color: #a8b2d1;
        font-size: clamp(0.9rem, 4vw, 1.3rem);
        margin-top: -10px;
        margin-bottom: 20px;
        font-weight: 300;
        padding: 0 15px;
    }
    .assistant-avatar {
        font-size: clamp(3rem, 10vw, 5rem);
        text-align: center;
        margin: 20px 0;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-10px); } }
    .product-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: clamp(15px, 3vw, 25px);
        margin: 15px 0;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        touch-action: manipulation;
    }
    .product-card:hover,
    .product-card:active {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
    }
    @media (max-width: 768px) {
        .product-card {
            margin: 10px 0;
            padding: 15px;
        }
    }
    .cart-item {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        padding: 15px; border-radius: 15px; margin: 10px 0; border: 1px solid rgba(102, 126, 234, 0.3);
    }
    .payment-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%);
        border: 2px solid rgba(16, 185, 129, 0.5); border-radius: 20px; padding: 30px;
        margin: 20px 0; backdrop-filter: blur(10px);
    }
    .stButton>button {
        border-radius: 25px;
        font-weight: 600;
        padding: 15px 30px;
        min-height: 44px;
        min-width: 44px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        cursor: pointer;
        -webkit-tap-highlight-color: transparent;
        touch-action: manipulation;
    }
    .stButton>button:hover,
    .stButton>button:active {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 12, 41, 0.95) 0%, rgba(48, 43, 99, 0.95) 100%);
        backdrop-filter: blur(10px); border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    .stChatMessage {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: clamp(10px, 2vw, 15px);
        margin: 10px 0;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #e6f1ff;
        word-wrap: break-word;
    }
    p, span, div {
        color: #a8b2d1;
        word-wrap: break-word;
    }
    /* Mobile-specific styles */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
            letter-spacing: -1px;
        }
        .tagline {
            font-size: 1rem;
            margin-bottom: 15px;
        }
        [data-testid="stSidebar"] {
            width: 85vw !important;
        }
        .stChatInput {
            font-size: 16px !important; /* Prevents zoom on iOS */
        }
    }
    /* iOS Safari specific fixes */
    @supports (-webkit-touch-callout: none) {
        input, textarea, select {
            font-size: 16px !important;
        }
        .stApp {
            padding-bottom: env(safe-area-inset-bottom);
        }
    }
</style>
""", unsafe_allow_html=True)

if 'db' not in st.session_state:
    st.session_state.db = NuvexaDB()
    st.session_state.user_id = st.session_state.db.get_or_create_user("User")
    st.session_state.ai_assistant = NuvexaAssistant()
    st.session_state.shopping_engine = ShoppingEngine()
    st.session_state.current_mode = 'assistant'
    st.session_state.messages = []
    st.session_state.show_products = False
    st.session_state.search_results = []
    st.session_state.cart_open = False
    st.session_state.show_checkout = False

def load_conversation_history():
    history = st.session_state.db.get_conversation_history(st.session_state.user_id, st.session_state.current_mode)
    st.session_state.messages = [{"role": role, "content": content} for role, content in history]

def save_message(role, content):
    st.session_state.db.save_message(st.session_state.user_id, st.session_state.current_mode, content, role)

def switch_mode(new_mode):
    st.session_state.current_mode = new_mode
    st.session_state.ai_assistant.set_mode(new_mode)
    load_conversation_history()
    st.session_state.show_products = False

def add_to_cart(product):
    st.session_state.db.add_to_cart(st.session_state.user_id, product['name'], product['price'], product['image'], product['description'])
    st.session_state.show_checkout = True
    st.success(f"✨ Added {product['name']} to cart!")

def get_cart_total():
    items = st.session_state.db.get_cart_items(st.session_state.user_id)
    return sum(item[2] * item[5] for item in items)

def simulate_payment(total):
    import time
    time.sleep(2)
    transaction_id = f"TXN{random.randint(100000, 999999)}"
    card_last4 = random.randint(1000, 9999)
    return {
        'success': True,
        'transaction_id': transaction_id,
        'amount': total,
        'card_last4': card_last4,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def checkout():
    items = st.session_state.db.get_cart_items(st.session_state.user_id)
    if items:
        total = get_cart_total()
        payment_result = simulate_payment(total)
        if payment_result['success']:
            order_items = [{"name": item[1], "price": item[2], "qty": item[5]} for item in items]
            order_id = st.session_state.db.create_order(st.session_state.user_id, order_items, total)
            st.session_state.db.clear_cart(st.session_state.user_id)
            st.session_state.show_checkout = False
            return order_id, total, payment_result
    return None, 0, None

st.markdown(f'<h1 class="main-header">✨ {APP_NAME}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="tagline">{APP_TAGLINE}</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("#### 🎭 Your Assistant")
    avatar_style = st.selectbox("Avatar Style", AVATAR_STYLES, index=0, label_visibility="collapsed")
    avatar_map = {"Stylized Futuristic Human": "🤖", "Realistic Human": "👨‍💼", "Anime Style": "😊", "Cartoon Style": "🎭", "Minimalist Icon": "●"}
    avatar_emoji = avatar_map.get(avatar_style, "🤖")
    st.markdown(f'<div class="assistant-avatar">{avatar_emoji}</div>', unsafe_allow_html=True)
    st.caption(f"💫 {avatar_style}")
    st.divider()
    
    st.markdown("#### 🎯 Assistant Mode")
    for mode_key, mode_info in MODES.items():
        is_active = mode_key == st.session_state.current_mode
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"### {mode_info['icon']}")
        with col2:
            if st.button(mode_info['name'], key=f"btn_{mode_key}", use_container_width=True, type="primary" if is_active else "secondary"):
                switch_mode(mode_key)
                st.rerun()
    
    current_mode_info = MODES[st.session_state.current_mode]
    st.markdown(f'<div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); padding: 15px; border-radius: 12px; border-left: 4px solid #667eea; margin: 10px 0;">📝 {current_mode_info["description"]}</div>', unsafe_allow_html=True)
    st.divider()
    
    cart_items = st.session_state.db.get_cart_items(st.session_state.user_id)
    st.markdown(f"#### 🛒 Shopping Cart ({len(cart_items)})")
    
    if cart_items:
        cart_total = get_cart_total()
        st.markdown(f'<div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%); padding: 20px; border-radius: 15px; text-align: center;"><div style="font-size:2.5rem;font-weight:700;color:#667eea;">${cart_total:.2f}</div></div>', unsafe_allow_html=True)
        st.write("")
        if st.button("💳 Checkout Now", use_container_width=True, type="primary"):
            st.session_state.show_checkout = True
            st.session_state.cart_open = False
            st.rerun()
    else:
        st.info("🛒 Your cart is empty")
    
    st.divider()
    orders = st.session_state.db.get_user_orders(st.session_state.user_id, limit=3)
    if orders:
        st.markdown("#### 📦 Recent Orders")
        for order in orders:
            order_id, items, total, status, created = order
            st.markdown(f'<div class="cart-item">Order #{order_id}<br><strong>${total:.2f}</strong></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"## {MODES[st.session_state.current_mode]['icon']} {MODES[st.session_state.current_mode]['name']} Mode")
    
    if not st.session_state.messages:
        load_conversation_history()
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    prompt = st.chat_input("💬 Message NUVEXA...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        save_message("user", prompt)
        
        if st.session_state.current_mode == 'shopping':
            query = prompt.lower()
            products = st.session_state.shopping_engine.search_products(query)
            if products:
                st.session_state.search_results = products
                st.session_state.show_products = True
                response = f"🛍️ Found {len(products)} great options for you! Check them out on the right side →"
            else:
                response = "🛍️ Hmm, I couldn't find that product. Try: chocolate, candlestick, or coconut water!"
        else:
            conversation_history = [(msg["role"], msg["content"]) for msg in st.session_state.messages[:-1]]
            response = st.session_state.ai_assistant.chat(prompt, conversation_history)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        save_message("assistant", response)
        st.rerun()

with col2:
    if st.session_state.show_checkout and get_cart_total() > 0:
        st.markdown("### 💳 Checkout")
        cart_items = st.session_state.db.get_cart_items(st.session_state.user_id)
        
        st.markdown('<div class="payment-box">', unsafe_allow_html=True)
        st.markdown("#### 🎉 Complete Your Order")
        
        for item in cart_items:
            cart_id, name, price, image, description, qty = item
            st.markdown(f"{image} **{name}** - ${price:.2f} × {qty}")
        
        st.divider()
        total = get_cart_total()
        st.markdown(f'<div style="font-size: 2.5rem; font-weight: 700; color: #10b981; text-align: center; margin: 20px 0;">${total:.2f}</div>', unsafe_allow_html=True)
        
        st.markdown("#### Payment Method")
        st.text_input("Card Number", value="4242 4242 4242 4242", disabled=True, key="card_num")
        col_exp, col_cvv = st.columns(2)
        with col_exp:
            st.text_input("Expiry", value="12/25", disabled=True, key="exp")
        with col_cvv:
            st.text_input("CVV", value="123", disabled=True, key="cvv")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button(f"🎉 COMPLETE PURCHASE ${total:.2f}", key="complete_purchase", use_container_width=True, type="primary"):
            with st.spinner("Processing payment..."):
                order_id, total_paid, payment = checkout()
                if order_id and payment:
                    st.success(f"✅ Payment Successful!")
                    st.balloons()
                    st.markdown(f"""
                    **Order #{order_id} Confirmed!**
                    
                    💳 Card ending in {payment['card_last4']}  
                    💰 Amount: ${payment['amount']:.2f}  
                    📋 Transaction: {payment['transaction_id']}  
                    ⏰ {payment['timestamp']}
                    
                    Thank you for shopping with NUVEXA! 🎉
                    """)
                    st.rerun()
        
        if st.button("← Back to Shopping", key="back_shop"):
            st.session_state.show_checkout = False
            st.rerun()
    
    elif st.session_state.show_products and st.session_state.search_results:
        st.markdown("### 🛍️ Products Found")
        
        for idx, product in enumerate(st.session_state.search_results):
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            
            if 'images' in product and len(product['images']) >= 2:
                col_img1, col_img2 = st.columns(2)
                with col_img1:
                    try:
                        st.image(product['images'][0], use_container_width=True)
                    except:
                        st.markdown(f'<div style="font-size:3rem;text-align:center;">{product["image"]}</div>', unsafe_allow_html=True)
                with col_img2:
                    try:
                        st.image(product['images'][1], use_container_width=True)
                    except:
                        st.markdown(f'<div style="font-size:3rem;text-align:center;">{product["image"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="font-size:4rem;text-align:center;margin:20px;">{product["image"]}</div>', unsafe_allow_html=True)
            
            st.markdown(f"### {product['name']}")
            st.write(product['description'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**💰 ${product['price']:.2f}**")
            with col2:
                st.markdown(f"⭐ {product['rating']}")
            with col3:
                st.markdown(f"📍 {product['source']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button(f"🛒 Add to Cart - ${product['price']:.2f}", key=f"add_prod_{idx}", type="primary", use_container_width=True):
                add_to_cart(product)
                st.rerun()
            
            st.write("")
    
    else:
        st.markdown("### 💡 Quick Tips")
        tips = {
            'assistant': ["📅 Help me plan my day", "🔍 Research any topic", "💼 Get project advice"],
            'shopping': ["🛍️ Try: chocolate, candlestick, coconut water", "⚖️ Compare options", "🛒 Complete checkout"],
            'therapist': ["💭 Share feelings", "❤️ Process emotions", "👂 Get support"],
            'builder': ["🏗️ Plan projects", "📋 Get material lists", "📊 Cost estimates"]
        }
        for tip in tips.get(st.session_state.current_mode, []):
            st.markdown(f'<div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); padding: 15px; border-radius: 12px; border-left: 4px solid #667eea; margin: 10px 0;">{tip}</div>', unsafe_allow_html=True)

st.divider()
st.markdown('<p style="text-align: center; color: #8b92a8; font-size: 0.9rem;">✨ NUVEXA v1.0 - Demo Payment System | Powered by OpenAI 🚀</p>', unsafe_allow_html=True)
