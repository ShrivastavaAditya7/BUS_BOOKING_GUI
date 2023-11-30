import tkinter as tk
from .screens.operator_screen import OperatorScreen
from .screens.route_screen import RouteScreen
from .screens.bus_screen import BusScreen
from .screens.running_screen import RunningScreen
from typing import Callable


class ApplicationAdmin:
    def __init__(self):
        self.operator_screen = OperatorScreen()
        self.route_screen = RouteScreen()
        self.bus_screen = BusScreen()
        self.running_screen = RunningScreen()

    def create_admin_screen(
        self, root: tk.Tk, back_screen: Callable = None, database_manager: object = None
    ) -> None:
        self.root = root
        if back_screen:
            self.back_screen = back_screen
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Online Bus Booking System | Admin")
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
            text="Add New Details to Database",
            font=("Arial", 20, "bold"),
            bg="darkolivegreen2",
        )
        sub_title.grid(row=2, column=0, pady=10)
        new_operator_but = tk.Button(
            frame,
            text="New Operator",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=lambda: self.operator_screen.create_screen(
                self.root, self.create_admin_screen, database_manager
            ),
        )
        new_operator_but.grid(row=0, column=0, padx=5)
        new_bus_but = tk.Button(
            frame,
            text="New Bus",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=lambda: self.bus_screen.create_screen(
                self.root, self.create_admin_screen, database_manager
            ),
        )
        new_bus_but.grid(row=0, column=1, padx=5)
        new_route_but = tk.Button(
            frame,
            text="New Route",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=lambda: self.route_screen.create_screen(
                self.root, self.create_admin_screen, database_manager
            ),
        )
        new_route_but.grid(row=0, column=2, padx=5)
        new_run_but = tk.Button(
            frame,
            text="New Run",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=lambda: self.running_screen.create_screen(
                self.root, self.create_admin_screen, database_manager
            ),
        )
        new_run_but.grid(row=0, column=3, padx=5)
        back_but = tk.Button(
            frame,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="darkolivegreen",
            fg="white",
            command=lambda: self.back_screen(self.root),
        )
        back_but.grid(row=1, column=3, pady=60)
        frame.grid(row=3, column=0, pady=100)
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationAdmin()
    app.create_admin_screen(root, app.create_admin_screen)
