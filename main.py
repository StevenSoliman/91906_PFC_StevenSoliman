from tkinter import *
from flask import Flask

class FinanceCalculator():
   """
   Personal Finance Calculator with multiple
    financial tools
   """

   def __init__(self):
       """
       Finance Calculator GUI
       """

       self.finance_frame = Frame(padx=40, pady=40)
       self.finance_frame.grid()

       self.finance_heading = Label(self.finance_frame,
                                    text="Finance Calculator",
                                    font=("Arial", "16", "bold"))
       self.finance_heading.grid(row=0)

       instructions = ("Please select a calculator type from the dropdown menu below "
                       "and a currency from the dropdown beside it. Enter the required value "
                       "in the field below, then press 'Calculate' to see your results.")
       self.finance_instructions = Label(self.finance_frame,
                                         text=instructions,
                                         wraplength=250, width=40,
                                         justify="left")
       self.finance_instructions.grid(row=1)

       self.finance_entry = Entry(self.finance_frame,
                              font=("Arial", "14"))
       self.finance_entry.grid(row=2, padx=10, pady=10)

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

        self.help_heading_label = Label(self.help_frame, text="Help / Info",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "To use this program simply enter a temperature  " \
                     "you wish to convert and then press the button " \
                     "to either convert from Celsius (centigrade) or Fahrenheit. \n\n" \
                     "Note that -273 degree C" \
                     "is the absolute zero and -459.67 degree F is the (coldest temperature as possible)." \
                    "If you try to convert temperatures below this limit you will receive an error. \n\n" \
                    "To see your calculation history and export it to a text file, press the 'History / Export' button."

        self.help_text_label = Label(self.help_frame, text=help_text, wraplength=350,
                                        justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                    font=  ("Arial", "12", "bold"),
                                    text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        recolour_list = [self.help_frame, self.help_heading_label, self.help_text_label, self.dismiss_button]
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