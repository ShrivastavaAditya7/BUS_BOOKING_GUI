import tkinter as tk
import _tkinter
import sqlite3
from tkinter import messagebox
from typing import Callable


class RunningScreen:
    def create_screen(
        self, root: tk.Tk, back_screen: Callable, database_manager: object = None
    ) -> None:
        self.database_manager = database_manager
        self.back_screen = back_screen
        self.root = root
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Online Bus Booking System | Admin | Add Bus Running Details")
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
            text="Add Bus Running Details",
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

        self.running_date = tk.StringVar()
        running_date_label = tk.Label(
            frame,
            text="Running Date (YYYY-MM-DD): ",
            font=("Arial", 11, "bold"),
            bg="light green",
        )
        running_date_entry = tk.Entry(frame, textvariable=self.running_date)
        running_date_label.grid(row=0, column=2, padx=5, pady=5)
        running_date_entry.grid(row=0, column=3, padx=5, pady=5)

        self.seat_available = tk.IntVar()
        seat_available_label = tk.Label(
            frame,
            text="Seat Available: ",
            font=("Arial", 11, "bold"),
            bg="light green",
        )
        seat_available_entry = tk.Entry(frame, textvariable=self.seat_available)
        seat_available_label.grid(row=0, column=4, padx=5, pady=5)
        seat_available_entry.grid(row=0, column=5, padx=5, pady=5)

        # self.operator_phone = tk.StringVar()
        # operator_phone_label = tk.Label(
        #     frame, text="Operator Phone: ", font=("Arial", 11, "bold"), bg="light green"
        # )
        # operator_phone_entry = tk.Entry(frame, textvariable=self.operator_phone)
        # operator_phone_label.grid(row=1, column=1, padx=5, pady=5)
        # operator_phone_entry.grid(row=1, column=2, padx=5, pady=5)

        # self.operator_email = tk.StringVar()
        # operator_email_label = tk.Label(
        #     frame, text="Operator Email: ", font=("Arial", 11, "bold"), bg="light green"
        # )
        # operator_email_entry = tk.Entry(frame, textvariable=self.operator_email)
        # operator_email_label.grid(row=1, column=3, padx=5, pady=5)
        # operator_email_entry.grid(row=1, column=4, padx=5, pady=5)

        add_running_but = tk.Button(
            frame,
            text="Add Running Details",
            font=("Arial", 11, "bold"),
            bg="green",
            fg="white",
            command=self.add_details,
        )
        add_running_but.grid(row=2, column=2, padx=5, pady=5)
        del_route_but = tk.Button(
            frame,
            text="Delete Running Details",
            font=("Arial", 11, "bold"),
            bg="green",
            fg="white",
            command=self.delete_details,
        )
        del_route_but.grid(row=2, column=3, padx=5, pady=5)
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

    def add_details(self) -> None:
        try:
            self.database_manager.running_table.add_running(
                self.bus_id.get(),
                self.running_date.get(),
                self.seat_available.get(),
            )
        except _tkinter.TclError:
            messagebox.showerror(
                "Error", "BUS ID and Seat Available can only be of integer type"
            )
            return
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error", "BUS ID and Running Date combination must be unique"
            )
            return
        except Exception as e:
            messagebox.showerror("Error", e)
            return
        messagebox.showinfo("Success", "Running Details Added Successfully")
        self.info_label.config(
            text=f"{self.bus_id.get()},{self.running_date.get()},\
    {self.seat_available.get()}",
            font=("Arial", 10, "bold"),
            bg="darkolivegreen3",
        )
        self.info_label.grid(row=0, column=0)
        self.editable_frame.grid(row=3, column=0, pady=30)

    def delete_details(self) -> None:
        try:
            self.database_manager.running_table.delete_running(
                self.bus_id.get(), self.running_date.get()
            )
        except _tkinter.TclError:
            messagebox.showerror("Error", "Route ID or Running Date is invalid")
            return
        except Exception as e:
            messagebox.showerror("Error", e)
            return
        messagebox.showinfo("Success", "Running Details Deleted Successfully")


if __name__ == "__main__":
    root = tk.Tk()
    app = RunningScreen()
    app.create_screen(root, app.create_screen)
