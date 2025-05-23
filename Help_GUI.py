from tkinter import *
from functools import partial

class FinanceCalculator:
    """
    Temperature conversion tool (°C to °F or °F to °C)
    """

    def __init__(self):
        """
        Temperature converter GUI
        """

        self.temp_frame = Frame(padx=50, pady=50)
        self.temp_frame.grid()

        self.to_help_button = Button(self.temp_frame,
                                     text="Help/Info",
                                     bg="#CC6600",
                                     fg="#ffffff",
                                     font=("Arial", "14", "bold"), width=12,
                                     command=self.to_help)
        self.to_help_button.grid(row=1, padx=5, pady=5)


    def to_help(self):
        """
        Open help dialogue box and display help button
        (so that users can't create multiple help box).
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

        self.help_heading_label = Label(self.help_frame, text="I",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = ""

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



# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Finance Calculator")
    FinanceCalculator()
    root.mainloop()
