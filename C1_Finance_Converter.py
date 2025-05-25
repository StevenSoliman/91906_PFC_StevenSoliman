from tkinter import *
from functools import partial
from tkinter import ttk, messagebox
import calculation_finance as calc


class PersonalFinanceCalculator:
    """
    Personal Finance Calculator with multiple financial tools
    """

    def __init__(self, root):
        """
        Initialize Finance Calculator GUI
        """
        self.root = root
        self.setup_main_frame()
        self.create_header()
        self.create_notebook()
        self.setup_tab_content()
        self.create_buttons()

    def setup_main_frame(self):
        """Setup main container frame"""
        self.finance_frame = Frame(padx=40, pady=40)
        self.finance_frame.pack(expand=True, fill="both")

    def create_header(self):
        """Create header section"""
        self.finance_heading = Label(self.finance_frame,
                                     text="Personal Finance Calculator",
                                     font=("Arial", "16", "bold"))
        self.finance_heading.pack(pady=(0, 10))

        instructions = ("Use the tabs below to access different financial calculators. "
                        "Enter the required information and press the calculate button.")
        self.finance_instructions = Label(self.finance_frame,
                                          text=instructions,
                                          wraplength=400,
                                          justify="center")
        self.finance_instructions.pack(pady=(0, 20))

    def create_notebook(self):
        """Create tabbed interface"""
        self.notebook = ttk.Notebook(self.finance_frame)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Create tab frames
        self.tabs = {
            "Loan Calculator": ttk.Frame(self.notebook),
            "Mortgage Calculator": ttk.Frame(self.notebook),
            "Investment Projector": ttk.Frame(self.notebook),
            "Retirement Planner": ttk.Frame(self.notebook)
        }

        # Add tabs to notebook
        for tab_name, tab_frame in self.tabs.items():
            self.notebook.add(tab_frame, text=tab_name)

    def setup_tab_content(self):
        """Setup content for each tab"""
        tab_configs = {
            "Loan Calculator": {
                "fields": ["Loan Amount (NZD)", "Annual Interest Rate (%)", "Loan Term (Years)"],
                "button_text": "Calculate Loan",
                "command": self.calculate_loan
            },
            "Mortgage Calculator": {
                "fields": ["Home Price (NZD)", "Down Payment (NZD)", "Annual Interest Rate (%)",
                           "Mortgage Term (Years)"],
                "button_text": "Calculate Mortgage",
                "command": self.calculate_mortgage
            },
            "Investment Projector": {
                "fields": ["Initial Investment (NZD)", "Annual Contribution (NZD)", "Annual Return Rate (%)",
                           "Investment Period (Years)"],
                "button_text": "Calculate Investment",
                "command": self.calculate_investment
            },
            "Retirement Planner": {
                "fields": ["Current Age", "Retirement Age", "Current KiwiSaver Balance (NZD)", "Annual Salary (NZD)",
                           "Employee Contribution Rate (%)", "Expected Annual Return (%)"],
                "button_text": "Calculate Retirement",
                "command": self.calculate_retirement
            }
        }

        self.entries = {}
        self.result_labels = {}

        for tab_name, config in tab_configs.items():
            tab_frame = self.tabs[tab_name]
            self.entries[tab_name] = {}

            # Create input frame (centered)
            input_frame = Frame(tab_frame)
            input_frame.pack(expand=True, pady=20)

            # Create input fields
            for i, field_name in enumerate(config["fields"]):
                Label(input_frame, text=field_name, font=("Arial", 10)).grid(row=i, column=0, sticky="w", padx=5,
                                                                             pady=5)
                entry = Entry(input_frame, width=20, font=("Arial", 10))
                entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries[tab_name][field_name] = entry

            # Create calculate button (centered)
            calc_button = Button(input_frame,
                                 text=config["button_text"],
                                 bg="#0066CC", fg="white",
                                 font=("Arial", 12, "bold"),
                                 command=config["command"],
                                 width=20)
            calc_button.grid(row=len(config["fields"]), column=0, columnspan=2, pady=20)

            # Create result label
            self.result_labels[tab_name] = Label(input_frame,
                                                 text="",
                                                 font=("Arial", 11, "bold"),
                                                 fg="#0066CC",
                                                 wraplength=300)
            self.result_labels[tab_name].grid(row=len(config["fields"]) + 1, column=0, columnspan=2, pady=10)

    def create_buttons(self):
        """Create main action buttons"""
        button_frame = Frame(self.finance_frame)
        button_frame.pack(pady=20)

        # Button list (button text | bg color | command | row | column)
        button_details_list = [
            ["Help/Info", "#CC6600", self.to_help, 0, 0],
            ["History/Export", "#004C99", self.to_history, 0, 1]
        ]

        self.button_ref_list = []

        for item in button_details_list:
            button = Button(button_frame,
                            text=item[0], bg=item[1],
                            fg="#FFFFFF", font=("Arial", 12, "bold"),
                            width=15, command=item[2])
            button.grid(row=item[3], column=item[4], padx=10, pady=5)
            self.button_ref_list.append(button)

        # Disable history button initially
        self.button_ref_list[1].config(state=DISABLED)

    def get_current_tab_name(self):
        """Get the name of currently selected tab"""
        current_tab = self.notebook.index(self.notebook.select())
        return self.notebook.tab(current_tab, option="text")

    def validate_inputs(self, tab_name, required_fields):
        """Validate input fields for calculations"""
        values = []
        for field in required_fields:
            try:
                value = float(self.entries[tab_name][field].get())
                if value < 0:
                    raise ValueError("Negative values not allowed")
                values.append(value)
            except ValueError:
                messagebox.showerror("Input Error", f"Please enter a valid positive number for {field}")
                return None
        return values

    def calculate_loan(self):
        """Calculate loan payment using NZ-specific calculations"""
        tab_name = "Loan Calculator"
        fields = ["Loan Amount (NZD)", "Annual Interest Rate (%)", "Loan Term (Years)"]
        values = self.validate_inputs(tab_name, fields)

        if values:
            principal, annual_rate, years = values

            try:
                monthly_payment, total_interest, total_amount = calc.calculate_loan_payment(
                    principal, annual_rate, years
                )

                result_text = (f"Monthly Payment: {calc.format_nz_currency(monthly_payment)}\n"
                               f"Total Interest: {calc.format_nz_currency(total_interest)}\n"
                               f"Total Amount: {calc.format_nz_currency(total_amount)}")

                self.result_labels[tab_name].config(text=result_text, fg="#0066CC")

            except Exception as e:
                messagebox.showerror("Calculation Error", f"Error calculating loan: {str(e)}")

    def calculate_mortgage(self):
        """Calculate mortgage payment using NZ-specific calculations"""
        tab_name = "Mortgage Calculator"
        fields = ["Home Price (NZD)", "Down Payment (NZD)", "Annual Interest Rate (%)", "Mortgage Term (Years)"]
        values = self.validate_inputs(tab_name, fields)

        if values:
            home_price, down_payment, annual_rate, years = values

            if down_payment >= home_price:
                messagebox.showerror("Input Error", "Down payment cannot be greater than or equal to home price")
                return

            try:
                mortgage_details = calc.calculate_nz_mortgage_payment(
                    home_price, down_payment, annual_rate, years
                )

                lvr_warning = " ⚠️ LMI Required" if mortgage_details['requires_lmi'] else ""

                result_text = (f"Monthly Payment: {calc.format_nz_currency(mortgage_details['monthly_payment'])}\n"
                               f"+ Insurance: {calc.format_nz_currency(mortgage_details['insurance_monthly'])}\n"
                               f"Total Monthly: {calc.format_nz_currency(mortgage_details['total_monthly_payment'])}\n"
                               f"LVR: {mortgage_details['lvr']:.1f}%{lvr_warning}\n"
                               f"Total Interest: {calc.format_nz_currency(mortgage_details['total_interest'])}")

                self.result_labels[tab_name].config(text=result_text, fg="#0066CC")

            except Exception as e:
                messagebox.showerror("Calculation Error", f"Error calculating mortgage: {str(e)}")

    def calculate_investment(self):
        """Calculate investment growth using NZ-specific calculations with tax considerations"""
        tab_name = "Investment Projector"
        fields = ["Initial Investment (NZD)", "Annual Contribution (NZD)", "Annual Return Rate (%)",
                  "Investment Period (Years)"]
        values = self.validate_inputs(tab_name, fields)

        if values:
            initial_investment, annual_contribution, annual_return_rate, years = values

            try:
                investment_details = calc.calculate_investment_growth_nz(
                    initial_investment, annual_contribution, annual_return_rate, years, include_tax=True
                )

                result_text = (f"Final Value: {calc.format_nz_currency(investment_details['final_value'])}\n"
                               f"Total Contributions: {calc.format_nz_currency(investment_details['total_contributions'])}\n"
                               f"Growth (After PIE Tax): {calc.format_nz_currency(investment_details['total_growth'])}\n"
                               f"Effective Return: {investment_details['effective_annual_return']:.2f}%\n"
                               f"Est. Tax Paid: {calc.format_nz_currency(investment_details['tax_paid_estimate'])}")

                self.result_labels[tab_name].config(text=result_text, fg="#0066CC")

            except Exception as e:
                messagebox.showerror("Calculation Error", f"Error calculating investment: {str(e)}")

    def calculate_retirement(self):
        """Calculate KiwiSaver retirement projection"""
        tab_name = "Retirement Planner"
        fields = ["Current Age", "Retirement Age", "Current KiwiSaver Balance (NZD)", "Annual Salary (NZD)",
                  "Employee Contribution Rate (%)", "Expected Annual Return (%)"]
        values = self.validate_inputs(tab_name, fields)

        if values:
            current_age, retirement_age, current_balance, annual_salary, employee_rate, expected_return = values

            if retirement_age <= current_age:
                messagebox.showerror("Input Error", "Retirement age must be greater than current age")
                return

            if retirement_age < 65:
                messagebox.showwarning("NZ Super Warning", "Note: NZ Super is available from age 65")

            try:
                retirement_details = calc.calculate_kiwisaver_retirement(
                    current_age, retirement_age, current_balance, annual_salary,
                    employee_rate, expected_return, salary_growth=2
                )

                total_annual_income = retirement_details['annual_nz_super'] + retirement_details[
                    'sustainable_annual_withdrawal']

                result_text = (
                    f"KiwiSaver at Retirement: {calc.format_nz_currency(retirement_details['projected_balance'])}\n"
                    f"Annual NZ Super: {calc.format_nz_currency(retirement_details['annual_nz_super'])}\n"
                    f"Sustainable Withdrawal: {calc.format_nz_currency(retirement_details['sustainable_annual_withdrawal'])}\n"
                    f"Total Annual Income: {calc.format_nz_currency(total_annual_income)}\n"
                    f"Years to Retirement: {retirement_details['years_to_retirement']}")

                self.result_labels[tab_name].config(text=result_text, fg="#0066CC")

            except Exception as e:
                messagebox.showerror("Calculation Error", f"Error calculating retirement: {str(e)}")

    def to_help(self):
        """Open help dialogue box"""
        tab_name = self.get_current_tab_name()

        help_texts = {
            "Loan Calculator": (
                "Loan Calculator Instructions:\n\n"
                "• Enter the loan amount you want to borrow (NZD)\n"
                "• Enter the annual interest rate (in %)\n"
                "• Enter the loan term in years\n"
                "• Click 'Calculate Loan' to see your monthly payment, total interest, and total amount\n\n"
                "Results include NZ currency formatting and comprehensive payment breakdown."
            ),
            "Mortgage Calculator": (
                "Mortgage Calculator Instructions:\n\n"
                "• Enter the total home price (NZD)\n"
                "• Enter your down payment amount (NZD)\n"
                "• Enter the annual interest rate (in %)\n"
                "• Enter the mortgage term in years\n"
                "• Click 'Calculate Mortgage' to see detailed breakdown\n\n"
                "Results include LVR calculation, insurance estimates, and LMI requirements for NZ mortgages."
            ),
            "Investment Projector": (
                "Investment Calculator Instructions:\n\n"
                "• Enter your initial investment amount (NZD)\n"
                "• Enter how much you'll contribute annually (NZD)\n"
                "• Enter the expected annual return rate (in %)\n"
                "• Enter the investment period in years\n"
                "• Click 'Calculate Investment' to see growth projection\n\n"
                "Results include PIE tax considerations (28% rate) for accurate NZ projections."
            ),
            "Retirement Planner": (
                "KiwiSaver Retirement Calculator Instructions:\n\n"
                "• Enter your current age\n"
                "• Enter your desired retirement age (NZ Super available from 65)\n"
                "• Enter your current KiwiSaver balance (NZD)\n"
                "• Enter your current annual salary (NZD)\n"
                "• Enter your KiwiSaver contribution rate (3%, 4%, 6%, 8%, or 10%)\n"
                "• Enter expected annual return rate (in %)\n"
                "• Click 'Calculate Retirement' for detailed retirement planning\n\n"
                "Includes employer contributions, government contributions, NZ Super estimates, and sustainable withdrawal calculations."
            )
        }

        selected_help_text = help_texts.get(tab_name, "No help available for this tab.")
        DisplayHelp(self, selected_help_text)

    def to_history(self):
        """Handle history/export functionality"""
        messagebox.showinfo("Coming Soon", "History and Export functionality will be available in a future update.")


class DisplayHelp:
    """Help dialog class"""

    def __init__(self, partner, help_text):
        background = "#ffe6cc"
        self.help_box = Toplevel()
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))
        self.help_box.title("Help")
        self.help_box.geometry("450x300")
        self.help_box.resizable(False, False)

        # Disable help button
        partner.button_ref_list[0].config(state=DISABLED)

        self.help_frame = Frame(self.help_box, bg=background)
        self.help_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.help_heading_label = Label(self.help_frame,
                                        text="Help / Info",
                                        font=("Arial", 16, "bold"),
                                        bg=background)
        self.help_heading_label.pack(pady=(0, 15))

        self.help_text_label = Label(self.help_frame,
                                     text=help_text,
                                     wraplength=400,
                                     justify="left",
                                     bg=background,
                                     font=("Arial", 10))
        self.help_text_label.pack(expand=True)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", 12, "bold"),
                                     text="Dismiss",
                                     bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner),
                                     width=15)
        self.dismiss_button.pack(pady=(15, 0))

    def close_help(self, partner):
        """Close help dialog and re-enable help button"""
        partner.button_ref_list[0].config(state=NORMAL)
        self.help_box.destroy()


# Main execution
if __name__ == "__main__":
    root = Tk()
    root.title("Personal Finance Calculator")
    PersonalFinanceCalculator(root)
    root.mainloop()