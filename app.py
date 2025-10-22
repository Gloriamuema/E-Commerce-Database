import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # change this
        password="1234",  # change this
        database="ecommerce_db"
    )

def fetch_data(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def run_query(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    conn.close()

# -----------------------------
# STREAMLIT CONFIG
# -----------------------------
st.set_page_config(page_title="E-Commerce Admin Dashboard", layout="wide")
st.title("🛍️ E-Commerce Store Database Management")
st.sidebar.header("Navigation")

menu = st.sidebar.selectbox(
    "Select Section",
    [
        "📊 Dashboard",
        "📋 View Tables",
        "👤 Add User",
        "📁 Add Category",
        "📦 Add Product",
        "🧾 Manage Orders"
    ]
)

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
if menu == "📊 Dashboard":
    st.subheader("📈 Business Overview")

    # --- Metrics ---
    total_sales = fetch_data("SELECT IFNULL(SUM(total_amount), 0) AS total FROM orders")["total"][0]
    total_orders = fetch_data("SELECT COUNT(*) AS cnt FROM orders")["cnt"][0]
    active_users = fetch_data("SELECT COUNT(*) AS cnt FROM users WHERE is_active = 1")["cnt"][0]
    total_products = fetch_data("SELECT COUNT(*) AS cnt FROM products")["cnt"][0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Sales (USD)", f"${total_sales:,.2f}")
    col2.metric("🧾 Total Orders", total_orders)
    col3.metric("👥 Active Users", active_users)
    col4.metric("📦 Products", total_products)

    st.markdown("---")

    # --- Sales Trend ---
    st.subheader("📅 Sales Trend (Past 7 Days)")
    query_sales_trend = """
        SELECT DATE(created_at) AS date, SUM(total_amount) AS total
        FROM orders
        WHERE created_at >= CURDATE() - INTERVAL 7 DAY
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at);
    """
    df_sales = fetch_data(query_sales_trend)
    if not df_sales.empty:
        chart = px.line(df_sales, x="date", y="total", markers=True, title="Daily Sales Trend")
        st.plotly_chart(chart, use_container_width=True)
    else:
        st.info("No sales data for the past 7 days.")

    # --- Top Selling Products ---
    st.subheader("🏆 Top Selling Products")
    query_top_products = """
        SELECT p.name, SUM(oi.quantity) AS total_sold
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.name
        ORDER BY total_sold DESC
        LIMIT 5;
    """
    df_top = fetch_data(query_top_products)
    if not df_top.empty:
        bar = px.bar(df_top, x="name", y="total_sold", title="Top 5 Best-Selling Products", text="total_sold")
        st.plotly_chart(bar, use_container_width=True)
    else:
        st.info("No product sales data available.")

    # --- Inventory Overview ---
    st.subheader("📦 Inventory Levels")
    df_inventory = fetch_data("""
        SELECT p.name, i.quantity
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        ORDER BY i.quantity ASC;
    """)
    if not df_inventory.empty:
        inv_chart = px.bar(df_inventory, x="name", y="quantity", title="Product Inventory Levels")
        st.plotly_chart(inv_chart, use_container_width=True)
    else:
        st.info("No inventory data available.")

# -----------------------------
# EXISTING PAGES BELOW
# -----------------------------
elif menu == "📋 View Tables":
    st.subheader("📊 View Database Tables")

    tables = [
        "users", "customer_profiles", "categories", "suppliers",
        "products", "inventory", "orders", "order_items", "payments", "reviews"
    ]

    selected_table = st.selectbox("Choose a table to view:", tables)
    df = fetch_data(f"SELECT * FROM {selected_table} LIMIT 100")
    st.dataframe(df)

elif menu == "👤 Add User":
    st.subheader("👤 Add New User")

    email = st.text_input("Email")
    password_hash = st.text_input("Password (hashed or plain for testing)")
    is_active = st.checkbox("Active", value=True)

    if st.button("Add User"):
        if email and password_hash:
            query = "INSERT INTO users (email, password_hash, is_active) VALUES (%s, %s, %s)"
            run_query(query, (email, password_hash, int(is_active)))
            st.success(f"✅ User {email} added successfully!")
        else:
            st.error("Please fill all fields.")

elif menu == "📁 Add Category":
    st.subheader("📁 Add Product Category")

    name = st.text_input("Category Name")
    slug = st.text_input("Slug (unique identifier)")
    description = st.text_area("Description")
    parent_id = st.number_input("Parent Category ID (optional)", min_value=0, step=1)

    if st.button("Add Category"):
        query = "INSERT INTO categories (name, slug, description, parent_id) VALUES (%s, %s, %s, %s)"
        run_query(query, (name, slug, description, parent_id if parent_id > 0 else None))
        st.success(f"✅ Category '{name}' added successfully!")

elif menu == "📦 Add Product":
    st.subheader("📦 Add New Product")

    name = st.text_input("Product Name")
    sku = st.text_input("SKU (unique)")
    category_df = fetch_data("SELECT category_id, name FROM categories")
    supplier_df = fetch_data("SELECT supplier_id, name FROM suppliers")

    category_id = st.selectbox("Category", category_df["category_id"]) if not category_df.empty else None
    supplier_id = st.selectbox("Supplier", supplier_df["supplier_id"]) if not supplier_df.empty else None
    price = st.number_input("Price (USD)", min_value=0.0, format="%.2f")
    stock = st.number_input("Initial Stock", min_value=0, step=1)
    description = st.text_area("Description")

    if st.button("Add Product"):
        query = """
        INSERT INTO products (sku, name, description, category_id, supplier_id, price)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        run_query(query, (sku, name, description, category_id, supplier_id, price))
        product_df = fetch_data("SELECT LAST_INSERT_ID() AS id")
        product_id = product_df.iloc[0]["id"]

        run_query("INSERT INTO inventory (product_id, quantity) VALUES (%s, %s)", (product_id, stock))
        st.success(f"✅ Product '{name}' added successfully!")

elif menu == "🧾 Manage Orders":
    st.subheader("🧾 Manage Orders")

    users_df = fetch_data("SELECT user_id, email FROM users")
    products_df = fetch_data("SELECT product_id, name, price FROM products")

    if users_df.empty or products_df.empty:
        st.warning("⚠️ Please ensure there are users and products before creating orders.")
    else:
        user_id = st.selectbox("Select Customer", users_df["user_id"])
        product_id = st.selectbox("Select Product", products_df["product_id"])
        quantity = st.number_input("Quantity", min_value=1, step=1)

        if st.button("Create Order"):
            order_number = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            price = products_df.loc[products_df["product_id"] == product_id, "price"].values[0]
            total = price * quantity

            run_query("INSERT INTO orders (user_id, order_number, total_amount) VALUES (%s, %s, %s)",
                      (user_id, order_number, total))

            order_df = fetch_data("SELECT LAST_INSERT_ID() AS id")
            order_id = order_df.iloc[0]["id"]

            run_query("INSERT INTO order_items (order_id, product_id, quantity, item_price) VALUES (%s, %s, %s, %s)",
                      (order_id, product_id, quantity, price))

            run_query("UPDATE inventory SET quantity = quantity - %s WHERE product_id = %s", (quantity, product_id))
            st.success(f"✅ Order {order_number} created successfully!")

st.markdown("---")
st.caption("E-Commerce DB UI | Streamlit + MySQL | © Gloria Muema 2025")
