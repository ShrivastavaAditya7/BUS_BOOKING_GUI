import tkinter as tk
import tkinter.ttk as ttk
import _tkinter
import sqlite3
from tkinter import messagebox
from typing import Callable


class BusScreen:
    def create_screen(
        self, root: tk.Tk, back_screen: Callable, database_manager: object = None
    ) -> None:
        self.database_manager = database_manager
        self.back_screen = back_screen
        self.root = root
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Online Bus Booking System | Admin | Add Bus Details")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.config(bg="light green")
        frame = tk.Frame(self.root, bg="light green")
        logo = tk.PhotoImage(file="logo0.png")
        label = tk.Label(self.root, image=logo, bg="light green")
        label.grid(row=0, column=0, padx=250, pady=10)
        title = tk.Label(
            self.root,
            text="Online Bus Booking System",
            font=("Arial", 30, "bold"),
            bg="green",
        )
        title.grid(row=1, column=0)
        sub_title = tk.Label(
            self.root,
            text="Add Bus Details",
            font=("Arial", 20, "bold"),
            bg="darkolivegreen2",
        )
        sub_title.grid(row=2, column=0, pady=10)

        self.bus_id = tk.IntVar()
        bus_id_label = tk.Label(
            frame, text="Bus ID: ", font=("Arial", 11, "bold"), bg="light green"
        )
        bus_id_entry = tk.Entry(frame, textvariable=self.bus_id)
        bus_id_label.grid(row=0, column=0, padx=5, pady=5)
        bus_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # listbox widget for bus types

        self.bus_type = tk.StringVar()
        bus_type_label = tk.Label(
            frame, text="Bus Type: ", font=("Arial", 11, "bold"), bg="light green"
        )
        bus_type_combobox = ttk.Combobox(
            frame, state="readonly", textvariable=self.bus_type
        )
        bus_type_combobox["values"] = (
            "AC 2x2",
            "AC 3x2",
            "Non-AC 2x2",
            "Non-AC 3x2",
            "AC Sleeper 2x1",
            "Non-AC Sleeper 2x1",
        )
        bus_type_label.grid(row=0, column=2, padx=5, pady=5)
        bus_type_combobox.grid(row=0, column=3, padx=5, pady=5)

        self.bus_capacity = tk.IntVar()
        bus_capacity_label = tk.Label(
            frame, text="Bus Capacity: ", font=("Arial", 11, "bold"), bg="light green"
        )
        bus_capacity_entry = tk.Entry(frame, textvariable=self.bus_capacity)
        bus_capacity_label.grid(row=0, column=4, padx=5, pady=5)
        bus_capacity_entry.grid(row=0, column=5, padx=5, pady=5)

        self.bus_fare = tk.DoubleVar()
        bus_fare_label = tk.Label(
            frame,
            text="Bus Fare: ",
            font=("Arial", 11, "bold"),
            bg="light green",
        )
        bus_fare_entry = tk.Entry(frame, textvariable=self.bus_fare)
        bus_fare_label.grid(row=1, column=0, padx=5, pady=5)
        bus_fare_entry.grid(row=1, column=1, padx=5, pady=5)

        self.operator_id = tk.IntVar()
        operator_id_label = tk.Label(
            frame, text="Operator ID: ", font=("Arial", 11, "bold"), bg="light green"
        )
        operator_id_entry = tk.Entry(frame, textvariable=self.operator_id)
        operator_id_label.grid(row=1, column=2, padx=5, pady=5)
        operator_id_entry.grid(row=1, column=3, padx=5, pady=5)

        self.route_id = tk.IntVar()
        route_id_label = tk.Label(
            frame, text="Route ID: ", font=("Arial", 11, "bold"), bg="light green"
        )
        route_id_entry = tk.Entry(frame, textvariable=self.route_id)
        route_id_label.grid(row=1, column=4, padx=5, pady=5)
        route_id_entry.grid(row=1, column=5, padx=5, pady=5)

        add_bus_but = tk.Button(
            frame,
            text="Add Bus",
            font=("Arial", 11, "bold"),
            bg="green",
            fg="white",
            command=self.add_details,
        )
        add_bus_but.grid(row=2, column=2, padx=5, pady=5)
        edit_bus_but = tk.Button(
            frame,
            text="Edit Bus",
            font=("Arial", 11, "bold"),
            bg="green",
            fg="white",
            command=lambda: self.add_details(True),
        )
        edit_bus_but.grid(row=2, column=3, padx=5, pady=5)
        back_but = tk.Button(
            frame,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="darkolivegreen",
            fg="white",
            command=lambda: self.back_screen(
                root=self.root, database_manager=self.database_manager
            ),
        )
        back_but.grid(row=3, column=4, pady=60)
        frame.grid(row=3, column=0, pady=50)
        self.editable_frame = tk.Frame(self.root, bg="light green")
        self.info_label = tk.Label(
            self.editable_frame,
            bg="light green",
        )
        self.root.mainloop()

    def add_details(self, edit_bus: bool = False) -> None:
        try:
            self.database_manager.bus_table.add_bus(
                self.bus_id.get(),
                self.bus_type.get(),
                self.bus_capacity.get(),
                self.bus_fare.get(),
                self.operator_id.get(),
                self.route_id.get(),
                edit_bus,
            )
        except _tkinter.TclError:
            messagebox.showerror("Error", "Invalid input")
            return
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Bus and Route ID pair already exists")
            return
        except Exception as e:
            messagebox.showerror("Error", e)
            return
        if edit_bus:
            msg_part = "edited"
        else:
            msg_part = "added"
        messagebox.showinfo("Success", f"Bus details {msg_part} successfully")
        self.info_label.config(
            text=f"{self.bus_id.get()}, {self.bus_type.get()}, {self.bus_capacity.get()},\
                {self.bus_fare.get()}, {self.operator_id.get()}, {self.route_id.get()}",
            font=("Arial", 10, "bold"),
            bg="darkolivegreen3",
        )
        self.info_label.grid(row=0, column=0)
        self.editable_frame.grid(row=3, column=0, pady=30)


if __name__ == "__main__":
    root = tk.Tk()
    app = BusScreen()
    app.create_screen(root, app.create_screen)
