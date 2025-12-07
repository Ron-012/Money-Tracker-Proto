import json
import os
from datetime import datetime

from functions import valid_amount
from functions import calc_allocation

FILENAME = "savings_data.json"

# --- Save / Load helpers (no try/except) ---
def save_data(state, filename=FILENAME):
    with open(filename, "w") as f:
        json.dump(state, f, indent=2)
    print("Data saved.\n")

def load_data(filename=FILENAME):
    if not os.path.exists(filename):
        return None
    with open(filename, "r") as f:
        return json.load(f)

# --- initial structure (matches your original) ---
default_data = {
  "Acc_bal": {
    "Current Total Balances": 0,
    "Total Expenses Tracked": 0
  },

  "savings": {
    "Total Allocated": 0,
    "Categories": {
      "Investments": 0,
      "Self-Development": 0,
      "Emergency Fund": 0,
      "Travel/Leisure": 0,
      "Home Improvement": 0
    }
  },

  "expenses": {
    "Bills & Utilities": 0,
    "Food & Groceries": 0,
    "Transportation": 0,
    "Debt & Payments": 0,
    "Health & Medicine": 0,
    "Shopping": 0,
    "Family & Gifts": 0,
    "Savings Withdrawal": 0,
    "Rent/Housing": 0,
    "Education": 0
  },

  "allocation": {
    "a_invest": 0.40,
    "a_selfdev": 0.30,
    "a_emerg": 0.10,
    "a_leisure": 0.10,
    "a_home": 0.10
  },

  # transactions: list of deposits; each transaction is a snapshot recorded after deposit
  # transaction example:
  # {
  #   "timestamp": "2025-11-24 16:53:14",
  #   "amount": 5000,
  #   "total_allocated_after": 5000,
  #   "categories_after": {
  #       "Investments": 2000, ...
  #    }
  # }
  "transactions": []
}

# load saved state or use default
data = load_data() or default_data

# --- helper to print one transaction in the exact receipt style you gave ---
def print_transaction_receipt(tx):
    # tx is a dict with keys: timestamp, amount, total_allocated_after, categories_after
    print("\n=========== TRANSACTION RECEIPT ===========")
    print(f"   ------ {tx['timestamp']} ------")
    print(f"\nTotal Balance: {tx['total_allocated_after']:>,.2f}")
    print("\nSAVINGS", "-" * 34)
    for key in tx["categories_after"]:
        width = 40
        amount = tx["categories_after"][key]
        amount_str = f"{amount:,.2f}"
        dots = "." * max(1, (width - len(key) - len(amount_str)))
        print(f" {key}{dots}{amount_str}")
    print()

# --- View Summary: print all saved transactions, most recent first ---
def view_summary(state):
    txs = state.get("transactions", [])
    if not txs:
        print("\nNo saved transactions yet.\n")
        return

    # print most recent first
    for tx in reversed(txs):
        print_transaction_receipt(tx)

# --- MAIN program (keeps your original menu and deposit flow) ---
while True:
  print("=" * 52)
  print("\t  💸 MONEY TRACKING SYSTEM 🪙")
  print("=" * 52)

  print("a) Add to Savings")
  print("b) Add to Expenses")
  print("c) View Summary")
  print("d) Quit")

  action = input("\nChoose action (a/b/c/d): ").lower()

  if action == "a":
    while True:
      print("a) Deposit")
      print("b) Back to main menu")

      action2 = input("\nChoose action(a/b): ").lower()

      if action2 == "a":
        # capture timestamp at moment of transaction
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        deposit_amount = valid_amount()

        # update balances
        data["Acc_bal"]["Current Total Balances"] += deposit_amount 
        data["savings"]["Total Allocated"] += deposit_amount

        # update categories using calc_allocation (keeps your original behaviour)
        data["savings"]["Categories"]["Investments"] = calc_allocation( 
                data["savings"]["Categories"]["Investments"], 
                deposit_amount, 
                data["allocation"]["a_invest"]) 
        data["savings"]["Categories"]["Self-Development"] = calc_allocation( 
                data["savings"]["Categories"]["Self-Development"], 
                deposit_amount, 
                data["allocation"]["a_selfdev"])
        data["savings"]["Categories"]["Emergency Fund"] = calc_allocation(
                data["savings"]["Categories"]["Emergency Fund"], 
                deposit_amount, 
                data["allocation"]["a_emerg"])
        data["savings"]["Categories"]["Travel/Leisure"] = calc_allocation(
                data["savings"]["Categories"]["Travel/Leisure"], 
                deposit_amount, 
                data["allocation"]["a_leisure"])
        data["savings"]["Categories"]["Home Improvement"] = calc_allocation(
                data["savings"]["Categories"]["Home Improvement"], 
                deposit_amount, 
                data["allocation"]["a_home"])

        # create a transaction snapshot AFTER the updates
        tx_snapshot = {
            "timestamp": timestamp,
            "amount": deposit_amount,
            "total_allocated_after": data["savings"]["Total Allocated"],
            # copy categories snapshot so future changes don't mutate past transactions
            "categories_after": {
                "Investments": data["savings"]["Categories"]["Investments"],
                "Self-Development": data["savings"]["Categories"]["Self-Development"],
                "Emergency Fund": data["savings"]["Categories"]["Emergency Fund"],
                "Travel/Leisure": data["savings"]["Categories"]["Travel/Leisure"],
                "Home Improvement": data["savings"]["Categories"]["Home Improvement"]
            }
        }

        # append transaction and save state
        data["transactions"].append(tx_snapshot)
        save_data(data)

        # print the receipt for this deposit (immediate feedback)
        print_transaction_receipt(tx_snapshot)

        break  # back to deposit menu

      elif action2 == "b": 
        print()
        break

      else:
        print("Invalid input. Please try again")
        print()

  elif action == "b":
    # expenses are not implemented in this version per your earlier request
    print("\nExpenses are disabled for now.\n")

  elif action == "c":
    # show all saved transactions grouped / separated by timestamp (most recent first)
    view_summary(data)

  elif action == "d":
    print("Goodbye — saving state and exiting.")
    save_data(data)
    break

  else:
    print("Invalid choice, please enter a/b/c/d.\n")
