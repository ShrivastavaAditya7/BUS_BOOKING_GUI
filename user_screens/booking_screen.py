import tkinter as tk
import tkinter.ttk as ttk
import _tkinter
import sqlite3
import re
from tkinter import messagebox
from typing import Callable
import datetime


class BookingScreen:
    def create_screen(
        self, root: tk.Tk, back_screen: Callable, database_manager: object = None
    ) -> None:
        self.database_manager = database_manager
        self.back_screen = back_screen
        self.root = root
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Online Bus Booking System | Book Ticket")
        window_height = tk.Tk.winfo_screenheight(self.root)
        self.root.geometry(f"900x{window_height - 100}")
        self.root.resizable(False, False)
        self.root.config(bg="light green")
        frame = tk.Frame(self.root, bg="light green")
        logo = tk.PhotoImage(file="logo0.png")
        label = tk.Label(self.root, image=logo, bg="light green")
        label.grid(row=0, column=0, padx=250, pady=5)
        title = tk.Label(
            self.root,
            text="Online Bus Booking System",
            font=("Arial", 30, "bold"),
            bg="green",
        )
        title.grid(row=1, column=0)
        sub_title = tk.Label(
            self.root,
            text="Enter Journey Details",
            font=("Arial", 15, "bold"),
            bg="darkolivegreen2",
        )
        sub_title.grid(row=2, column=0, pady=5)

        self.to_place = tk.StringVar()
        to_place_label = tk.Label(
            frame, text="To: ", font=("Arial", 11, "bold"), bg="light green"
        )
        to_place_entry = tk.Entry(frame, textvariable=self.to_place)
        to_place_label.grid(row=0, column=0, padx=5, pady=5)
        to_place_entry.grid(row=0, column=1, padx=5, pady=5)

        self.from_place = tk.StringVar()
        from_place_label = tk.Label(
            frame, text="From: ", font=("Arial", 11, "bold"), bg="light green"
        )
        from_place_entry = tk.Entry(frame, textvariable=self.from_place)
        from_place_label.grid(row=0, column=2, padx=5, pady=5)
        from_place_entry.grid(row=0, column=3, padx=5, pady=5)

        self.journey_date = tk.StringVar()
        journey_date_label = tk.Label(
            frame,
            text="Journey Date\n(YYYY-MM-DD): ",
            font=("Arial", 11, "bold"),
            bg="light green",
        )
        journey_date_entry = tk.Entry(frame, textvariable=self.journey_date)
        journey_date_label.grid(row=0, column=4, padx=5, pady=5)
        journey_date_entry.grid(row=0, column=5, padx=5, pady=5)

        show_bus = tk.Button(
            frame,
            text="Show Bus",
            font=("Arial", 11, "bold"),
            bg="green",
            fg="white",
            command=self.show_bus,
        )
        show_bus.grid(row=0, column=6, padx=5, pady=5)

        back_but = tk.Button(
            frame,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="darkolivegreen",
            fg="white",
            command=lambda: self.back_screen(self.root),
        )
        back_but.grid(row=0, column=7, padx=15, pady=5)
        frame.grid(row=3, column=0, pady=30)
        self.root.mainloop()

    def show_bus(self):
        try:
            from_place = self.from_place.get().title()
            to_place = self.to_place.get().title()
            if from_place == to_place:
                raise Exception("From and To places cannot be same")
            journey_date = self.journey_date.get()
            if not re.search(re.compile("^\d{4}-\d{2}-\d{2}$"), journey_date):
                raise Exception("Invalid date format (YYYY-MM-DD))")
        except _tkinter.TclError:
            messagebox.showerror("Error", "Invalid input")
            return
        except Exception as e:
            messagebox.showerror("Error", e)
            return
        if not from_place or not to_place or not journey_date:
            messagebox.showerror("Error", "Please fill all the fields")
            return
        try:
            buses = self.database_manager.get_buses(from_place, to_place, journey_date)
        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please fill all the fields correctly")
            return
        if not buses:
            messagebox.showerror("Error", "No buses found")
            return
        try:
            self.editable_frame.destroy()
            self.editable_frame1.destroy()
        except Exception:
            pass
        self.editable_frame = tk.Frame(self.root, bg="light green")
        self.editable_frame.grid(row=4, column=0)
        listbox = tk.Listbox(
            self.editable_frame, width=50, height=5, font=("Arial", 12)
        )
        listbox.grid(row=0, column=0)
        for i, bus in enumerate(buses, start=1):
            listbox.insert(i, "    ".join(list(map(str, [j for j in bus]))))
        listbox.bind("<<ListboxSelect>>", self.select_bus)

    def book_bus(self):
        try:
            self.database_manager.booking_table.add_passanger(
                self.passanger_name.get(),
                self.gender.get(),
                self.seat_count.get(),
                self.mobile_no.get(),
                self.age.get(),
                self.operator_name,
                self.from_place.get().title(),
                self.to_place.get().title(),
                self.fare,
                self.journey_date.get(),
                self.availability,
            )
        except _tkinter.TclError:
            messagebox.showerror("Error", "Invalid input")
            return
        except Exception as e:
            messagebox.showerror("Error", e)
            return
        messagebox.showinfo(
            "Your Ticket",
            f"PASSENGER NAME: {self.passanger_name.get()}\n\
        PASSANGER GENDER: {self.gender.get()}\n\
        SEAT COUNT: {self.seat_count.get()}\n\
        PASSANGER MOBILE NUMBER: {self.mobile_no.get()}\n\
        PASSANGER AGE: {self.age.get()}\n\
        OPERATOR NAME: {self.operator_name}\n\
        SOURCE: {self.from_place.get().title()}\n\
        DESTINATION: {self.to_place.get().title()}\n\
        BUS FARE: Rs. {self.fare}\n\
        RUNNING DATE: {self.journey_date.get()}\n\
        BOOKING DATE: {datetime.datetime.now().strftime('%Y-%m-%d')}",
        )

    def select_bus(self, event):
        self.editable_frame1 = tk.Frame(self.root, bg="light green")
        self.editable_frame1.grid(row=5, column=0)
        widget = event.widget
        selection = widget.curselection()
        if not selection:
            return
        index = selection[0]
        data = widget.get(index)
        data = data.split("    ")
        self.operator_name = data[0]
        self.bus_type = data[1]
        self.availability = data[2].split("/")[0]
        self.fare = data[3]
        self.info_label = tk.Label(
            self.editable_frame,
            text="Fill Passanger Details",
            font=("Arial", 15, "bold"),
            bg="darkolivegreen2",
        )
        self.info_label.grid(row=1, column=0, pady=5)

        self.passanger_name = tk.StringVar()
        passanger_name_label = tk.Label(
            self.editable_frame1,
            text="Name: ",
            font=("Arial", 11, "bold"),
            bg="light green",
        )
        passanger_name_entry = tk.Entry(
            self.editable_frame1, textvariable=self.passanger_name
        )
        passanger_name_label.grid(row=0, column=0, padx=5, pady=5)
        passanger_name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.gender = tk.StringVar()
        gender_label = tk.Label(
            self.editable_frame1,
            text="Gender: ",
            font=("Arial", 11, "bold"),
            bg="light green",
        )
        gender_combobox = ttk.Combobox(
            self.editable_frame1, state="readonly", textvariable=self.gender
        )
        gender_combobox["values"] = ["Male", "Female", "Third Gender"]
        gender_label.grid(row=0, column=2, padx=5, pady=5)
        gender_combobox.grid(row=0, column=3, padx=5, pady=5)

        self.seat_count = tk.IntVar()
        seat_count_label = tk.Label(
            self.editable_frame1,
            text="Seat Count: ",
            font=("Arial", 11, "bold"),
            bg="light green",
        )
        seat_count_entry = tk.Entry(self.editable_frame1, textvariable=self.seat_count)
        seat_count_label.grid(row=0, column=4, padx=5, pady=5)
        seat_count_entry.grid(row=0, column=5, padx=5, pady=5)

        self.mobile_no = tk.StringVar()
        mobile_no_label = tk.Label(
            self.editable_frame1,
            text="Mobile No: ",
            font=("Arial", 11, "bold"),
            bg="light green",
        )
        mobile_no_entry = tk.Entry(self.editable_frame1, textvariable=self.mobile_no)
        mobile_no_label.grid(row=1, column=2, padx=5, pady=5)
        mobile_no_entry.grid(row=1, column=3, padx=5, pady=5)

        self.age = tk.IntVar()
        age_label = tk.Label(
            self.editable_frame1,
            text="Age: ",
            font=("Arial", 11, "bold"),
            bg="light green",
        )
        age_entry = tk.Entry(self.editable_frame1, textvariable=self.age)
        age_label.grid(row=1, column=4, padx=5, pady=5)
        age_entry.grid(row=1, column=5, padx=5, pady=5)

        book_but = tk.Button(
            self.editable_frame1,
            text="Book",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=self.book_bus,
        )
        book_but.grid(row=2, column=3, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = BookingScreen()
    app.create_screen(root, app.create_screen)
