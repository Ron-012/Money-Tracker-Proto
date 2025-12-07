
total_bal = 0.0 #initialize value

#savings
investments = 0.0
self_dev = 0.0
emergency = 0.0
leisure = 0.0
home = 0.0

#allocation
a_invest = 0.40
a_selfdev = 0.30
a_emerg = 0.10
a_leisure = 0.10
a_home = 0.10

#expenses
total_exp = 0
bills = 0
food = 0
transport = 0
debt = 0
health = 0
shopping = 0
family = 0
withdrawal = 0
rent = 0
education = 0

#get date
from datetime import datetime

date = datetime.now()
timestamp = date.strftime("%Y-%m-%d %H:%M:%S")

def process_expense(category_total, total_exp, total_bal, label):
    amount = valid_amount()
    total_exp, category_total, total_bal = calc_exp(total_exp, category_total, total_bal, amount)

    receipt()
    print(receipt_format(label, category_total))

    return category_total, total_exp, total_bal

def receipt():
      print("\n ---Expenses---")
      print(f"Total Expenses: {total_exp:,.2f}")
      print(f"\n- {timestamp} -")
    

#formatting receipt
def receipt_format(label, value, width=40):
      value_str = f"{value:,.2f}"
      dot = "." * (width - len(label) - len(value_str))
      return f"{label}{dot}{value_str}"


def calc_exp(exp, value, balance, amount):
  exp += amount
  value += amount
  balance -= amount
  return exp, value, balance

    
#handle invalid amount
def valid_amount(prompt="Enter Amount: "):
    while True:
        amt_input = input(prompt).strip()
        try:
            amount = float(amt_input)
            if amount <= 0:
                print("Invalid amount. Amount must be greater than 0.")
                continue
            return amount
        except ValueError:
            print("Invalid amount. Enter only the numeric value.")



# print("--- MONEY TRACKING SYSTEM---") #HOME PAGE/INTERFACE
# print("Total balance:", total_bal)


while True:
  print("\n--- MONEY TRACKING SYSTEM---") #HOME PAGE/INTERFACE
  print(f"Total balance: {total_bal:,.2f}")
  print("\na) Add to savings \nb) Add to expenses \nc) View Summary \nd) Quit")
  action = input("\nChoose action (a/b/c/d): ")
  
#enter savings interface  
  if action == "a":
    print("\na) Add to savings \nb) View Summary")
    select = input("Choose action (a/b): ")

#add to savings
    if select == "a":
      print("\n---Savings---")
      add = valid_amount()
      total_bal += add

#get allocations
      investments += add * a_invest 
      self_dev += add * a_selfdev
      emergency += add * a_emerg
      leisure += add * a_leisure
      home += add * a_home

  
#print receipt
    print("\n---Savings---")

    print(f"\n\t-- {timestamp} --")

    print(receipt_format("Investments:", investments))
    print(receipt_format("Self-development:", self_dev))
    print(receipt_format("Emergency Fund:", emergency))
    print(receipt_format("Travel/Leisure:", leisure))
    print(receipt_format("Home improvement:", home))
    print(receipt_format("Total:", add))
    print(receipt_format("\nNew Balance:", total_bal))
#view summary


############################################################################


#expenses interface

  elif action == "b":
    print("\n---Expenses---")
    print("a) Bills & Utilities")
    print("b) Food & Groceries")
    print("c) Transportation")
    print("d) Debt & Payments")
    print("e) Health & Medicine")
    print("f) Shopping")
    print("g) Family & Gifts")
    print("h) Savings Withdrawal")
    print("i) Rent/Housing")
    print("j) Education")

    action = input("\nSelect action(a/b/c/d/e/f/g/h/i): ")

    if action == "a":
      bills, total_exp, total_bal = process_expense(bills, total_exp, total_bal, "Bills and Utilities:")

    elif action == "b":
      food, total_exp, total_bal = process_expense(food, total_exp, total_bal, "Foods & Groceries:")


    elif action == "c":
      transport, total_exp, total_bal = process_expense(transport, total_exp, total_bal, "Transportation:")


    elif action == "d":
      debt, total_exp, total_bal = process_expense(debt, total_exp, total_bal, "Debt & Payments:")

    elif action == "e":
      health, total_exp, total_bal = process_expense(health, total_exp, total_bal, "Health & Medicine:")


    elif action == "f":
      shopping, total_exp, total_bal = process_expense(shopping, total_exp, total_bal, "Shopping:")
 

    elif action == "g":
      family, total_exp, total_bal = process_expense(family, total_exp, total_bal, "Family & Gifts:")

    elif action == "h":
      shopping, total_exp, total_bal = process_expense(shopping, total_exp, total_bal, "Savings and Withdrawal:")
    

    elif action == "i":
      withdrawal, total_exp, total_bal = process_expense(withdrawal, total_exp, total_bal, "Rent/Housing:")
  
    elif action == "j":
      education, total_exp, total_bal = process_expense(education, total_exp, total_bal, "Education:")
       
       



      
      




#print total balance
#print total expenses

#print default allocation and categories in savings:
          # Investments - 40%
          # Self-development - 30%
          # Emergency fund - 10%
          # Travel / Leisure - 10%
          # Home improvement - 10%

#choose action
# 1) Add to savings
# 2) Add to expences
# 3) Edit default allocations
# 4) Quit (terminate the program)

# if select == 1:
  #choose action
    #add to savings
    #view summary

      #if add to savings
      #Enter date
      #Enter amount
        #amount will be split to 5 categories based on the given percentage
          # Investments - 40%
          # Self-development - 30%
          # Emergency fund - 10%
          # Travel / Leisure - 10%
          # Home improvement - 10%
      #print transaction receipt (total balance and balance per category)

       # add another? y/n
        #if no back to home
        #if yes back to add to savings

      #if view summary
        #print all transactions
        #choose action
          #back to home
      
      
# elif select == 2:
#choose action
  #add expenses
  #view history/summary

    # if add expenses
      # show categories
        #1) bills and utilities
        #2) food and groceries
        #3) transportation
        #4) debt payments
        #5) health and medicine
        #6) shopping
        #7) family/gifts
        #8) savings withdrawal
        #9) rent/housing
        #10) eudcation

      # user selects category
      # ask for date
      # ask for the amount
      # amount gets added to total expenses
      # amount get subtracted to main savings
      # expenses saved with the selected category
      #print transaction receipt and updated balance
      # save transaction to history

      # add another? y/n
        #if no back to home
        #if yes back to add expenses
      
  #if view history/summary
    #print all history/summary
    #choose action
      #back to home

# if select == 3:
  #if edit categories
        #print all categories
        #select which category to edit
          #select which to edit
            #name 
            #percentage
              #if percentage:
                #all must be equal to 100%
                #saved the new category and percentage (will automatically update the calculation in the next transaction)
                #back to home

              #else input invalid try again (loop to edit percentage)


# if select == 4:
  #terinate program

