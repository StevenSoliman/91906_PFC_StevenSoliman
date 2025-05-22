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
           ["Help/Info", "#CC6600", "", 1, 0],
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
       self.to_history_button = self.button_ref_list[1].config(state=DISABLED)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Finance Calculator")
    FinanceCalculator()
    root.mainloop()