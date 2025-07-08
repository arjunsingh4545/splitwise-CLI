import argparse
import os
import pickle
from splitwise import Splitwise, Expense

DATA_FILE = "splitwise_data.pkl"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'rb') as f:
            return pickle.load(f)
    return Splitwise()

def save_data(data):
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(data, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Splitwise CLI Tool")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Create user
    user_parser = subparsers.add_parser("add_user")
    user_parser.add_argument("-n", "--name", type=str, required=True, help="Name of the user")

    # Create group
    group_parser = subparsers.add_parser("create_group")
    group_parser.add_argument("-n", "--name", type=str, required=True, help="Name of the group")
    group_parser.add_argument("-m", "--members", nargs='+', required=True, help="List of user names to add to the group")

    # Add expense
    expense_parser = subparsers.add_parser("add_expense")
    expense_parser.add_argument("--group", required=True, help="Group name")
    expense_parser.add_argument("--payer", required=True, help="Name of the payer")
    expense_parser.add_argument("--amount", type=float, required=True, help="Amount paid")
    expense_parser.add_argument("--splits", nargs='+', required=True, help="Format: name:amount")

    # Get group balance
    balance_parser = subparsers.add_parser("balance")
    balance_parser.add_argument("--group_balance", required=True, help="Group name for balance")

    args = parser.parse_args()
    sw = load_data()

    match args.command:

        case "add_user":
            user = sw.add_user(args.name)
            print(f"User created: {user.name}")

        case "create_group":
            members = [sw.get_user(name) for name in args.members]
            if None in members:
                print("One or more users not found.")
            else:
                group = sw.create_group(args.name, members)
                print(f"Group created: {group.groupName} with members {[u.name for u in members]}")

        case "add_expense":
            payer = sw.get_user(args.payer)
            group = sw.get_group(args.group)
            if not payer or not group:
                print("Invalid payer or group")
            else:
                expense = Expense(payer=payer, amount=args.amount)
                for split in args.splits:
                    try:
                        name, amt = split.split(":")
                        user = sw.get_user(name)
                        if user:
                            expense.add_split(user, float(amt))
                        else:
                            print(f"User {name} not found")
                    except ValueError:
                        print(f"Invalid split format: {split}")
                sw.add_expense_to_group(args.group, expense)
                print(f"Added expense to {args.group}: {expense}")

        case "balance":
            group = sw.get_group(args.group_balance)
            if group:
                balances = sw.get_group_balance(args.group_balance)
                print(f"Balances for group '{args.group_balance}':")
                for name, bal in balances.items():
                    print(f"{name}: {bal:.2f}")
            else:
                print("Group not found")

    save_data(sw)
    print("Data saved successfully.")

