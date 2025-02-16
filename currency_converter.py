import re
import requests
from datetime import datetime
from tkinter import *
import tkinter as tk
from tkinter import ttk

class CurrencyRateFetcher():
    def __init__(self, api_url):
        self.data = self.get_currency_data(api_url)
        self.exchange_rates = self.data['rates']

    def get_currency_data(self, api_url):
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API request error: {e}")
            return None

    def calculate_conversion(self, source_currency, target_currency, amount):
        initial_amount = amount
        if source_currency != 'CAD':
            amount = amount / self.exchange_rates[source_currency]

        amount = round(amount * self.exchange_rates[target_currency], 4)
        return amount

class ConversionHistoryWindow(tk.Toplevel):
    def __init__(self, master, history_list):
        tk.Toplevel.__init__(self, master)
        self.geometry("800x600")

        self.display_history(history_list)

    def display_history(self, history_list):
        self.title_label = Label(self, text="Conversion History", font=('courier', 14, 'bold'))
        self.title_label.pack(pady=10)

        for record in history_list:
            history_record_label = Label(self, text=record, font=('courier', 10))
            history_record_label.pack(pady=5)

class CurrencyConverterApp(tk.Tk):
    def __init__(self, currency_rate_fetcher):
        tk.Tk.__init__(self)
        self.title('Currency Converter')
        self.converter = currency_rate_fetcher

        self.setup_gui()
        self.add_intro_labels()
        self.add_user_input_fields()
        self.add_conversion_result_fields()
        self.add_buttons()

    def setup_gui(self):
        self.geometry("500x400")

        self.main_frame = Frame(self)
        self.main_frame.pack(padx=10, pady=10)

    def add_intro_labels(self):
        self.greeting_label = Label(self.main_frame, text='WorldCurrency Converter 💸', fg='black', font=('courier', 16, 'bold'))
        self.greeting_label.grid(row=0, column=0, columnspan=4, pady=15)

        self.exchange_rate_label = Label(self.main_frame, text=f"1 CAD = {self.converter.calculate_conversion('CAD','USD',1)} USD\nDate: {self.converter.data['date']}", relief=tk.GROOVE, borderwidth=2, font=('courier', 10))
        self.exchange_rate_label.grid(row=1, column=0, columnspan=4, pady=10, padx=10, sticky='nsew')

    def add_user_input_fields(self):

        self.amount_label = Label(self.main_frame, text="Amount:", font=('courier', 12))
        self.amount_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')

        valid = (self.register(self.only_numbers), '%d', '%P')
        self.amount_input_field = Entry(self.main_frame, bd=2, relief=tk.RIDGE, justify=tk.CENTER, validate='key', validatecommand=valid, font=('courier', 12))
        self.amount_input_field.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        self.source_currency_var = StringVar(self.main_frame)
        self.source_currency_var.set("CAD")
        self.target_currency_var = StringVar(self.main_frame)
        self.target_currency_var.set("USD")

        font = ("courier", 12, "bold")
        self.source_currency_dropdown = ttk.Combobox(self.main_frame, textvariable=self.source_currency_var, values=list(self.converter.exchange_rates.keys()), font=font, state='readonly', justify=tk.CENTER)
        self.source_currency_dropdown.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')

        self.target_currency_dropdown = ttk.Combobox(self.main_frame, textvariable=self.target_currency_var, values=list(self.converter.exchange_rates.keys()), font=font, state='readonly', justify=tk.CENTER)
        self.target_currency_dropdown.grid(row=4, column=1, padx=10, pady=10, sticky='nsew')

    def add_conversion_result_fields(self):
        self.converted_amount_label = Label(self.main_frame, text="Converted Amount:", font=('courier', 12))
        self.converted_amount_label.grid(row=5, column=0, padx=10, pady=10, sticky='e')

        self.converted_amount_display = Label(self.main_frame, text='', fg='black', bg='white', relief=tk.RIDGE, justify=tk.CENTER, width=17, borderwidth=2, font=('courier', 12))
        self.converted_amount_display.grid(row=5, column=1, padx=10, pady=10, sticky='w')

    def add_buttons(self):
        self.convert_button = Button(self.main_frame, text="Convert", fg="black", command=self.convert_currency, font=('courier', 12, 'bold'))
        self.convert_button.grid(row=6, column=0, columnspan=2, pady=15)
        self.history_button = Button(self.main_frame, text="View History", fg="black", command=self.view_history, font=('courier', 12, 'bold'))
        self.history_button.grid(row=7, column=0, columnspan=2, pady=15)

    def convert_currency(self):
        amount = float(self.amount_input_field.get())
        source_currency = self.source_currency_var.get()
        target_currency = self.target_currency_var.get()

        converted_amount = self.converter.calculate_conversion(source_currency, target_currency, amount)
        converted_amount = round(converted_amount, 2)

        self.converted_amount_display.config(text=str(converted_amount))

        user_name = "User"  # You can customize the user name input if needed

        self.add_to_history(user_name, source_currency, target_currency, amount, converted_amount)

    def only_numbers(self, action, string):
        regex = re.compile(r'^[0-9]*\.?[0-9]*$')
        result = regex.match(string)
        return (string == "" or (string.count('.') <= 1 and result is not None))

    def add_to_history(self, user_name, source_currency, target_currency, amount, converted_amount):
        history_record = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {user_name}: {amount} {source_currency} to {converted_amount} {target_currency}"

        if hasattr(self, 'conversion_history'):
            self.conversion_history.insert(0, history_record)
            self.conversion_history = self.conversion_history[:10]
        else:
            self.conversion_history = [history_record]

    def view_history(self):
        if hasattr(self, 'conversion_history'):
            history_window = ConversionHistoryWindow(self, self.conversion_history)
            history_window.grab_set()
        else:
            self.conversion_history = []
            print("No history available.")

if __name__ == '__main__':
    api_url = 'https://api.exchangerate-api.com/v4/latest/CAD'
    rate_fetcher = CurrencyRateFetcher(api_url)
    app = CurrencyConverterApp(rate_fetcher)
    app.mainloop()
