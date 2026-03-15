import streamlit as st
import os
import datetime

TRACKED = os.path.join(os.path.dirname(__file__), "tracked.txt")

st.set_page_config("Expense tracker", layout="wide")
st.title("💸 Expense Tacker System")

st.markdown(
"""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
""",
unsafe_allow_html=True
)
menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Add Expense",
        "View Expense",
        "Total Expense",
        "Edit Expense",
        "Delete Expense",
        "Expense Chart",
        "Monthly Analytics"
        
    ]
)
st.sidebar.markdown("---")

st.sidebar.markdown(
"""
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
""",
unsafe_allow_html=True
)


def exp_validation(payment_id):
     return  payment_id.startswith("EX") and  payment_id[2:].isdigit() and len(payment_id) == 5

def load_expense():
    expenses = []
    if not os.path.exists(TRACKED):
        open(TRACKED, "w").close()
    with open(TRACKED) as f:
        for line in f:
            d = line.strip().split("|")
            if len(d) == 5:
                expenses.append({
                    "payment_id":d[0],
                    "date": d[1],
                    "category": d[2],
                    "amount": d[3],
                    "description": d[4],
                     
                })
    return expenses

def save_expenses(expenses):
    with open(TRACKED, "w") as f:
        for s in expenses:
            line = "|".join(str(value) for value in s.values())
            f.write(line + "\n")

def ValidateAmount(amount):
   return amount>0

expenses=load_expense()

if menu == "Add Expense":
    st.subheader("➕ Add Expense")

    with st.form("add_student", clear_on_submit=True):
        payment_id = st.text_input("expense ID (EX001,EX002,...)")
        date = datetime.date.today().strftime("%d-%m-%Y") 
        category = st.text_input("Enter category(Food,cloth,books,etc..)")
        amount=st.number_input("enter amount")
        description = st.text_input("additional description")
        submit = st.form_submit_button("Add Expense")

    if submit:
         if not exp_validation(payment_id):
            st.error("Invalid payment ID")
         elif any(s["payment_id"] == payment_id for s in expenses):
            st.warning("expense id already exists")  
         elif not ValidateAmount(amount):
             st.error("amount should be greater than 0.Rs") 
         else:

            expenses.append({
                    "payment_id":payment_id,
                    "date": date,
                    "category": category,
                    "amount": amount,
                    "description": description,
                    
                
            })

            save_expenses(expenses)
            st.success("saved!!!")      

if menu == "View Expense":
    st.subheader("📋 All Expenses")

    if len(expenses) == 0:
        st.info("No expenses found")
    else:
         st.dataframe(expenses, use_container_width=True)

if menu == "Total Expense":
    st.subheader("💰 Total Spending")

    total = sum(float(i["amount"]) for i in expenses)

    st.metric("Total Spent", f"₹ {total}")

if menu == "Edit Expense":
    st.subheader("✏ Edit Expense")

    payment_ids = [i["payment_id"] for i in expenses]

    selected_id = st.selectbox("Select Expense ID", payment_ids)

    new_amount = st.number_input("Enter new amount", min_value=1)

    if st.button("Update Expense"):
        for i in expenses:
            if i["payment_id"] == selected_id:
                i["amount"] = new_amount
                save_expenses(expenses)
                st.success("Expense updated successfully!")
                break

if menu == "Delete Expense":
    st.subheader("🗑 Delete Expense")

    payment_ids = [i["payment_id"] for i in expenses]

    selected_id = st.selectbox("Select Expense ID to delete", payment_ids)

    if st.button("Delete Expense"):
        for i in expenses:
            if i["payment_id"] == selected_id:
                expenses.remove(i)
                save_expenses(expenses)
                st.success("Expense deleted successfully!")
                break     

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

#---------------Monthly spendings__________________
if menu == "Monthly Analytics":
    st.subheader("📅 Monthly Expense Analytics")

    monthly_data = {}

    for i in expenses:
        date_str = i["date"]
        amount = float(i["amount"])

        date_obj = datetime.datetime.strptime(date_str, "%d-%m-%Y")
        month_key = date_obj.strftime("%B %Y")   # Example: March 2026

        if month_key in monthly_data:
            monthly_data[month_key] += amount
        else:
            monthly_data[month_key] = amount

    if len(monthly_data) == 0:
        st.info("No expenses available")
    else:
        st.bar_chart(monthly_data)

        highest_month = max(monthly_data, key=monthly_data.get)

        st.metric(
            "Highest Spending Month",
            highest_month,
            f"₹ {monthly_data[highest_month]}"
        )
