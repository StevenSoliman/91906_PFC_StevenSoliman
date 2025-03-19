from tkinter import *

class Converter():
   """
   Personal Finance Calculator with multiple
    financial tools
   """


   def __init__(self):
       """
       Finance Calculator GUI
       """
       self.all_calculations_list = []


       self.finance_frame = Frame(padx=10, pady=10)
       self.finance_frame.grid()


       self.finance_heading = Label(self.finance_frame,
                                    text="Personal Finance Calculator",
                                    font=("Arial", "16", "bold"))
       self.finance_heading.grid(row=0)


       instructions = ("Please select a calculator type from the "
                       "dropdown menu above *&TK, "
                       "and a currency from the dropdown beside "
                       "enter the *&TK in the fields below, "
                       "then press 'Calculate' to see your results.")
       self.finance_instructions = Label(self.finance_frame,
                                      text=instructions,
                                      wraplength=250, width=40,
                                      justify="left")
       self.finance_instructions.grid(row=1)


       self.fin_entry = Entry(self.finance_frame,
                               font=("Arial", "14"))
       self.fin_entry.grid(row=2, padx=10, pady=10)

       error = "Please enter a number"
       self.answer_error = Label(self.finance_frame, text=error, fg="#004C99",
                                 font=("Arial", "14", "bold"))
       self.answer_error.grid(row=3)

       # Conversion, help and history/export buttons
       self.button_frame = Frame(self.finance_frame)
       self.button_frame.grid(row=4)

       button_details_list = [
           ["Calculate", "#990099", "", 0, 0],
           [" ?? ", "#009900", "", 0, 1],
           ["Help / Info", "#CC6600", "", 1, 0],
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
           self.to_history_button = (self.button_ref_list[3])
           self.to_history_button.config(state=DISABLED)

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Finance Calculator")
    Converter()
    root.mainloop()