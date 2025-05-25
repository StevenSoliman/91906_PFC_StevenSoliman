from tkinter import *
from functools import partial
import all_constants as c
from datetime import date

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
        calc_amount = "all your" if len(calculations) <= c.MAX_FINANCE_CALCS else f"your recent calculations - showing {c.MAX_FINANCE_CALCS} / {len(calculations)}"

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
            [newest_first_string, ("Arial", 14), calc_back],
            [export_instruction_txt, ("Arial", 11), None],
        ]

        history_labels_ref = []
        for count, item in enumerate(history_labels_list):
            make_label = Label(
                self.history_frame, text=item[0], font=item[1],
                bg=item[2], wraplength=300, justify="left", padx=20, pady=10
            )
            make_label.grid(row=count)
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

        success_string = f"Export successful. The file is called {file_name}.txt"
        self.export_filename_label.config(fg="#009900", text=success_string,
                                          font=("Arial", "12", "bold"))

        write_to = f"{file_name}.txt"

        with open(write_to, "w") as text_file:
            text_file.write("***** Personal Finance Calculations *****\n")
            text_file.write(f"Generated: {day}/{month}/{year}\n\n")
            text_file.write("Here is your calculation history (oldest to newest)...\n")

            # Write calculations in chronological order (oldest first)
            for item in calculations:
                text_file.write(item)
                text_file.write("\n")

    def close_history(self, partner):
        """Close history dialog and re-enable history button"""
        partner.button_ref_list[1].config(state=NORMAL)
        self.history_box.destroy()