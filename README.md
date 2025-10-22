# E-Commerce-Database
A e-commerce database created using MySQL 
# 🛍️ E-Commerce Database Management System

A complete **E-Commerce Store Management** application built with **Python (Streamlit)** and **MySQL**, featuring interactive dashboards, real-time data visualization, and a simple admin interface for managing users, products, orders, and inventory.

---

## 🚀 Project Overview

This project demonstrates a **relational database design and implementation** for a real-world **E-Commerce Store** use case.  
It provides both the **backend database schema (MySQL)** and a **front-end UI (Streamlit)** for managing data.

### 🎯 Key Features
- **Database Design** with multiple related tables (Users, Products, Orders, etc.)
- **Data Integrity** through Primary and Foreign Key constraints
- **Streamlit UI** for CRUD operations and business management
- **Interactive Dashboard** built with **Plotly** for:
  - Total sales and orders
  - Active users
  - Top-selling products
  - Inventory levels
  - Daily sales trends
---
## Database Schema

### Database Name:
`ecommerce_db`

### Core Tables:
| Table | Description |
|--------|-------------|
| `users` | Stores user login credentials and status |
| `customer_profiles` | Additional details for each customer |
| `categories` | Product categories and hierarchy |
| `suppliers` | Vendor and supplier information |
| `products` | Product details including SKU, category, supplier |
| `inventory` | Tracks stock quantity for each product |
| `orders` | Customer order summary |
| `order_items` | Individual product details per order |
| `payments` | Payment transactions for each order |
| `reviews` | Customer reviews and product feedback |

### Relationships:
- **One-to-Many:** Users → Orders  
- **Many-to-Many:** Products ↔ Orders (via `order_items`)  
- **One-to-One:** Users ↔ Customer Profiles  
- **One-to-Many:** Categories → Products  
- **One-to-Many:** Suppliers → Products  
---
## ⚙️ Installation Guide
### Prerequisites
- Python 3.9+
- MySQL Server
- pip package manager

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Gloriamuema/E-Commerce-Database.git
cd E-Commerce-Database

Create the MySQL Database
Run the provided SQL schema file

## Configure Database Connection
## Edit the connection credentials in app.py:
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",                # Your MySQL username
        password="your_password",   # Your MySQL password
        database="ecommerce_db"
    )


Install Dependencies
pip install streamlit mysql-connector-python pandas plotly

Run the Application
python -m streamlit run app.py

Dashboard Preview
Available Insights:

💰 Total Sales
🧾 Total Orders
👥 Active Users
🏆 Top 5 Best-Selling Products
📦 Current Inventory Levels
📈 Sales Trend (Past 7 Days)

Project Structure
📁 ecommerce-dbms
│
├── app.py                 # Streamlit user interface
├── ecommerce_db.sql  # MySQL database schema
├── README.md              # Project documentation


How to Use

Navigate using the sidebar menu:

📊 Dashboard: View KPIs and visual insights.
📋 View Tables: Inspect any table’s data.
👤 Add User: Create new users.
📁 Add Category: Manage product categories.
📦 Add Product: Add and stock new products.
🧾 Manage Orders: Create new customer orders.


Input data and submit using Streamlit forms.
All data changes are saved directly into MySQL.

Technologies Used

| Category            | Technology     |
| ------------------- | -------------- |
| **Frontend/UI**     | Streamlit      |
| **Backend**         | Python         |
| **Database**        | MySQL          |
| **Visualization**   | Plotly, Pandas |
| **Version Control** | Git & GitHub   |


Future Improvements
Add user authentication and login
Include sales forecasting using AI models
Add email notifications for orders
Support CSV import/export for data management

Author
Gloria Muema