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

       #Heading
       self.finance_heading = Label(self.finance_frame,
                                    text="Finance Calculator",
                                    font=("Arial", "16", "bold"))
       self.finance_heading.grid(row=0)

       #Intructions
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

       # Create tabs
       self.loan_tab = self.create_loan_tab()
       self.mortgage_tab = self.create_mortgage_tab()
       self.investment_tab = self.create_investment_tab()
       self.retirement_tab = self.create_retirement_tab()
       self.budget_tab = self.create_budget_tab()

       # Add tabs to notebook
       self.notebook.add(self.loan_tab, text="Loan Calculator")
       self.notebook.add(self.mortgage_tab, text="Mortgage Calculator")
       self.notebook.add(self.investment_tab, text="Investment Projector")
       self.notebook.add(self.retirement_tab, text="Retirement Planner")
       self.notebook.add(self.budget_tab, text="Budget Allocator")


       self.finance_entry = Entry(self.finance_frame,
                              font=("Arial", "14"))
       self.finance_entry.grid(row=6, padx=10, pady=10)

       error = "Please enter a number"
       self.finance_error = Label(self.finance_frame, text=error, fg="#004C99",
                                 font=("Arial", "14", "bold"))
       self.finance_error.grid(row=3)

       # Conversion, help and history/export buttons
       self.button_frame = Frame(self.finance_frame)
       self.button_frame.grid(row=4)

       button_details_list = [
           ["To Calculate", "#990099", "", 0, 0],
           [" ?? ", "#009900", "", 0, 1],
           ["i", "#CC6600", "", 1, 0],
           ["History / Export", "#004C99", "", 1, 1]
       ]

       # List to hold buttons once they have been made
       self.button_ref_list = []

       for item in button_details_list:
           self.make_button = Button(self.button_frame,
                                     text=item[0], bg=item[1],
                                     fg="#FFFFFF", font=("Arial", "12", "bold"),
                                     width=12, command=item[2])
           self.make_button.grid(row=item[3], column=item[4], padx=5, pady=5)
           self.button_ref_list.append(self.make_button)

       # Retrieve 'history / export' button and disable it at the start
       self.to_history_button = self.button_ref_list[3].config(state=DISABLED)

       def to_help(self):
           """
           Open help dialogue box and display help button
           (so that users can't create multiple help boxes).
           As a (i)
           """
           DisplayHelp(self)

class DisplayHelp:

    # setup dialogeu box and background colour
    def __init__(self, partner):
        background = "#ffe6cc"
        self.help_box = Toplevel()

        partner.to_help_button.config(state=DISABLED)

        #If users press cross at top, closes help and release help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help,partner))

        self.help_frame = Frame(self.help_box, width=300,height=200)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame, text="Info for '' ",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = """                       Welcome to the Finance Calculator!

        This application provides five specialized financial tools:

        1. Loan Calculator:
        - Calculate loan payments, interest costs, and amortization schedules
        - Enter loan amount, interest rate, and term
        - View detailed repayment breakdown

        2. Mortgage Calculator:
        - Estimate monthly mortgage payments
        - Compare different loan terms and rates
        - See principal vs interest breakdown

        3. Investment Projector:
        - Forecast investment growth over time
        - Compare different contribution strategies
        - Visualize compound interest effects

        4. Retirement Planner:
        - Estimate retirement savings needs
        - Project savings growth until retirement
        - Calculate sustainable withdrawal rates

        5. Budget Allocator:
        - Create and analyze personal budgets
        - Track income vs expenses
        - Identify savings opportunities

        General Usage:
        - Select the desired calculator tab
        - Enter all required values in the input fields
        - Press 'Calculate' to see results
        - Use 'History/Export' to save your calculations

        Note: All calculations are estimates only. For professional 
        financial advice, please consult a qualified advisor."""

        self.help_text_label = Label(self.help_frame, text=help_text, wraplength=550,
                                        justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                    font=  ("Arial", "12", "bold"),
                                    text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        recolour_list = [self.help_frame, self.help_heading_label,
                         self.help_text_label]
        for item in recolour_list:
            item.config(bg=background)

    def close_help(self, partner):
        self.help_box.destroy()
        """
        Close help dialogue box and reenable help button.
        """
        #put help button to normal
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()



# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Finance Calculator")
    FinanceCalculator()
    root.mainloop()