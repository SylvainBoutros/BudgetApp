class Category:
    # Initialize class object assign category name and create empty list instance
    def __init__(self, name):
        self.name = name
        self.ledger = []

    # Format the printing of the object
    def __str__(self):
        how_many = 30 - len(self.name)
        results = "*" * (how_many//2) + self.name + "*" * (how_many//2) + "\n"
        for i in self.ledger:
            results += f"{i['description'][:23].ljust(23)}" + str('{:.2f}'.format(i['amount'])).rjust(7) + "\n"

        total = self.get_balance()
        results += f"Total: {total}"
        return results

    # Deposit function
    def deposit(self, amount, description="") -> None:
        self.ledger.append({'amount': amount, 'description': description})

    # Withdraw function
    def withdraw(self, amount, description="") -> bool:
        current_amount = self.check_funds(amount)
        if current_amount:
            self.ledger.append({'amount': -amount, 'description': description})
        return current_amount

    # Get balance of the account
    def get_balance(self) -> float:
        total = 0.0
        for v in self.ledger:
            total += v['amount']

        return total

    # Create a transfer between categories
    def transfer(self, amount, categories):
        tmp = self.check_funds(amount)
        if tmp:
            self.withdraw(amount, description=("Transfer to " + categories.name))
            categories.deposit(amount, description=("Transfer from " + self.name))
            return True
        return False

    # Check if there is enough money in the account
    def check_funds(self, amount):
        current_balance = self.get_balance()
        if current_balance < amount:
            return False
        return True

# Creates a chart that display percentage spending
def create_spend_chart(categories):
    # Get total withdrawals and names of categories
    total_withdrawals = 0
    category_names = []
    for category in categories:
        withdrawals = sum(transaction['amount'] for transaction in category.ledger if transaction['amount'] < 0)
        total_withdrawals += withdrawals
        category_names.append(category.name)

    # Calculate percentage spent per category
    category_percents = []
    for category in categories:
        withdrawals = sum(transaction['amount'] for transaction in category.ledger if transaction['amount'] < 0)
        percent = int((withdrawals / total_withdrawals) * 100)
        category_percents.append(percent)

    # Build chart
    chart = "Percentage spent by category\n"
    for i in range(100, -10, -10):
        chart += str(i).rjust(3) + "| "
        for percent in category_percents:
            if percent >= i:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"

    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # Get longest category name
    max_len = max(len(name) for name in category_names)

    # Build category names row
    for i in range(max_len):
        chart += "     "
        for name in category_names:
            if i >= len(name):
                chart += "   "
            else:
                chart += name[i] + "  "
        if i != max_len - 1:
            chart += "\n"

    return chart
