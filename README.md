# 💸 splitwise-CLI

A command-line tool for managing shared expenses and group balances, inspired by [Splitwise](https://splitwise.com). Easily track who owes what, split bills, and manage group spending — all from your terminal.

---

## 📦 Features

- ✅ Add users
- ✅ Create groups with multiple users
- ✅ Add expenses with custom splits
- ✅ View group balances
- ✅ Persistent data storage using `pickle`
- 🚧 CLI interface built using `argparse`

---

## 🗂️ Project Structure

splitwise-CLI/
├── main.py # CLI handler using argparse
├── splitwise.py # Core logic: User, Expense, Group, Splitwise
├── rough.sh # Temporary script file (dev/testing)
├── splitwise_data.pkl # Auto-saved data for persistence
└── README.md # You're here!


---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/arjunsingh4545/splitwise-CLI.git
cd splitwise-CLI



2. Run the CLI

python3 main.py <command> [arguments]


🔧 Usage
➕ Add a User
bash
Copy
Edit
python3 main.py add_user -n Alice
🧑‍🤝‍🧑 Create a Group
bash
Copy
Edit
python3 main.py create_group -n GoaTrip -m Alice Bob Charlie
💰 Add an Expense
bash
Copy
Edit
python3 main.py add_expense \
  --group GoaTrip \
  --payer Alice \
  --amount 1500 \
  --splits Alice:500 Bob:500 Charlie:500
📊 View Group Balance
bash
Copy
Edit
python3 main.py balance --group_balance GoaTrip

💾 Data Persistence
Data is automatically saved in splitwise_data.pkl.

No manual saving required.

On each CLI invocation, the previous state is loaded and updated.

🔍 Internals
Classes Overview:
User – Individual with balances relative to others.

Expense – One payment split among multiple users.

Transaction – Direct money transfers between users.

Group – Collection of users and their expenses.

Splitwise – Main class managing all entities.

🧠 Future Improvements
 Add equal/percentage split logic

 Implement interactive terminal mode

 Add ability to remove expenses or users

 Generate summary reports (CSV/JSON)

 Add unit tests

🤝 Contributing
This project is not completed.
Open for suggestions, feedback, and pull requests!

If you find a bug or want to add features, feel free to open an issue or submit a PR.
