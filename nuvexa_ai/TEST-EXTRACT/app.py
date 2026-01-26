import streamlit as st
from datetime import datetime
import json
from config import APP_NAME, APP_TAGLINE, MODES, AVATAR_STYLES
from database import NuvexaDB
from assistant import NuvexaAssistant
from shopping import ShoppingEngine

st.set_page_config(page_title=APP_NAME, page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.main-header { font-size: 3rem; font-weight: bold; background: linear-gradient(90deg, #00D9FF 0%, #7B2FFF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
.assistant-avatar { font-size: 4rem; text-align: center; margin: 20px 0; }
.product-card { border: 1px solid #444; border-radius: 10px; padding: 15px; margin: 10px 0; background-color: #1a1a1a; }
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
    st.success(f"Added to cart!")

def get_cart_total():
    items = st.session_state.db.get_cart_items(st.session_state.user_id)
    return sum(item[2] * item[5] for item in items)

def checkout():
    items = st.session_state.db.get_cart_items(st.session_state.user_id)
    if items:
        total = get_cart_total()
        order_items = [{"name": item[1], "price": item[2], "qty": item[5]} for item in items]
        order_id = st.session_state.db.create_order(st.session_state.user_id, order_items, total)
        st.session_state.db.clear_cart(st.session_state.user_id)
        return order_id, total
    return None, 0

st.markdown(f'<h1 class="main-header">{APP_NAME}</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Settings")
    avatar_style = st.selectbox("Avatar", AVATAR_STYLES, index=0)
    avatar_emoji = "🤖"
    st.markdown(f'<div class="assistant-avatar">{avatar_emoji}</div>', unsafe_allow_html=True)
    st.divider()
    st.subheader("Mode")
    for mode_key, mode_info in MODES.items():
        is_active = mode_key == st.session_state.current_mode
        if st.button(f"{mode_info['icon']} {mode_info['name']}", key=f"btn_{mode_key}", type="primary" if is_active else "secondary"):
            switch_mode(mode_key)
            st.rerun()
    st.divider()
    cart_items = st.session_state.db.get_cart_items(st.session_state.user_id)
    st.subheader(f"Cart ({len(cart_items)})")
    if cart_items:
        st.metric("Total", f"${get_cart_total():.2f}")
        if st.button("Checkout", type="primary"):
            order_id, total = checkout()
            if order_id:
                st.success(f"Order placed!")
                st.rerun()

col1, col2 = st.columns([2, 1])

with col1:
    st.header(f"{MODES[st.session_state.current_mode]['name']} Mode")
    if not st.session_state.messages:
        load_conversation_history()
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    prompt = st.chat_input("Message NUVEXA...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        save_message("user", prompt)
        if st.session_state.current_mode == 'shopping' and st.session_state.ai_assistant.analyze_shopping_intent(prompt):
            product_query = st.session_state.ai_assistant.extract_product_query(prompt)
            st.session_state.search_results = st.session_state.shopping_engine.search_products(product_query)
            st.session_state.show_products = True
        conversation_history = [(msg["role"], msg["content"]) for msg in st.session_state.messages[:-1]]
        response = st.session_state.ai_assistant.chat(prompt, conversation_history)
        st.session_state.messages.append({"role": "assistant", "content": response})
        save_message("assistant", response)
        st.rerun()

with col2:
    if st.session_state.show_products and st.session_state.search_results:
        st.subheader("Products")
        for idx, product in enumerate(st.session_state.search_results):
            st.markdown(f"### {product['image']} {product['name']}")
            st.write(f"{product['description']}")
            st.write(f"**${product['price']:.2f}** - {product['rating']} ⭐ - {product['source']}")
            if st.button("Add to Cart", key=f"add_{idx}"):
                add_to_cart(product)
                st.rerun()
            st.divider()
    else:
        st.subheader("Tips")
        st.caption("Ask questions, shop for products, or get advice!")

st.divider()
st.caption("NUVEXA v1.0 - Your Living AI Assistant")
