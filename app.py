import streamlit as st
from datetime import datetime
import json
import logging
from typing import Optional, Tuple
from config import APP_NAME, APP_TAGLINE, MODES, AVATAR_STYLES
from database import NuvexaDB
from assistant import NuvexaAssistant
from shopping import ShoppingEngine

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title=APP_NAME, 
    page_icon="🤖", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Enhanced CSS styling
st.markdown("""
<style>
    .main-header { 
        font-size: 3rem; 
        font-weight: bold; 
        background: linear-gradient(90deg, #00D9FF 0%, #7B2FFF 100%); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        text-align: center; 
        margin-bottom: 0.5rem;
    }
    .assistant-avatar { 
        font-size: 4rem; 
        text-align: center; 
        margin: 20px 0; 
    }
    .product-card { 
        border: 1px solid #444; 
        border-radius: 10px; 
        padding: 15px; 
        margin: 10px 0; 
        background-color: #1a1a1a;
        transition: transform 0.2s;
    }
    .product-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 217, 255, 0.2);
    }
    .cart-item {
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        background-color: #1e1e1e;
    }
    .stButton>button {
        width: 100%;
    }
    .error-message {
        color: #ff6b6b;
        padding: 10px;
        border-radius: 5px;
        background-color: #2a1a1a;
    }
    .success-message {
        color: #51cf66;
        padding: 10px;
        border-radius: 5px;
        background-color: #1a2a1a;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
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
    st.session_state.show_order_history = False
    
    # Check API key on startup
    if not st.session_state.ai_assistant.client:
        api_key_value = st.session_state.ai_assistant.api_key if hasattr(st.session_state.ai_assistant, 'api_key') else None
        if api_key_value and api_key_value != 'your-openai-api-key-here':
            st.error(f"⚠️ API key found but client initialization failed. Key starts with: {api_key_value[:10]}...")
        else:
            st.error("⚠️ OpenAI API key not configured. Please check your .env file in the project folder.")
            st.info("💡 Make sure your .env file contains: `OPENAI_API_KEY=sk-your-key-here`")

def load_conversation_history():
    """Load conversation history from database."""
    history = st.session_state.db.get_conversation_history(
        st.session_state.user_id, 
        st.session_state.current_mode
    )
    st.session_state.messages = [
        {"role": role, "content": content} 
        for role, content in history
    ]

def save_message(role: str, content: str):
    """Save message to database."""
    st.session_state.db.save_message(
        st.session_state.user_id, 
        st.session_state.current_mode, 
        content, 
        role
    )

def switch_mode(new_mode: str):
    """Switch to a new mode."""
    st.session_state.current_mode = new_mode
    st.session_state.ai_assistant.set_mode(new_mode)
    load_conversation_history()
    st.session_state.show_products = False
    st.session_state.search_results = []

def add_to_cart(product: dict):
    """Add product to cart."""
    result = st.session_state.db.add_to_cart(
        st.session_state.user_id, 
        product['name'], 
        product['price'], 
        product.get('image', ''), 
        product.get('description', '')
    )
    if result:
        st.success(f"✅ Added {product['name']} to cart!")
    else:
        st.error("❌ Failed to add item to cart. Please try again.")

def get_cart_total() -> float:
    """Calculate total cart value."""
    items = st.session_state.db.get_cart_items(st.session_state.user_id)
    return sum(item[2] * item[5] for item in items)

def get_cart_item_count() -> int:
    """Get total number of items in cart."""
    items = st.session_state.db.get_cart_items(st.session_state.user_id)
    return sum(item[5] for item in items)

def checkout() -> Tuple[Optional[int], float]:
    """Process checkout."""
    items = st.session_state.db.get_cart_items(st.session_state.user_id)
    if items:
        total = get_cart_total()
        order_items = [
            {"name": item[1], "price": item[2], "qty": item[5]} 
            for item in items
        ]
        order_id = st.session_state.db.create_order(
            st.session_state.user_id, 
            order_items, 
            total
        )
        if order_id:
            st.session_state.db.clear_cart(st.session_state.user_id)
            return order_id, total
    return None, 0

# Main header
st.markdown(f'<h1 class="main-header">{APP_NAME}</h1>', unsafe_allow_html=True)
st.caption(f"*{APP_TAGLINE}*")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Avatar selection with persistence
    current_avatar = st.session_state.db.get_avatar_style(st.session_state.user_id)
    avatar_index = AVATAR_STYLES.index(current_avatar) if current_avatar in AVATAR_STYLES else 0
    avatar_style = st.selectbox(
        "Avatar Style", 
        AVATAR_STYLES, 
        index=avatar_index,
        key="avatar_select"
    )
    
    if avatar_style != current_avatar:
        if st.session_state.db.update_avatar_style(st.session_state.user_id, avatar_style):
            st.success("Avatar style updated!")
            st.rerun()
    
    avatar_emoji = "🤖"
    st.markdown(f'<div class="assistant-avatar">{avatar_emoji}</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Mode selection
    st.subheader("🎯 Mode")
    for mode_key, mode_info in MODES.items():
        is_active = mode_key == st.session_state.current_mode
        button_type = "primary" if is_active else "secondary"
        if st.button(
            f"{mode_info['icon']} {mode_info['name']}", 
            key=f"btn_{mode_key}", 
            type=button_type,
            use_container_width=True
        ):
            switch_mode(mode_key)
            st.rerun()
        if is_active:
            st.caption(f"*{mode_info['description']}*")
    
    st.divider()
    
    # Cart section
    cart_items = st.session_state.db.get_cart_items(st.session_state.user_id)
    cart_count = get_cart_item_count()
    st.subheader(f"🛒 Cart ({cart_count} items)")
    
    if cart_items:
        st.metric("Total", f"${get_cart_total():.2f}")
        
        # Expandable cart view
        with st.expander("View Cart", expanded=st.session_state.cart_open):
            for item in cart_items:
                cart_id, name, price, image, desc, qty = item
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{name}**")
                        st.caption(f"${price:.2f} × {qty}")
                    with col2:
                        new_qty = st.number_input(
                            "Qty", 
                            min_value=1, 
                            max_value=99, 
                            value=qty, 
                            key=f"qty_{cart_id}",
                            label_visibility="collapsed"
                        )
                        if new_qty != qty:
                            st.session_state.db.update_cart_quantity(cart_id, new_qty)
                            st.rerun()
                    with col3:
                        if st.button("🗑️", key=f"remove_{cart_id}", help="Remove item"):
                            st.session_state.db.remove_from_cart(cart_id)
                            st.success("Item removed!")
                            st.rerun()
                    st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛒 View Cart", use_container_width=True):
                st.session_state.cart_open = not st.session_state.cart_open
                st.rerun()
        with col2:
            if st.button("💳 Checkout", type="primary", use_container_width=True):
                with st.spinner("Processing order..."):
                    order_id, total = checkout()
                    if order_id:
                        st.success(f"✅ Order #{order_id} placed! Total: ${total:.2f}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Failed to process order. Please try again.")
    else:
        st.caption("Your cart is empty")
    
    st.divider()
    
    # Order history
    if st.button("📜 Order History", use_container_width=True):
        st.session_state.show_order_history = not st.session_state.show_order_history
    
    if st.session_state.show_order_history:
        orders = st.session_state.db.get_user_orders(st.session_state.user_id, limit=10)
        if orders:
            st.subheader("Recent Orders")
            for order in orders:
                order_id, items_json, total, status, created_at = order
                items = json.loads(items_json)
                with st.expander(f"Order #{order_id} - ${total:.2f} - {created_at[:10]}"):
                    for item in items:
                        st.write(f"• {item['name']} × {item['qty']} - ${item['price']:.2f}")
        else:
            st.caption("No orders yet")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header(f"{MODES[st.session_state.current_mode]['icon']} {MODES[st.session_state.current_mode]['name']} Mode")
    
    # Load conversation history if empty
    if not st.session_state.messages:
        load_conversation_history()
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    prompt = st.chat_input("Message NUVEXA...")
    
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        save_message("user", prompt)
        
        # Check for shopping intent in shopping mode
        if (st.session_state.current_mode == 'shopping' and 
            st.session_state.ai_assistant.analyze_shopping_intent(prompt)):
            product_query = st.session_state.ai_assistant.extract_product_query(prompt)
            st.session_state.search_results = st.session_state.shopping_engine.search_products(product_query)
            st.session_state.show_products = True
        
        # Get AI response - this will be displayed on next rerun
        conversation_history = [
            (msg["role"], msg["content"]) 
            for msg in st.session_state.messages[:-1]
        ]
        
        # Show spinner and get response
        with st.spinner("🤔 NUVEXA is thinking..."):
            try:
                response = st.session_state.ai_assistant.chat(prompt, conversation_history)
                
                if not response:
                    response = "Error: No response received. Please check your API key in .env file."
                elif response.startswith("Error:"):
                    # Keep error message as-is but ensure it's added to chat
                    pass
                
                # Always add response to messages (even errors) so user sees what happened
                st.session_state.messages.append({"role": "assistant", "content": response})
                save_message("assistant", response)
                
            except Exception as e:
                # Catch any unexpected errors during the API call
                error_msg = f"Error: {str(e)}. Please check your API key in .env file and ensure it's valid."
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                save_message("assistant", error_msg)
                logger.error(f"Unexpected error in chat: {str(e)}")
        
        # Rerun to display the response
        st.rerun()

with col2:
    if st.session_state.show_products and st.session_state.search_results:
        st.subheader("🛍️ Products")
        st.caption(f"Found {len(st.session_state.search_results)} result(s)")
        
        for idx, product in enumerate(st.session_state.search_results):
            with st.container():
                st.markdown(f"### {product.get('image', '📦')} {product['name']}")
                st.write(f"{product.get('description', 'No description available')}")
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**${product['price']:.2f}**")
                    st.caption(f"{product.get('rating', 0)} ⭐ | {product.get('source', 'Unknown')}")
                with col2:
                    if st.button("➕ Add", key=f"add_{idx}", use_container_width=True):
                        add_to_cart(product)
                        st.rerun()
                
                if idx < len(st.session_state.search_results) - 1:
                    st.divider()
    else:
        st.subheader("💡 Tips")
        mode_tips = {
            'assistant': [
                "Ask me anything!",
                "I can help with planning and research",
                "Try asking about current events or general knowledge"
            ],
            'shopping': [
                "Say 'I want to buy...' or 'Find me...'",
                "I'll search for products and add them to your cart",
                "Try: 'buy coconut water' or 'find headphones'"
            ],
            'therapist': [
                "Share what's on your mind",
                "I'm here to listen and support you",
                "No judgment, just understanding"
            ],
            'builder': [
                "Describe your project",
                "I'll help break it down into steps",
                "Ask about parts, materials, or planning"
            ]
        }
        
        tips = mode_tips.get(st.session_state.current_mode, ["Ask questions, shop for products, or get advice!"])
        for tip in tips:
            st.write(f"• {tip}")

# Footer
st.divider()
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.caption(f"**{APP_NAME}** v1.0")
with footer_col2:
    st.caption("Your Living AI Assistant")
with footer_col3:
    if st.button("🔄 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.db.clear_cart(st.session_state.user_id)
        st.success("Chat cleared!")
        st.rerun()
