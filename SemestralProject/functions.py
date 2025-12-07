#get valid amount



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

def calc_allocation(entered_amount, percentage):
    allocation = entered_amount * percentage
    return allocation

def calc_summary(current_total, entered_amount, percentage):
    update = entered_amount * percentage
    return current_total + update



    
