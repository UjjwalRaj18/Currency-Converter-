# Currency Converter Application
This application allows users to convert between different currencies based on real-time exchange rates. It uses the Exchange Rate API to fetch live currency rates and provides a graphical user interface (GUI) to make the conversion easy.

# Features
Convert between any two currencies.
Display live exchange rates.
Track and view the history of previous conversions.
Input validation for the amount field to ensure only numeric values are entered.
# Components
The project consists of several key components:

1. CurrencyRateFetcher Class
   
Fetches live currency exchange data from a given API URL.
Provides conversion rates for multiple currencies.

2. CurrencyConverterApp Class
   
The main GUI class using tkinter to create an interactive window for currency conversion.
Lets users input an amount, choose source and target currencies, and view the converted amount.
Includes history tracking of previous conversions.

3. ConversionHistoryWindow Class

A secondary window that displays the conversion history.

4. Conversion Logic
   
The calculate_conversion method computes the converted amount based on the provided source and target currencies.

5.Requirements

Python 3.x
requests library
tkinter library (included with standard Python installations)
