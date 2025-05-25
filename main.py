from tkinter import *
from functools import partial
from tkinter import ttk, messagebox
import calculation_finance as calc
import all_constants as c
from datetime import date


class PersonalFinanceCalculator:
    """
    Personal Finance Calculator with multiple financial tools
    """

    def __init__(self, root):
        """
        Initialize Finance Calculator GUI
        """
        self.root = root
        self.calculation_history = []  # Store calculation history
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

    def add_to_history(self, calculation_string):
        """Add a calculation to the history"""
        today = date.today().strftime("%d/%m/%Y")
        history_entry = f"[{today}] {calculation_string}"
        self.calculation_history.append(history_entry)

    def get_current_tab_name(self):
        """Get the name of currently selected tab"""
        current_tab = self.notebook.index(self.notebook.select())
        return self.notebook.tab(current_tab, option="text")

    def validate_inputs(self, tab_name, required_fields, field_types=None):
        """Validate input fields for calculations with user-friendly error messages"""
        values = []

        for i, field in enumerate(required_fields):
            field_value = self.entries[tab_name][field].get().strip()

            # Check if field is empty
            if not field_value:
                error_msg = f"❌ Please enter a value for {field}"
                self.result_labels[tab_name].config(text=error_msg, fg="#CC0000")
                return None

            try:
                value = float(field_value)

                # Check for negative values
                if value < 0:
                    error_msg = f"❌ {field} cannot be negative. Please enter a positive number."
                    self.result_labels[tab_name].config(text=error_msg, fg="#CC0000")
                    return None

                # Special validation for percentages
                if "%" in field:
                    if value > 100:
                        error_msg = f"❌ {field} seems too high ({value}%). Please check your percentage."
                        self.result_labels[tab_name].config(text=error_msg, fg="#CC0000")
                        return None
                    if "Interest Rate" in field and value > 50:
                        error_msg = f"❌ Interest rate of {value}% seems unusually high. Please verify."
                        self.result_labels[tab_name].config(text=error_msg, fg="#CC0000")
                        return None

                # Special validation for ages
                if "Age" in field:
                    if value < 16 or value > 120:
                        error_msg = f"❌ {field} of {int(value)} seems unrealistic. Please enter a valid age."
                        self.result_labels[tab_name].config(text=error_msg, fg="#CC0000")
                        return None

                # Special validation for years/terms
                if "Term" in field or "Period" in field:
                    if value > 50:
                        error_msg = f"❌ {field} of {int(value)} years seems too long. Please check your input."
                        self.result_labels[tab_name].config(text=error_msg, fg="#CC0000")
                        return None

                values.append(value)

            except ValueError:
                error_msg = f"❌ Please enter numbers only for {field}. Remove any letters or symbols."
                self.result_labels[tab_name].config(text=error_msg, fg="#CC0000")
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

                # Add to history
                history_entry = f"Loan: Amount: {calc.format_nz_currency(principal)}, Rate: {annual_rate}%, Term: {int(years)} years → Monthly: {calc.format_nz_currency(monthly_payment)}"
                self.add_to_history(history_entry)

            except Exception as e:
                error_msg = f"❌ Calculation error: Unable to process your loan details. Please check your inputs."
                self.result_labels[tab_name].config(text=error_msg, fg="#CC0000")

    def calculate_mortgage(self):
        """Calculate mortgage payment using NZ-specific calculations"""
        tab_name = "Mortgage Calculator"
        fields = ["Home Price (NZD)", "Down Payment (NZD)", "Annual Interest Rate (%)", "Mortgage Term (Years)"]
        values = self.validate_inputs(tab_name, fields)

        if values:
            home_price, down_payment, annual_rate, years = values

            # Custom validation for mortgage
            if down_payment >= home_price:
                error_msg = "❌ Down payment cannot be equal to or greater than the home price."
                self.result_labels[tab_name].config(text=error_msg, fg="#CC0000")
                return

            try:
                mortgage_details = calc.calculate_nz_mortgage_payment(
                    home_price, down_payment, annual_rate, years
                )

                lvr_warning = " (LMI Required)" if mortgage_details['requires_lmi'] else ""

                result_text = (f"Monthly Payment: {calc.format_nz_currency(mortgage_details['monthly_payment'])}\n"
                               f"+ Insurance: {calc.format_nz_currency(mortgage_details['insurance_monthly'])}\n"
                               f"Total Monthly: {calc.format_nz_currency(mortgage_details['total_monthly_payment'])}\n"
                               f"LVR: {mortgage_details['lvr']:.1f}%{lvr_warning}\n"
                               f"Total Interest: {calc.format_nz_currency(mortgage_details['total_interest'])}")

                self.result_labels[tab_name].config(text=result_text, fg="#0066CC")

                # Add to history
                history_entry = f"Mortgage: Home: {calc.format_nz_currency(home_price)}, Down: {calc.format_nz_currency(down_payment)}, Rate: {annual_rate}% → Monthly: {calc.format_nz_currency(mortgage_details['total_monthly_payment'])}, LVR: {mortgage_details['lvr']:.1f}%"
                self.add_to_history(history_entry)

            except Exception as e:
                error_msg = f"❌ Calculation error: Unable to process your mortgage details. Please check your inputs."
                self.result_labels[tab_name].config(text=error_msg, fg="#CC0000")

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

                # Add to history
                history_entry = f"Investment: Initial: {calc.format_nz_currency(initial_investment)}, Annual: {calc.format_nz_currency(annual_contribution)}, Return: {annual_return_rate}%, Period: {int(years)} years → Final: {calc.format_nz_currency(investment_details['final_value'])}"
                self.add_to_history(history_entry)

            except Exception as e:
                error_msg = f"❌ Calculation error: Unable to process your investment details. Please check your inputs."
                self.result_labels[tab_name].config(text=error_msg, fg="#CC0000")

    def calculate_retirement(self):
        """Calculate KiwiSaver retirement projection"""
        tab_name = "Retirement Planner"
        fields = ["Current Age", "Retirement Age", "Current KiwiSaver Balance (NZD)", "Annual Salary (NZD)",
                  "Employee Contribution Rate (%)", "Expected Annual Return (%)"]
        values = self.validate_inputs(tab_name, fields)

        if values:
            current_age, retirement_age, current_balance, annual_salary, employee_rate, expected_return = values

            # Custom validation for retirement
            if retirement_age <= current_age:
                error_msg = f"❌ Retirement age ({int(retirement_age)}) must be greater than current age ({int(current_age)})."
                self.result_labels[tab_name].config(text=error_msg, fg="#CC0000")
                return

            # Show warning for early retirement (but don't block calculation)
            warning_text = ""
            if retirement_age < 65:
                warning_text = "\n⚠️ Note: NZ Super is available from age 65"

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
                    f"Years to Retirement: {retirement_details['years_to_retirement']}{warning_text}")

                self.result_labels[tab_name].config(text=result_text, fg="#0066CC")

                # Add to history
                history_entry = f"Retirement: Age: {int(current_age)}→{int(retirement_age)}, Balance: {calc.format_nz_currency(current_balance)}, Salary: {calc.format_nz_currency(annual_salary)} → Retirement Balance: {calc.format_nz_currency(retirement_details['projected_balance'])}"
                self.add_to_history(history_entry)

            except Exception as e:
                error_msg = f"❌ Calculation error: Unable to process your retirement details. Please check your inputs."
                self.result_labels[tab_name].config(text=error_msg, fg="#CC0000")

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
        if not self.calculation_history:
            # Show inline message instead of popup
            current_tab = self.get_current_tab_name()
            error_msg = "📝 No calculations saved yet. Perform some calculations first to see your history."
            self.result_labels[current_tab].config(text=error_msg, fg="#FF8800")
        else:
            HistoryExport(self, self.calculation_history)


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


class HistoryExport:
    """
    Displays history dialog box and export button for finance calculations
    """

    def __init__(self, partner, calculations):
        self.history_box = Toplevel()
        partner.button_ref_list[1].config(state=DISABLED)  # Disable history button

        self.history_box.protocol('WM_DELETE_WINDOW', partial(self.close_history, partner))
        self.history_box.title("Finance Calculation History")

        self.history_frame = Frame(self.history_box)
        self.history_frame.grid()

        # Determine background color and calculation display
        calc_back = "#D5E8D4" if len(calculations) <= c.MAX_FINANCE_CALCS else "#ffe6cc"
        calc_amount = "all your" if len(
            calculations) <= c.MAX_FINANCE_CALCS else f"your recent calculations - showing {c.MAX_FINANCE_CALCS} / {len(calculations)}"

        recent_intro_txt = f"Below are {calc_amount} financial calculations"

        # Show most recent calculations first
        newest_first_list = list(reversed(calculations))
        newest_first_string = "\n".join(newest_first_list[:c.MAX_FINANCE_CALCS])

        export_instruction_txt = (
            "Please push <Export> to save your calculations in a file. "
            "If the filename already exists, it will be overwritten."
        )

        # Create labels
        history_labels_list = [
            ["Finance History / Export", ("Arial", 16, "bold"), None],
            [recent_intro_txt, ("Arial", 11), None],
            [newest_first_string, ("Arial", 11), calc_back],  # Reduced font size from 14 to 11
            [export_instruction_txt, ("Arial", 11), None],
        ]

        history_labels_ref = []
        for count, item in enumerate(history_labels_list):
            make_label = Label(
                self.history_frame, text=item[0], font=item[1],
                bg=item[2], wraplength=400, justify="left", padx=15, pady=8  # Increased wraplength, reduced padding
            )
            make_label.grid(row=count, padx=10, pady=5)  # Added grid padding for better spacing
            history_labels_ref.append(make_label)

        self.export_filename_label = history_labels_ref[3]

        # Button frame
        self.history_button_frame = Frame(self.history_box)
        self.history_button_frame.grid(row=4)

        button_details_list = [
            ["Export", "#004C99", lambda: self.export_data(calculations), 0, 0],
            ["Close", "#666666", partial(self.close_history, partner), 0, 1]
        ]

        for btn in button_details_list:
            make_button = Button(
                self.history_button_frame, font=("Arial", 12, "bold"),
                text=btn[0], bg=btn[1], fg="#FFFFFF", width=12,
                command=btn[2]
            )
            make_button.grid(row=btn[3], column=btn[4], padx=20, pady=10)

    def export_data(self, calculations):
        """Export calculation data to a text file"""
        today = date.today()

        # Get day, month and year as individual strings
        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")

        file_name = f"finance_{year}_{month}_{day}"

        write_to = f"{file_name}.txt"

        try:
            with open(write_to, "w") as text_file:
                text_file.write("***** Personal Finance Calculations *****\n")
                text_file.write(f"Generated: {day}/{month}/{year}\n\n")
                text_file.write("Here is your calculation history (oldest to newest)...\n\n")

                # Write calculations in chronological order (oldest first)
                for item in calculations:
                    text_file.write(item)
                    text_file.write("\n")

            # Show success message
            success_string = f"✅ Export successful! File saved as {file_name}.txt"
            self.export_filename_label.config(fg="#009900", text=success_string,
                                              font=("Arial", "11", "bold"))

        except Exception as e:
            error_string = f"❌ Export failed: {str(e)}"
            self.export_filename_label.config(fg="#CC0000", text=error_string,
                                              font=("Arial", "11", "bold"))

    def close_history(self, partner):
        """Close history dialog and re-enable history button"""
        partner.button_ref_list[1].config(state=NORMAL)
        self.history_box.destroy()


# Main execution
if __name__ == "__main__":
    root = Tk()
    root.title("Personal Finance Calculator")
    PersonalFinanceCalculator(root)
    root.mainloop()