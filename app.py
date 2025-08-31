import streamlit as st

class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def check_funds(self, amount):
        funds = self.get_balance()
        if amount > funds:
            return False
        return True

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        return False

    def transfer(self, amount, other_category):
        if self.check_funds(amount):
            self.withdraw(amount, description='Transfer to ' + other_category.name)
            other_category.deposit(amount, description='Transfer from ' + self.name)
            return True
        return False

    def __str__(self):
        title = f'{self.name}'.center(30, '*')
        ledger_str = ''
        for item in self.ledger:
            description = item['description'][:23].ljust(23)
            amount = f'{item["amount"]:.2f}'.rjust(7)
            ledger_str += f'{description}{amount}\n'
        total = self.get_balance()
        total_str = f'Total: {total:.2f}'

        return title + '\n' + ledger_str + total_str

    def get_balance(self):
        total = 0
        for item in self.ledger:
            total += item['amount']
        return total

def create_spend_chart(categories):
    spent_amounts = []
    for category in categories:
        total_spent = 0
        for item in category.ledger:
            if item['amount'] < 0:
                total_spent += abs(item['amount'])
        spent_amounts.append(total_spent)

    total_spend = sum(spent_amounts)
    if total_spend == 0:
        percentages = [0] * len(categories)
    else:
        percentages = []
        for amount in spent_amounts:
            percentage = (amount / total_spend) * 100
            rounded_percentage = int(percentage / 10) * 10
            percentages.append(rounded_percentage)

    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += str(i).rjust(3) + "| "
        for percentage in percentages:
            if percentage >= i:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"
    
    chart += "    " + "---" * len(categories) + "-\n"

    longest_name_length = 0
    for category in categories:
        if len(category.name) > longest_name_length:
            longest_name_length = len(category.name)

    for i in range(longest_name_length):
        chart += "     "
        for category in categories:
            if i < len(category.name):
                chart += category.name[i] + "  "
            else:
                chart += "   "
        if i < longest_name_length - 1:
            chart += "\n"
    
    return chart

# --- Interfaz de Usuario de Streamlit ---

# Título de la aplicación
st.title("Aplicación de Presupuesto Personal")
st.write("Esta aplicación muestra un resumen de gastos por categoría.")

# Definir las categorías y agregar datos de ejemplo
food = Category("Food")
clothing = Category("Clothing")
auto = Category("Auto")

food.deposit(1000, "initial deposit")
food.withdraw(10.55, "groceries")
food.withdraw(15.89, "restaurant and more food")
clothing.deposit(100, "initial deposit")
clothing.withdraw(20.30, "t-shirt")
food.transfer(50, clothing)
auto.deposit(200, "initial deposit")
auto.withdraw(150.00, "gas")

categories = [food, clothing, auto]

# Mostrar los datos del gráfico
st.header("Gráfico de Gastos por Categoría")
chart_output = create_spend_chart(categories)
st.text(chart_output)

# Mostrar el detalle de cada categoría
st.header("Detalle del Libro Mayor")
st.text(food)
st.text(clothing)
st.text(auto)