import streamlit as st
import sqlite3
import datetime

# DATABASE CONNECTION
conn = sqlite3.connect("expenses.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
payment_id TEXT PRIMARY KEY,
date TEXT,
category TEXT,
amount REAL,
description TEXT
)
""")
conn.commit()

st.set_page_config("Expense tracker", layout="wide")
st.title("💸 Expense Tracker System")

st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
""", unsafe_allow_html=True)

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Add Expense",
        "View Expense",
        "Total Expense",
        "Edit Expense",
        "Delete Expense",
        "Expense Chart"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("""
<div style="display:flex; justify-content:center; gap:20px; margin-top:20px;">
<a href="https://www.linkedin.com/in/parth-adsul-889106384/" target="_blank">
<i class="fab fa-linkedin" style="font-size:34px; color:#0A66C2;"></i>
</a>

<a href="https://github.com/parth484" target="_blank">
<i class="fab fa-github" style="font-size:34px; color:black;"></i>
</a>
</div>

<p style="text-align:center; font-size:12px; margin-top:8px;">
Made by Parth Adsul
</p>
""", unsafe_allow_html=True)

print("------------------Khata book app----------------------")


def exp_validation(payment_id):
    return payment_id.startswith("EX") and payment_id[2:].isdigit() and len(payment_id) == 5


def load_expense():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    expenses = []
    for r in rows:
        expenses.append({
            "payment_id": r[0],
            "date": r[1],
            "category": r[2],
            "amount": r[3],
            "description": r[4],
        })
    return expenses


def ValidateAmount(amount):
    return amount > 0


expenses = load_expense()

# ADD EXPENSE
if menu == "Add Expense":
    st.subheader("➕ Add Expense")

    with st.form("add_expense", clear_on_submit=True):
        payment_id = st.text_input("Expense ID (EX001, EX002...)")
        date = datetime.date.today().strftime("%d-%m-%Y")
        category = st.text_input("Enter category (Food, cloth, books...)")
        amount = st.number_input("Enter amount")
        description = st.text_input("Additional description")
        submit = st.form_submit_button("Add Expense")

    if submit:
        if not exp_validation(payment_id):
            st.error("Invalid payment ID")

        elif any(s["payment_id"] == payment_id for s in expenses):
            st.warning("Expense ID already exists")

        elif not ValidateAmount(amount):
            st.error("Amount should be greater than 0")

        else:
            cursor.execute(
                "INSERT INTO expenses VALUES (?,?,?,?,?)",
                (payment_id, date, category, amount, description)
            )
            conn.commit()

            st.success("Expense saved successfully!")

# VIEW EXPENSE
if menu == "View Expense":
    st.subheader("📋 All Expenses")

    if len(expenses) == 0:
        st.info("No expenses found")
    else:
        st.dataframe(expenses, use_container_width=True)

# TOTAL EXPENSE
if menu == "Total Expense":
    st.subheader("💰 Total Spending")

    total = sum(float(i["amount"]) for i in expenses)

    st.metric("Total Spent", f"₹ {total}")

# EDIT EXPENSE
if menu == "Edit Expense":
    st.subheader("✏ Edit Expense")

    payment_ids = [i["payment_id"] for i in expenses]

    selected_id = st.selectbox("Select Expense ID", payment_ids)

    new_amount = st.number_input("Enter new amount", min_value=1)

    if st.button("Update Expense"):

        cursor.execute(
            "UPDATE expenses SET amount=? WHERE payment_id=?",
            (new_amount, selected_id)
        )
        conn.commit()

        st.success("Expense updated successfully!")

# DELETE EXPENSE
if menu == "Delete Expense":
    st.subheader("🗑 Delete Expense")

    payment_ids = [i["payment_id"] for i in expenses]

    selected_id = st.selectbox("Select Expense ID to delete", payment_ids)

    if st.button("Delete Expense"):

        cursor.execute(
            "DELETE FROM expenses WHERE payment_id=?",
            (selected_id,)
        )
        conn.commit()

        st.success("Expense deleted successfully!")

# EXPENSE CHART
if menu == "Expense Chart":
    st.subheader("📊 Expense Category Chart")

    category_data = {}

    for i in expenses:
        cat = i["category"]
        amt = float(i["amount"])

        if cat in category_data:
            category_data[cat] += amt
        else:
            category_data[cat] = amt

    st.bar_chart(category_data)