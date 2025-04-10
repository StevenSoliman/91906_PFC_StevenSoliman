from tkinter import *
from functools import partial


class CircleButton(Canvas):
    """A circular button widget that matches your style"""

    def __init__(self, parent, text, command, diameter=30, bg="#CC6600", fg="#FFFFFF"):
        super().__init__(parent, width=diameter, height=diameter,
                         highlightthickness=0, bd=0, cursor="hand2")
        self.command = command
        self.bg = bg
        self.fg = fg
        self.disabled_color = "#999999"
        self.state = NORMAL

        # Draw circle with padding
        padding = 2
        self.circle = self.create_oval(
            padding, padding, diameter - padding, diameter - padding,
            fill=bg, outline=bg
        )

        # Add centered text
        self.text = self.create_text(
            diameter // 2, diameter // 2,
            text=text, fill=fg,
            font=("Arial", "14", "bold")
        )

        self.bind("<Button-1>", self._on_click)

    def _on_click(self, event):
        if self.state == NORMAL:
            self.command()

    def config(self, state=None):
        if state is not None:
            self.state = state
            color = self.disabled_color if state == DISABLED else self.bg
            self.itemconfig(self.circle, fill=color)


class FinanceCalculator:
    def __init__(self):
        self.temp_frame = Frame(padx=50, pady=50)
        self.temp_frame.grid()

        # Replace Button with CircleButton
        self.to_help_button = CircleButton(
            self.temp_frame,
            text="i",
            command=self.to_help,
            bg="#CC6600",
            fg="#FFFFFF"
        )
        self.to_help_button.grid(row=1, padx=5, pady=5)

    def to_help(self):
        DisplayHelp(self)


class DisplayHelp:
    def __init__(self, partner):
        background = "#ffe6cc"
        self.help_box = Toplevel()
        partner.to_help_button.config(state=DISABLED)

        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300, height=200, bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame, text="I",
                                        font=("Arial", "14", "bold"), bg=background)
        self.help_heading_label.grid(row=0)

        help_text = "Your help text goes here"
        self.help_text_label = Label(self.help_frame, text=help_text,
                                     wraplength=350, justify="left", bg=background)
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    def close_help(self, partner):
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Finance Calculator")
    FinanceCalculator()
    root.mainloop()