from tkinter import *
from functools import partial
from tkinter import ttk, messagebox

class FinanceCalculator:
    """
       Finance Calculator with multiple financial tools
       """

    def __init__(self):
        """
        Finance Calculator GUI
        """

        self.finance_frame = Frame(padx=40, pady=40)
        self.finance_frame.grid()

        # Heading
        self.finance_heading = Label(self.finance_frame,
                                     text="Finance Calculator",
                                     font=("Arial", "16", "bold"))
        self.finance_heading.grid(row=0)

        # Intructions
        instructions = ("Use the tabs below to access different financial calculators. "
                        "Enter the required information and press the calculate button.")
        self.finance_instructions = Label(self.finance_frame,
                                          text=instructions,
                                          wraplength=250, width=40,
                                          justify="left")
        self.finance_instructions.grid(row=1)

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.finance_frame)
        self.notebook.grid(row=2, padx=10, pady=10)

        # Create tabs (empty frames for now)
        self.loan_tab = ttk.Frame(self.notebook)
        self.mortgage_tab = ttk.Frame(self.notebook)
        self.investment_tab = ttk.Frame(self.notebook)
        self.retirement_tab = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.loan_tab, text="Loan Calculator")
        self.notebook.add(self.mortgage_tab, text="Mortgage Calculator")
        self.notebook.add(self.investment_tab, text="Investment Projector")
        self.notebook.add(self.retirement_tab, text="Retirement Planner")

        # Help and history buttons frame
        self.button_frame = Frame(self.finance_frame)
        self.button_frame.grid(row=3)

        # Conversion, help and history/export buttons
        self.button_frame = Frame(self.finance_frame)
        self.button_frame.grid(row=4)

        button_details_list = [
            ["Help/Info", "#CC6600", self.to_help, 1, 0],
            ["History / Export", "#004C99", "", 1, 1]
        ]

        # List to hold buttons once they have been made
        self.button_ref_list = []

        for item in button_details_list:
            button = Button(self.button_frame,
                            text=item[0], bg=item[1],
                            fg="#FFFFFF", font=("Arial", "12", "bold"),
                            width=12, command=item[2])
            button.grid(row=item[3], column=item[4], padx=5, pady=5)
            self.button_ref_list.append(button)

            # Assign to specific button attributes
            if item[0] == "Help/Info":
                self.to_help_button = button
            elif item[0] == "History / Export":
                self.to_history_button = button

        # Retrieve 'history / export' button and disable it at the start
        self.to_history_button = self.button_ref_list[1].config(state=DISABLED)

    def to_help(self):
        """
        Open help dialogue box and show text based on current tab.
        """
        current_tab = self.notebook.index(self.notebook.select())
        tab_name = self.notebook.tab(current_tab, option="text")

        help_texts = {
            "Loan Calculator": (
                "Loan Calculator Instructions:\n\n"
                "• Enter the loan amount you want to borrow (NZD)\n"
                "• Enter the annual interest rate (in %)\n"
                "• Enter the loan term in years\n"
                "• Click 'Calculate Loan Payment' to see your monthly payment, total interest, and total amount\n\n"
                "Results include NZ currency formatting and comprehensive payment breakdown."
            ),
            "Mortgage Calculator": (
                "Mortgage Calculator Instructions:\n\n"
                "• Enter the total home price (NZD)\n"
                "• Enter your down payment amount (NZD)\n"
                "• Enter the annual interest rate (in %)\n"
                "• Enter the mortgage term in years\n"
                "• Click 'Calculate Mortgage Payment' to see detailed breakdown\n\n"
                "Results include LVR calculation, insurance estimates, and LMI requirements for NZ mortgages."
            ),
            "Investment Projector": (
                "Investment Calculator Instructions:\n\n"
                "• Enter your initial investment amount (NZD)\n"
                "• Enter how much you'll contribute annually (NZD)\n"
                "• Enter the expected annual return rate (in %)\n"
                "• Enter the investment period in years\n"
                "• Click 'Calculate Future Value' to see growth projection\n\n"
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
                "• Click 'Calculate KiwiSaver Projection' for detailed retirement planning\n\n"
                "Includes employer contributions, government contributions, NZ Super estimates, and sustainable withdrawal calculations."
            )
        }

        selected_help_text = help_texts.get(tab_name, "No help available for this tab.")
        DisplayHelp(self, selected_help_text)


class DisplayHelp:

    def __init__(self, partner, help_text):
        background = "#ffe6cc"
        self.help_box = Toplevel()
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        # Store reference to help button
        partner.to_help_button.config(state=DISABLED)

        self.help_frame = Frame(self.help_box, width=300, height=200)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame, text="Help / Info", font=("Arial", 14, "bold"))
        self.help_heading_label.grid(row=0)

        self.help_text_label = Label(self.help_frame, text=help_text, wraplength=350, justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame, font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#CC6600", fg="#FFFFFF",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        for item in [self.help_frame, self.help_heading_label, self.help_text_label]:
            item.config(bg=background)

    def close_help(self, partner):
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()



# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Finance Calculator")
    FinanceCalculator()
    root.mainloop()
