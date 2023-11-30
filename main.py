import tkinter as tk
from admin_screens import admin
from database import database_manager
from user_screens import booking_screen
from user_screens import booking_check_screen


class Application:
    def __init__(self) -> None:
        self.root = None
        self.admin_screen = admin.ApplicationAdmin()
        self.booking_screen = booking_screen.BookingScreen()
        self.booking_check_screen = booking_check_screen.BookingCheckScreen()
        self.database_manager = database_manager.DatabaseManager("bus.db")

    def splash_screen(self) -> None:
        self.root = tk.Tk()
        self.root.title("Online Bus Booking System")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.config(bg="light green")
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
        name = tk.Label(
            self.root, text="Name: Aditya Shrivastava", font=("Arial", 15), bg="light green"
        )
        name.grid(row=2, column=0, pady=5)
        eno = tk.Label(
            self.root,
            text="Mobile no: +91 7828716912",
            font=("Arial", 15),
            bg="light green",
        )
        eno.grid(row=3, column=0)
        mobile = tk.Label(
            self.root, text="Btech cse Student", font=("Arial", 15), bg="light green"
        )
        mobile.grid(row=4, column=0)
        footer = tk.Label(
            self.root,
            text="Project using Tkinter in python",
            font=("Arial", 20, "bold"),
            bg="green",
        )
        footer.grid(row=5, column=0, pady=70)
        name = tk.Label(
            self.root,
            text="Project Based Learning",
            font=("Arial", 18),
            bg="light green",
        )
        name.grid(row=6, column=0, pady=5)
        self.root.after(3000, self.home_screen)
        self.root.mainloop()

    def home_screen(self, caller_root: tk.Tk = None) -> None:
        if caller_root:
            caller_root.destroy()
        else:
            self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Online Bus Booking System | Home")
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
        book_but = tk.Button(
            frame,
            text="Book Ticket",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=lambda: self.booking_screen.create_screen(
                self.root, self.home_screen, self.database_manager
            ),
        )
        book_but.grid(row=0, column=0, padx=5)
        check_but = tk.Button(
            frame,
            text="Check Ticket",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=lambda: self.booking_check_screen.create_screen(
                self.root, self.home_screen, self.database_manager
            ),
        )
        check_but.grid(row=0, column=1, padx=5)
        add_but = tk.Button(
            frame,
            text="Add Bus",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=lambda: self.admin_screen.create_admin_screen(
                self.root, self.home_screen, self.database_manager
            ),
        )
        add_but.grid(row=0, column=2, padx=5)
        info_label = tk.Label(
            frame,
            text="For Admin Only",
            font=("Arial", 10, "bold"),
            bg="darkolivegreen3",
        )
        info_label.grid(row=1, column=2, pady=5)
        frame.grid(row=2, column=0, pady=100)
        self.root.mainloop()


if __name__ == "__main__":
    app = Application()
    app.splash_screen()
    # app.home_screen()
    # app.admin_screen()
