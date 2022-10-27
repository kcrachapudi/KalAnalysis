import pandas as pd
from pathlib import Path
import numpy as np
import questionary

class Customer:
    cust_expected_return = 0.0
    cust_risk_profile = ''
    cust_risk_val = 0.0
    cust_inv_amount = 0.00
    final_ticker = ''

    def customer_details(self):
        return f'Customer: Risk Profile: {self.cust_risk_profile}, Investment Amount: {self.cust_inv_amount} '
