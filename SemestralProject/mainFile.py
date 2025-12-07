from functions import valid_amount
from functions import calc_summary
from functions import calc_allocation
import json
import os


from datetime import datetime
date = datetime.now()
timestamp = date.strftime("%Y-%m-%d %H:%M:%S")



if os.path.exists("datatest6.json"):
    with open("datatest6.json", "r") as f:
        data = json.load(f)

else:        
  data = {
      "meta": {"created": datetime.now().isoformat()},

      "acc_bal": {                    
          "account_balance": 0.0
      },

      "summary": {                    
          "total_savings": 0.0,
          "savings": {
              "Investments": 0.0,
              "Self-Development": 0.0,
              "Emergency Fund": 0.0,
              "Travel/Leisure": 0.0,
              "Home Improvement": 0.0
          },
          "total_expenses": 0.0,
          "expenses": {
              "Bills & Utilities": 0.0,
              "Food & Groceries": 0.0,
              "Transportation": 0.0,
              "Debt & Payments": 0.0,
              "Health & Medicine": 0.0,
              "Shopping": 0.0,
              "Family & Gifts": 0.0,
              "Insurance": 0.0,
              "Rent/Housing": 0.0,
              "Education": 0.0
          }
      },

      "transactions": [],           

      "allocations": {                 
          "Investments": 0.40,
          "Self-Development": 0.30,
          "Emergency Fund": 0.10,
          "Travel/Leisure": 0.10,
          "Home Improvement": 0.10
      }
  }



while True:
  print("=" * 52)
  print("\t  💸 MONEY TRACKING SYSTEM 🪙")
  print("=" * 52)

  print("a) Add to Savings")
  print("b) Add to Expenses")
  print("c) View Summary")
  print("d) View Transaction History") 
  print("e) Quit")

  action = input("\nChoose action (a/b/c/d): ").lower()

# ------------------Add to Savings------------------
  if action == "a":
    while True:
      print("a) Deposit")
      print("b) Back to main menu")

      action = input("\nChoose action(a/b): ").lower()

      if action == "a": #calculate allocations and update balances
        entered_amount = valid_amount()
        
        #update categories (summaries)
        #invest
        data["summary"]["savings"]["Investments"] = calc_summary(data['summary']['savings']['Investments'], entered_amount, data["allocations"]["Investments"])

        #self dev
        data["summary"]["savings"]["Self-Development"] = calc_summary(data ['summary']['savings']['Self-Development'], entered_amount, data["allocations"]["Self-Development"])

        #emergency fund
        data["summary"]["savings"]["Emergency Fund"] = calc_summary(data ['summary']['savings']['Emergency Fund'], entered_amount, data["allocations"]["Emergency Fund"])

        #leisure
        data["summary"]["savings"]["Travel/Leisure"] = calc_summary(data ['summary']['savings']['Travel/Leisure'], entered_amount, data["allocations"]["Travel/Leisure"])

        #home improvement
        data["summary"]["savings"]["Home Improvement"] = calc_summary(data ['summary']['savings']['Home Improvement'], entered_amount, data["allocations"]["Home Improvement"])

        savings_values = data['summary']['savings'].values()

        calculated_total = sum(savings_values)

        data['summary']['total_savings'] = calculated_total


        #------------record transaction------------

        transaction_record = {
            "type": "savings",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "amount": entered_amount,
            "total_savings": data["summary"]["total_savings"],
            "Allocations": {
                "Investments": calc_allocation(entered_amount, data['allocations']['Investments']),
                "Self-Development": calc_allocation(entered_amount, data['allocations']['Self-Development']),
                "Emergency Fund": calc_allocation(entered_amount, data['allocations']['Emergency Fund']),
                "Travel/Leisure": calc_allocation(entered_amount, data['allocations']['Travel/Leisure']),
                "Home Improvement": calc_allocation(entered_amount, data['allocations']['Home Improvement'])
            }
        }

        data["transactions"].append(transaction_record)


        # ------------------Print Transaction Receipt------------------
        print("\n=========== TRANSACTION RECEIPT ===========")
        print(f"   ------ {timestamp}------")
        print(f"\nTotal Savings: {data['summary']['total_savings']:>,.2f}")
        print("\nSAVINGS", "-" * 34)
        print(f" Investments: {calc_allocation(entered_amount, data['allocations']['Investments']):,.2f}")
        print(f" Self-Development: {calc_allocation(entered_amount, data['allocations']['Self-Development']):,.2f}")
        print(f" Emergency Fund: {calc_allocation(entered_amount, data['allocations']['Emergency Fund']):,.2f}")
        print(f" Travel/Leisure: {calc_allocation(entered_amount, data['allocations']['Travel/Leisure']):,.2f}")
        print(f" Home Improvement: {calc_allocation(entered_amount, data['allocations']['Home Improvement']):,.2f}")
        print() 

        #------------save data to json file------------
        # with open("datatest2.json", "w") as f:
        #   json.dump(data, f)

      elif action == "b": #back to main menu
        break

      else:
        print("\nInvalid action. Please choose again.")



# ------------------Add to Expenses------------------
  elif action == "b":
      exp_receipt = [] #append here for multiple seletion
      #--------print selection---------
      while True:
        print("\nSelect Expense Category (1-10):")
        categories = list(data["summary"]["expenses"].keys())
        for idx, category in enumerate(categories, start=1):
            print(f" {idx}) {category}")
        #------handle invalid input--------
        try:
          selected_category = int(input("\nSelect Category(1-10): "))

          if not (1 <= selected_category <= len(categories)):
            print("\nInvalid selection. Please enter a number between 1 and 10.")
            continue

        except ValueError:
            print("\nInvalid input. Please enter a number.")
            continue
        # -------- categorize -------
        category_name = categories[selected_category - 1]

        entered_amount = valid_amount()

        receipt = {
            "Category": category_name,
            "amount": entered_amount
        }
        exp_receipt.append(receipt)

        # -------- update main balances for expenses ----------
        data["summary"]["expenses"][category_name] += entered_amount
        data["summary"]["total_expenses"] += entered_amount
        
        #--------add another option---------
        stop = False
        while True:
          again = input("Add other expense? (y/n): ").lower()

          if again == "y":
            break
        #----------print transaction receipt-----------
          elif again == "n": 
              total_expense = 0
              print("\n=========== EXPENSE RECEIPT ===========")
              print(f"-------{timestamp}-------")
              for item in exp_receipt:
                  print(f"{item['Category']}: {item['amount']:,.2f}")
                  total_expense += item['amount']

              print("\nTotal:", total_expense)

              print("=======================================")
              print()

              #---------------RECORD TRANSACTION------------
              
              expense_record = {
                  "type": "expenses",
                  "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  "details": exp_receipt,  # list of category/amount dicts
                  "total": sum(item['amount'] for item in exp_receipt)
              }

              data["transactions"].append(expense_record)





              # expense_record = {
              #   "type": "expenses",
              #   "timestamp": timestamp,
              #   "details": exp_receipt,  # all expense items in this batch
              #   "total": sum(item['amount'] for item in exp_receipt)
              #   }

              # data["transactions"].append(expense_record)

              stop = True
              break
          else:
             print("\nInvalid input. Please select again.")
      
        if stop:
          break
          
       


      

#individual transaction receipt
#allocation system

# ------------------View Summary Report------------------
  if action == "c": 
    print("\nSummary Report") #savings
    print("SAVINGS")
    print(f"Investments {data["summary"]["savings"]["Investments"]:.2f}")

    print(f"Self-Development {data['summary']['savings']['Self-Development']:.2f}")

    print(f"Emergency Fund {data['summary']['savings']['Emergency Fund']:.2f}")
          
    print(f"Travel/Leisure {data['summary']['savings']['Travel/Leisure']:.2f}")
  
    print(f"Home Improvement {data['summary']['savings']['Home Improvement']:.2f}")

    print()
    print(f"Total Savings: {data['summary']['total_savings']:,.2f}")

    print("\nEXPENSES")
    print(f"Bills & Utilities: {data["summary"]["expenses"]["Bills & Utilities"]:.2f}")
    print(f"Food & Groceries: {data["summary"]["expenses"]["Food & Groceries"]}")
    print(f"Transportation: {data["summary"]["expenses"]["Transportation"]}")
    print(f"Debt & Payments: {data["summary"]["expenses"]["Debt & Payments"]}")
    print(f"Health & Medicine: {data["summary"]["expenses"]["Health & Medicine"]}")
    print(f"Shopping: {data["summary"]["expenses"]["Shopping"]}")
    print(f"Family & Gifts: {data["summary"]["expenses"]["Family & Gifts"]}")
    print(f"Insurance: {data["summary"]["expenses"]["Insurance"]}")
    print(f"Rent/Housing: {data["summary"]["expenses"]["Rent/Housing"]}")
    print(f"Education: {data["summary"]["expenses"]["Education"]}")
    


# ------------------View Transaction History------------------
  if action == "d":
    print("\nTransaction History")
    if not data["transactions"]:
        print("No transactions yet.")
    for transaction in data["transactions"]:
        print("-" * 40)
        print(f"Type: {transaction['type'].capitalize()}")
        print(f"Timestamp: {transaction['timestamp']}")

        if transaction["type"] == "savings":
            print(f"Amount: {transaction['amount']:,.2f}")
            print("Allocations:")
            for cat, amt in transaction["Allocations"].items():
                print(f"  {cat}: {amt:,.2f}")
        elif transaction["type"] == "expenses":
            print("Details:")
            for item in transaction["details"]:
                print(f"  {item['Category']}: {item['amount']:,.2f}")
            print(f"Total: {transaction['total']:,.2f}")

     


















     
      # print("\nTransaction History")
      # for transaction in data["transactions"]:      
      #     print("-" * 40)
      #     print(f"Type: {transaction['type'].capitalize()}")
      #     print(f"Amount: {transaction['amount']:,.2f}")
      #     print(f"Timestamp: {transaction['timestamp']}")
      #     if transaction["type"] == "savings":
      #         print("Allocations:")
      #         print(f"  Investments: {transaction['Investments']:,.2f}")
      #         print(f"  Self-Development: {transaction['Self-Development']:,.2f}")
      #         print(f"  Emergency Fund: {transaction['Emergency Fund']:,.2f}")
      #         print(f"  Travel/Leisure: {transaction['Travel/Leisure']:,.2f}")
      #         print(f"  Home Improvement: {transaction['Home Improvement']:,.2f}")
      #         print("-" * 40)  
      #     elif transaction["type"] == "expenses":
      #       for item in transaction["details"]:
      #           print(f"{item['Category']}: {item['amount']:,.2f}")
      #       print(f"Total: {transaction['total']:,.2f}")




#---------quit program-----------
  if action == "e":
     break
            
        

  with open("datatest6.json", "w") as f:
    json.dump(data, f, indent=4)
        














        # data["summary"]["Categories"]["Investments"] = calc_allocation( 
        #         data["savings"]["Categories"]["Investments"], 
        #         entered_amount, 
        #         data["allocation"]["a_invest"]) 
        # #selfdev
        # data["savings"]["Categories"]["Self-Development"] = calc_allocation( 
        #         data["savings"]["Categories"]["Self-Development"], 
        #         entered_amount, 
        #         data["allocation"]["a_selfdev"])
        # # emerg fund
        # data["savings"]["Categories"]["Emergency Fund"] = calc_allocation(
        #         data["savings"]["Categories"]["Emergency Fund"], 
        #         entered_amount, 
        #         data["allocation"]["a_emerg"])
        # #leisure
        # data["savings"]["Categories"]["Travel/Leisure"] = calc_allocation(
        #         data["savings"]["Categories"]["Travel/Leisure"], 
        #         entered_amount, 
        #         data["allocation"]["a_leisure"])
        # #home
        # data["savings"]["Categories"]["Home Improvement"] = calc_allocation(
        #         data["savings"]["Categories"]["Home Improvement"], 
        #         entered_amount, 
        #         data["allocation"]["a_home"])

        # print("\n=========== TRANSACTION RECEIPT ===========")
        # print(f"   ------ {timestamp}------")
        # print(f"\nTotal Balance: {data["savings"]["Total Allocated"]:>,.2f}")
        # print("\nSAVINGS", "-" * 34)

        # for key in data["savings"]["Categories"]: 
        #   width = 40
        #   amount = data['savings']["Categories"][key]
        #   amount_str = f"{amount:,.2f}"
        #   dots = "." * (width - len(key) - len(amount_str))
        #   print(f" {key}{dots}{amount_str}")

        # print()

        
    

  

      


        # transaction_record = {
        #   "type": "savings",
        #   "amount": entered_amount,
        #   "timestamp": timestamp,
        #   "Total Savings": data["summary"]["total_savings"],
        #   "Investments": calc_allocation(entered_amount, data['allocations']['Investments']),
        #   "Self-Development": calc_allocation(entered_amount, data['allocations']['Self-Development']),
        #   "Emergency Fund": calc_allocation(entered_amount, data['allocations']['Emergency Fund']),
        #   "Travel/Leisure": calc_allocation(entered_amount, data['allocations']['Travel/Leisure']),
        #   "Home Improvement": calc_allocation(entered_amount, data['allocations']['Home Improvement'])
        # }