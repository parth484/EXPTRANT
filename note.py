import streamlit as st
import os
import datetime

TRACKED="tracked.txt"



print("------------------Khata book app----------------------")

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

def getAmount():
    while True:
        try:
            amount=int(input("enter a amount"))
            if amount<=0:
                print("amount should be greater than 0")
                continue
            return amount
        except ValueError:
            print("Invalid input!! Please enter valid amount type")

def menu():
    while True:
        print("+++++++++++++++++expense tracker+++++++++++++++++++++")
        print("1.add ur expenses")  
        print("2.view all expenses")
        print("3.show total spent")
        print("4.edit expenses")
        print("5.delete expenses")
        print("6.exit")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        x=int(input("enter a option :"))

        if(x==1):

            print("ADD UR EXPENSES")
            addExpenses()
        elif(x==2):

            print("view all expenses")  
            view_expenses()
        elif(x==3):

            print("total expanditure")  
            show_ttlspent()

        elif(x==4):

            print("edit") 
            edit_expenses()
        elif(x==5):

            print("delete") 
            delete_expense()

        elif(x==6):

            print("exit")  
            return False

expenses=load_expense()
def addExpenses():
   payment_id=input("enter expense ID for ur sleamless use(Should contain eg:-EX123)")
   if not exp_validation(payment_id):
       print("payment id format - (EX122,EX890")
       return
   for i in expenses:
       if i['payment_id']==payment_id:
           print("id already exist please enter another")
           return
   date = datetime.date.today().strftime("%d-%m-%Y")    
   category=input("Write category(food,cloth,books,etc)")
   amount=getAmount()
   description=input("enter a object name u pay for")
   xo=input("enter to continue")

   expenses.append({
        "payment_id":payment_id,
        "date": date,
        "category": category,
        "amount": amount,
        "description": description,
        
       
   })

   save_expenses(expenses)
   print("saved!!!")

def view_expenses():
    print("expense id  |  date         |  category  |  Amount  |  description")
    for i in expenses:
           
           print(f"{i['payment_id']}       |  {i['date']}   |   {i['category']}   |    {i['amount']}  |  {i['description']}")

def show_ttlspent():
    sum=0
    for i in expenses:
        sum=sum+int(i['amount'])
    
    print(sum)

def edit_expenses():
    
    co=input("do u really want to edit Y/N").lower()
    if co=="y":
        payment_id=input("enter expense id to delete!")
        for i in expenses:
           if i['payment_id']==payment_id:
              print("u can update only amount!!")
              new_amount=getAmount()
              i['amount']=new_amount
              save_expenses(expenses)
              return i
        print("not found")
        return None
    
def delete_expense():
    dele=input("Do you really want to delete Y/N").lower()
    found=False
    if dele=="y":
      expense_id=input("enter expense id")
      for i in expenses:
          if i['payment_id']==expense_id:
              expenses.remove(i)
              save_expenses(expenses)
              print("successfully deleted")
              found=True
              return
          
      if not found:
          print("not found")
menu()