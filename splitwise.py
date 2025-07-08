class User:
    def __init__(self, name: str):
        self.name = name
        self.balances = {}

    def __repr__(self) -> str:
        return f"User({self.name}, {self.balances})"

    def add_balance(self, user: "User", amount: float):
        if user.name in self.balances:
            self.balances[user.name] += amount
        else:
            self.balances[user.name] = amount

    def get_balance(self, user: "User") -> float:
        return self.balances.get(user.name, 0.0)


class Expense:
    def __init__(self, payer: "User", amount: float, description: str = ""):
        self.payer = payer
        self.amount = amount
        self.description = description
        self.splits = {}

    def add_split(self, user: "User", amount: float):
        if user.name in self.splits:
            self.splits[user.name] += amount
        else:
            self.splits[user.name] = amount
        user.add_balance(self.payer, -amount)

    def get_split(self, user: "User") -> float:
        return self.splits.get(user.name, 0.0)

    def __repr__(self) -> str:
        return f"Expense(payer={self.payer.name}, amount={self.amount}, description={self.description}, splits={self.splits})"


class Transaction:
    def __init__(self, from_user: "User", to_user: "User", amount: float):
        self.from_user = from_user
        self.to_user = to_user
        self.amount = amount

    def __repr__(self) -> str:
        return f"Transaction(from={self.from_user.name}, to={self.to_user.name}, amount={self.amount})"


class Group:
    def __init__(self, groupName: str, members: list["User"]):
        self.groupName = groupName
        self.members = members
        self.expenses = []
        self.transactions = []

    def add_expense(self, expense: "Expense"):
        self.expenses.append(expense)
        for user_name, amount in expense.splits.items():
            user = next((u for u in self.members if u.name == user_name), None)
            if user:
                user.add_balance(expense.payer, -amount)

    def add_transaction(self, transaction: "Transaction"):
        self.transactions.append(transaction)
        transaction.from_user.add_balance(transaction.to_user, -transaction.amount)
        transaction.to_user.add_balance(transaction.from_user, transaction.amount)

    def get_balance(self, user: "User") -> float:
        total_balance = 0.0
        for expense in self.expenses:
            total_balance += expense.get_split(user)
        for transaction in self.transactions:
            if transaction.from_user == user:
                total_balance -= transaction.amount
            elif transaction.to_user == user:
                total_balance += transaction.amount
        return total_balance

    def __repr__(self) -> str:
        return f"Group(name={self.groupName}, members={[member.name for member in self.members]}, expenses={self.expenses}, transactions={self.transactions})"


class Splitwise:
    def __init__(self):
        self.users = {}
        self.groups = {}

    def add_user(self, name: str) -> "User":
        user = User(name)
        self.users[name] = user
        return user

    def create_group(self, groupName: str, members: list["User"]) -> "Group":
        group = Group(groupName, members)
        self.groups[groupName] = group
        return group

    def get_user(self, name: str) -> "User":
        return self.users.get(name)

    def get_group(self, groupName: str) -> "Group":
        return self.groups.get(groupName)

    def add_expense_to_group(self, groupName: str, expense: "Expense"):
        group = self.get_group(groupName)
        if group:
            group.add_expense(expense)
        else:
            raise ValueError(f"Group {groupName} does not exist.")

    def add_transaction_to_group(self, groupName: str, transaction: "Transaction"):
        group = self.get_group(groupName)
        if group:
            group.add_transaction(transaction)
        else:
            raise ValueError(f"Group {groupName} does not exist.")

    def get_user_balance(self, userName: str, groupName: str = None) -> float:
        user = self.get_user(userName)
        if not user:
            raise ValueError(f"User {userName} does not exist.")
        if groupName:
            group = self.get_group(groupName)
            if not group:
                raise ValueError(f"Group {groupName} does not exist.")
            return group.get_balance(user)
        else:
            total_balance = 0.0
            for group in self.groups.values():
                total_balance += group.get_balance(user)
            return total_balance

    def get_group_balance(self, groupName: str) -> dict:
        group = self.get_group(groupName)
        if not group:
            raise ValueError(f"Group {groupName} does not exist.")
        balances = {}
        for member in group.members:
            balances[member.name] = group.get_balance(member)
        return balances

    def __repr__(self) -> str:
        return f"Splitwise(users={list(self.users.keys())}, groups={list(self.groups.keys())})"

