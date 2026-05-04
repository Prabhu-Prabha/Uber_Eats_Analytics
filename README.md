#Uber_Eats_Analytics
End-to-end Data Analytics project using Python, MySQL Xampp, Streamlit

 #Project Overview
This project is an end-to-end **Data Analytics & Business Intelligence Dashboard** built using **Python, MySQL, and Streamlit**.  
It analyzes restaurant and order data inspired by Uber Eats to uncover business insights through **SQL-driven analytics** and an **interactive web dashboard**.

The project demonstrates the complete data lifecycle:
- Data Cleaning & Preparation
- Database Design & SQL Analysis
- Interactive Dashboard Development
- Business Question Answering

---

🛠 Libraries and softwares and frameworks Used
- **Python** (Pandas, NumPy)
- **MySQL** (Database & SQL Queries)
- **Streamlit** (Interactive Dashboard)
- **VS Code** (Development)
- **Jupyter Notebook** (Database Query Validation)


---

🧹 Data Cleaning
- Removed duplicate records
- Handled missing and inconsistent ratings
- Converted categorical columns into numerical values
- Cleaned and standardized cost fields
- Exported cleaned data for database ingestion

---

 🗄 Database Design
- MySQL database: **project_i**
- Tables:
  - `uber_explore` – restaurant-level information
  - `orders` – transactional order data (imported from JSON)

---

 📊 Streamlit Dashboard Features

 🔹 Tab 1: Interactive Dashboard
- Dynamic filters:
  - Location
  - Price segment
  - Online order availability
- SQL-based filtering for real-time data updates
- Results displayed in structured tabular format

---

🔹 Tab 2: Business Q&A Analysis
- 10 predefined business questions
- Examples:
  - Top-rated locations
  - Impact of online ordering on ratings
  - Best price segments
- SQL-driven aggregation and analysis

---

🔹 Tab 3: Order Data Analytics
- JSON order data integrated into MySQL
- Advanced metrics:
  - Total orders per restaurant
  - Average order value
- Business insights based on transactional behavior

---

▶️ How to Run the Project

 Step 1: Install Dependencies
```bash
pip install -r requirements.txt

streamlit run Uber_Eats_Explore.py

or Use VS Code to run directly from editor and built-in terminal
