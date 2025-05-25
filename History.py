from tkinter import *
from functools import partial
import calculation_finance as m
from datetime import date


class Converter:
    """
    Temperature conversion tool (°C to °F or °F to °C)
    """

    def __init__(self):
        """
        Temperature converter GUI
        """

        self.all_calculations_list = [
            '10.0 °F is -12°C', '20.0 °F is -7°C',
            '30.0 °F is -1°C', '40.0 °F is 4°C',
            '50.0 °F is 10°C', 'this is a test'
        ]

        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.to_history_button = Button(
            self.temp_frame,
            text="History / Export",
            bg="#CC6600",
            fg="#FFFFFF",
            font=("Arial", 14, "bold"),
            width=12,
            command=self.to_history
        )
        self.to_history_button.grid(row=1, padx=5, pady=5)

    def to_history(self):
        """
        Open history dialog box and disable history button
        """
        HistoryExport(self, self.all_calculations_list)


class HistoryExport:
    """
    Displays history dialog box and export button
    """

    def __init__(self, partner, calculations):
        self.history_box = Toplevel()
        partner.to_history_button.config(state=DISABLED)

        self.history_box.protocol('WM_DELETE_WINDOW', partial(self.close_history, partner))

        self.history_frame = Frame(self.history_box)
        self.history_frame.grid()

        calc_back = "#D5E8D4" if len(calculations) <= c.MAX_CALCS else "#ffe6cc"
        calc_amount = "all your" if len(
            calculations) <= c.MAX_CALCS else f"your recent calculations - showing {c.MAX_CALCS} / {len(calculations)}"

        recent_intro_txt = f"Below are {calc_amount} calculations (to the nearest degree)"

        newest_first_list = list(reversed(calculations))
        newest_first_string = "\n".join(newest_first_list[:c.MAX_CALCS])

        export_instruction_txt = (
            "Please push <Export> to save your calculations in a file. "
            "If the filename already exists, it will be overwritten."
        )

        history_labels_list = [
            ["History / Export", ("Arial", 16, "bold"), None],
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
        today = date.today()

        # Get day, month and year as individual string
        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")

        file_name = f"temperature_{year}_{month}_{day}"

        success_string = ("Export successful. The file is called" 
                          f" {file_name}.txt")
        self.export_filename_label.config(fg="#009900", text=success_string ,
                                          font=("Arial", "12", "bold"))

        write_to = f"{file_name}.txt"

        with open(write_to, "w") as text_file:
            text_file.write("***** Temperature Calculations *****\n")
            text_file.write(f"Generated: {day}/{month}/{year}\n\n")
            text_file.write("Here is your calculation history (oldest to newest)...\n")

            # write the item to file
            for item in calculations:
                text_file.write(item)
                text_file.write("\n")

    def close_history(self, partner):
        partner.to_history_button.config(state=NORMAL)
        self.history_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
