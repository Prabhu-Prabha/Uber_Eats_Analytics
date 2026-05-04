import streamlit as st
import pandas as pd
import mysql.connector

# -------------------- DATABASE CONNECTION --------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="project_i",
        port = "3306"
    )

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Uber Eats Analytics Dashboard",
    layout="wide"
)

st.title("Uber Eats Analytics Dashboard")


tab1, tab2, tab3 = st.tabs([
    "📊 Dashboard",
    "📈 Business Q&A",
    "🛒 Orders Analytics"
])

# TAB 1: DASHBOARD PAGE (SQL-ONLY FILTERING)

with tab1:
    st.header("📊 Interactive Dashboard")

    conn = get_connection()
    mycursor = conn.cursor()

    # Filters
    location = st.selectbox(
        "Select Location",
        ["All"] + pd.read_sql("SELECT DISTINCT location FROM uber_explore", conn)["location"].tolist()
    )

    price_range = st.selectbox(
        "Select Price Segment",
        ["All", "Low", "Mid", "Premium"]
    )

    online_order = st.selectbox(
        "Online Order Available?",
        ["All", 1, 0]
    )

    # SQL query construction
    query = """
    SELECT name, location, rate, approx_cost_for_two_people,
           online_order, book_table, cuisines
    FROM uber_explore
    WHERE 1=1
    """

    if location != "All":
        query += f" AND location = '{location}'"

    if online_order != "All":
        query += f" AND online_order = {online_order}"

    if price_range != "All":
        if price_range == "Low":
            query += " AND approx_cost_for_two_people < 300"
        elif price_range == "Mid":
            query += " AND approx_cost_for_two_people BETWEEN 300 AND 700"
        else:
            query += " AND approx_cost_for_two_people > 700"

    df = pd.read_sql(query, conn)
    st.dataframe(df)

    conn.close()

# TAB 2: BUSINESS Q&A PAGE (10 PREDEFINED QUESTIONS)

with tab2:
    st.header("📈 Business Questions & Insights")

    conn = get_connection()

    questions = {
        "Top 10 Locations by Average Rating": """
            SELECT location,
                   ROUND(AVG(rate),2) AS avg_rating,
                   COUNT(*) AS restaurant_count
            FROM uber_explore
            GROUP BY location
            HAVING COUNT(*) >= 10
            ORDER BY avg_rating DESC
            LIMIT 10;
        """,

        "Over-saturated Locations": """
            SELECT location,
                   COUNT(*) AS restaurant_count
            FROM uber_explore
            GROUP BY location
            ORDER BY restaurant_count DESC;
        """,

        "Online Order vs Rating": """
            SELECT online_order,
                   ROUND(AVG(rate),2) AS avg_rating
            FROM uber_explore
            GROUP BY online_order;
        """,

        "Table Booking vs Rating": """
            SELECT book_table,
                   ROUND(AVG(rate),2) AS avg_rating
            FROM uber_explore
            GROUP BY book_table;
        """,

        "Best Price Range by Rating": """
            SELECT
              CASE
                WHEN approx_cost_for_two_people < 300 THEN 'Low'
                WHEN approx_cost_for_two_people BETWEEN 300 AND 700 THEN 'Mid'
                ELSE 'Premium'
              END AS price_range,
              ROUND(AVG(rate),2) AS avg_rating
            FROM uber_explore
            GROUP BY price_range;
        """,

        "Top Cuisines by Count": """
            SELECT cuisines,
                   COUNT(*) AS restaurant_count
            FROM uber_explore
            GROUP BY cuisines
            ORDER BY restaurant_count DESC
            LIMIT 10;
        """,

        "Top Rated Cuisines": """
            SELECT cuisines,
                   ROUND(AVG(rate),2) AS avg_rating
            FROM uber_explore
            GROUP BY cuisines
            HAVING COUNT(*) >= 5
            ORDER BY avg_rating DESC
            LIMIT 10;
        """,

        "High Demand but Low Rating Locations": """
            SELECT location,
                   COUNT(*) AS restaurant_count,
                   ROUND(AVG(rate),2) AS avg_rating
            FROM uber_explore
            GROUP BY location
            HAVING restaurant_count > 50 AND avg_rating < 4.0;
        """,

        "Online + Table Booking Performance": """
            SELECT online_order, book_table,
                   ROUND(AVG(rate),2) AS avg_rating
            FROM uber_explore
            GROUP BY online_order, book_table;
        """,

        "Top Restaurants by Rating": """
            SELECT name, rate, location
            FROM uber_explore
            WHERE rate >= 4.5
            ORDER BY rate DESC
            LIMIT 10;
        """
    }

    selected_q = st.selectbox("Select Business Question", list(questions.keys()))
    df = pd.read_sql(questions[selected_q], conn)
    st.dataframe(df)

    conn.close()

# TAB 3: ORDERS DATA ANALYTICS

with tab3:
    st.header("🛒 Orders Data Analytics")

    conn = get_connection()

    order_questions = {
        "Top 10 Revenue Generating Restaurants": """
            SELECT restaurant_name,
                   ROUND(SUM(order_value),2) AS total_revenue
            FROM orders
            GROUP BY restaurant_name
            ORDER BY total_revenue DESC
            LIMIT 10;
        """,

        "Average Order Value by Payment Method": """
            SELECT payment_method,
                   ROUND(AVG(order_value),2) AS avg_order_value,
                   COUNT(*) AS total_orders
            FROM orders
            GROUP BY payment_method;
        """,

        "Discount Impact on Order Value": """
            SELECT discount_used,
                   ROUND(AVG(order_value),2) AS avg_order_value,
                   COUNT(*) AS total_orders
            FROM orders
            GROUP BY discount_used;
        """,

        "Daily Revenue Trend": """
            SELECT order_date,
                   ROUND(SUM(order_value),2) AS daily_revenue
            FROM orders
            GROUP BY order_date
            ORDER BY order_date;
        """,

        "Top Restaurants by Average Order Value": """
            SELECT restaurant_name,
                   ROUND(AVG(order_value),2) AS avg_order_value,
                   COUNT(order_id) AS total_orders
            FROM orders
            GROUP BY restaurant_name
            HAVING COUNT(order_id) >= 5
            ORDER BY avg_order_value DESC
            LIMIT 10;
        """
    }

    selected_order_q = st.selectbox(
        "Select Orders Business Question",
        list(order_questions.keys())
    )

    df_orders = pd.read_sql(order_questions[selected_order_q], conn)
    st.dataframe(df_orders)

    conn.close()
