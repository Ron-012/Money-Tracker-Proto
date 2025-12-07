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
  print("f) RESET")

  action = input("\nChoose action (a/b/c/d): ").lower().strip()

# ------------------add to savings------------------
  if action == "a":
    while True:
      print("a) Deposit")
      print("b) Back to main menu")

      action = input("\nChoose action(a/b): ").lower().strip()

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
            "timestamp": timestamp,
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


        # ------------------print transaction receipt------------------
        print("\n=========== TRANSACTION RECEIPT ===========")
        print(f"   ------ {timestamp} ------\n")

        total_savings = data['summary']['total_savings']
        print(f"Total Savings: {total_savings:,.2f}\n")

        print("ALLOTMENT")
        width = 40  

        for category, pct in data['allocations'].items():
            amount = calc_allocation(entered_amount, pct)
            amount_str = f"{amount:,.2f}"
            dots = "." * (width - len(category) - len(amount_str))
            print(f" {category}{dots}{amount_str}")

        print("\n" + "=" * 43 + "\n")
        with open("datatest6.json", "w") as f:
          json.dump(data, f, indent=4)
      elif action == "b": #back to main menu
        break

      else:
        print("\nInvalid action. Please choose again.")



# ------------------Add to Expenses------------------
  elif action == "b":
      exp_receipt = [] #(multiple seletion)
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
              amount_entered = sum(item['amount'] for item in exp_receipt)
              master_total = data['summary']['total_expenses']
              width = 40  
            
              print("\n========= TRANSACTION RECEIPT ==========")
              print(f"   ------ {timestamp} ------\n")
              print(f"{'Master Total Expenses':<}{'.' * (width - len('Master Total Expenses') - len(f'{master_total:,.2f}'))}{master_total:,.2f}")
              print(f"{'Total Amount Entered':<}{'.' * (width - len('Total Amount Entered') - len(f'{amount_entered:,.2f}'))}{amount_entered:,.2f}")
              print("-" * width)

             

              print("Details:")
              for item in exp_receipt:
                  amount = item['amount']
                  total_expense += amount
                  amount_str = f"{amount:,.2f}"
                  category = item['Category']
                  dots = "." * (width - len(category) - len(amount_str))
                  print(f"{category}{dots}{amount_str}")
              print()
              print(f"{'Total':<}{'.' * (width - len('Total') - len(f'{total_expense:,.2f}'))}{total_expense:,.2f}")
              print("=" * width + "\n")


              #---------------record transaction------------
              
              expense_record = {
                  "type": "expenses",
                  "timestamp": timestamp,
                  "details": exp_receipt,  # list of category/amount dicts
                  "total": sum(item['amount'] for item in exp_receipt)
              }

              data["transactions"].append(expense_record)

              with open("datatest6.json", "w") as f:
                json.dump(data, f, indent=4)

              stop = True
              break
          else:
             print("\nInvalid input. Please select again.")
      
        if stop:
          break
        

# ------------------summary------------------
  elif action == "c": 
    width = 52

    print("\n" + "=" * 52)
    print("\t\t  SUMMARY REPORT")
    print("=" * 52)

    # ------------------ savings ------------------
    print("\nSAVINGS")
    print("-" * 52)
    print(f"{'Total Savings':<}{'.' * (width - len('Total Savings') - len(f'{data['summary']['total_savings']:,.2f}'))}{data['summary']['total_savings']:,.2f}\n")

    for category, amount in data['summary']['savings'].items():
        amount_str = f"{amount:,.2f}"
        dots = "." * (width - len(category) - len(amount_str))
        print(f"{category:<}{dots}{amount_str}")

    print("_" * 52)

    # ------------------ expenses ------------------
    print("\nEXPENSES")
    print("-" * 52)
    print(f"{'Total Expenses':<}{'.' * (width - len('Total Expenses') - len(f'{data['summary']['total_expenses']:,.2f}'))}{data['summary']['total_expenses']:,.2f}\n")

    for category, amount in data['summary']['expenses'].items():
        amount_str = f"{amount:,.2f}"
        dots = "." * (width - len(category) - len(amount_str))
        print(f"{category:<}{dots}{amount_str}")

    print("_" * 52)
    print()
    
 
# ------------------view history------------------
  elif action == "d":
    width = 52
    print("=" * 52)
    print("\t\t TRANSACTION HISTORY")
    print("=" * 52)

    if not data["transactions"]:
        print("No transactions yet.\n")
    else:
        for transaction in data["transactions"]:
            print("=" * 52)
            print(f"Type: {transaction['type'].capitalize()}")
            print(f"Timestamp: {transaction['timestamp']}\n")

            if transaction["type"] == "savings":
                amount_str = f"{transaction['amount']:,.2f}"
                print(f"{'Total Amount Entered':<}{'.' * (width - len('Total Amount Entered') - len(amount_str))}{amount_str}")
                print("-" * 52)
                print("Allocations:")
                for cat, amt in transaction["Allocations"].items():
                    amt_str = f"{amt:,.2f}"
                    dots = "." * (width - len(cat) - len(amt_str)-2)
                    print(f"  {cat:<}{dots}{amt_str}")

            elif transaction["type"] == "expenses":
                total_str = f"{transaction['total']:,.2f}"
                print(f"{'Total Amount Entered':<}{'.' * (width - len('Total Amount Entered') - len(total_str))}{total_str}")
                print("-" *52)
                print("Details:")
                for item in transaction["details"]:
                    amt_str = f"{item['amount']:,.2f}"
                    dots = "." * (width - len(item['Category']) - len(amt_str)-2)
                    print(f"  {item['Category']:<}{dots}{amt_str}")
                print()

#---------quit program-----------
  elif action == "e":
    with open("datatest6.json", "w") as f:
      json.dump(data, f, indent=4)
    break
  

 #----------clear data---------------
  elif action == "f":
      confirm = input("\n⚠️ This will erase ALL data and restore default settings.\nAre you sure? (y/n): ").lower().strip()
      if confirm != "y":
          print("\nReset cancelled.\n")
          continue   

      current_allocations = data.get("allocations", {
          "Investments": 0.40,
          "Self-Development": 0.30,
          "Emergency Fund": 0.10,
          "Travel/Leisure": 0.10,
          "Home Improvement": 0.10
      })

      default_data = {
          "meta": {"created": datetime.now().isoformat()},
          "acc_bal": {"account_balance": 0.0},
          "summary": {
              "total_savings": 0.0,
              "savings": {k: 0.0 for k in current_allocations.keys()},
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
          "allocations": current_allocations
      }


      filename = "datatest6.json"
      with open(filename, "w") as file:
          json.dump(default_data, file, indent=4)

    
      data = default_data

      print("\n✅ All data cleared! Defaults restored.\n")

   
  else:
    print("Invalid action, Please try again.")
            
        


