from tkinter import *
from functools import partial


class FinanceCalculator:
    """
    Personal Finance Calculator with multiple financial tools
    """

    def __init__(self):
        """
        Finance Calculator GUI
        """
        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        # Create a canvas for the circular button
        self.button_canvas = Canvas(self.temp_frame, width=30, height=30,
                                    highlightthickness=0, bd=0)
        self.button_canvas.grid(row=1, padx=5, pady=5)

        # Draw the circular button
        self.circle = self.button_canvas.create_oval(5, 5, 25, 25,
                                                     fill="#000000",
                                                     outline="#000000")

        # Add the "i" text
        self.button_text = self.button_canvas.create_text(15, 15,
                                                          text="i",
                                                          fill="#ffffff",
                                                          font=("Arial", "14", "bold"))

        # Bind click event to the canvas
        self.button_canvas.bind("<Button-1>", lambda e: self.to_help())

        # Store the button state
        self.button_state = NORMAL

    def to_help(self):
        """
        Open help dialogue box if button is enabled
        """
        if self.button_state == NORMAL:
            DisplayHelp(self)

    def set_button_state(self, state):
        """Set the state of the circular button"""
        self.button_state = state
        if state == NORMAL:
            self.button_canvas.itemconfig(self.circle, fill="#000000")
        else:
            self.button_canvas.itemconfig(self.circle, fill="#808080")


class DisplayHelp:
    def __init__(self, partner):
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # Disable the circular button
        partner.set_button_state(DISABLED)

        # If users press cross at top, closes help and release help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300, height=200)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame, text="Help",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "This is the help text for your finance calculator."

        self.help_text_label = Label(self.help_frame, text=help_text,
                                     wraplength=350, justify="left")
        self.help_text_label.grid(row=1, padx=100)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        recolour_list = [self.help_frame, self.help_heading_label,
                         self.help_text_label, self.dismiss_button]
        for item in recolour_list:
            item.config(bg=background)

    def close_help(self, partner):
        """Close help dialogue box and re-enable help button."""
        partner.set_button_state(NORMAL)
        self.help_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Finance Calculator")
    FinanceCalculator()
    root.mainloop()