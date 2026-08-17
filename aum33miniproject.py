import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


# =========================
# DATABASE
# =========================

DB_NAME = "savings.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_database():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT,
            date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            target REAL NOT NULL,
            saved REAL DEFAULT 0,
            deadline TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================
# BUSINESS LOGIC
# =========================

def get_total_income():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'income'
    """)

    result = cursor.fetchone()[0]
    conn.close()

    return result


def get_total_expense():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'expense'
    """)

    result = cursor.fetchone()[0]
    conn.close()

    return result


def get_total_savings():
    return get_total_income() - get_total_expense()


def add_transaction(transaction_type, category, amount, note):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (type, category, amount, note, date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        transaction_type,
        category,
        amount,
        note,
        datetime.now().strftime("%Y-%m-%d")
    ))

    conn.commit()
    conn.close()


def add_goal(name, target, deadline):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO goals
        (name, target, saved, deadline)
        VALUES (?, ?, 0, ?)
    """, (name, target, deadline))

    conn.commit()
    conn.close()


# =========================
# MAIN APPLICATION
# =========================

class SavingsApp:

    def __init__(self, root):
        self.root = root

        self.root.title("Savings System")
        self.root.geometry("1100x700")
        self.root.configure(bg="#0B1F3A")

        self.setup_style()
        self.create_sidebar()
        self.create_content()

        self.show_dashboard()

    # =========================
    # STYLE
    # =========================

    def setup_style(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#102A4C",
            foreground="white",
            fieldbackground="#102A4C",
            rowheight=35
        )

        style.configure(
            "Treeview.Heading",
            background="#1769E0",
            foreground="white",
            font=("Arial", 11, "bold")
        )

    # =========================
    # SIDEBAR
    # =========================

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.root,
            bg="#07182E",
            width=220
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        title = tk.Label(
            self.sidebar,
            text="SAVINGS\nSYSTEM",
            font=("Arial", 20, "bold"),
            fg="#4DA3FF",
            bg="#07182E"
        )

        title.pack(
            pady=35
        )

        buttons = [
            ("🏠  Dashboard", self.show_dashboard),
            ("💰  Transactions", self.show_transactions),
            ("🎯  Goals", self.show_goals),
            ("📊  Analytics", self.show_analytics),
            ("📋  Reports", self.show_reports)
        ]

        for text, command in buttons:

            btn = tk.Button(
                self.sidebar,
                text=text,
                command=command,
                anchor="w",
                font=("Arial", 12),
                fg="white",
                bg="#102A4C",
                activebackground="#1769E0",
                activeforeground="white",
                relief="flat",
                padx=20,
                pady=14,
                cursor="hand2"
            )

            btn.pack(
                fill="x",
                padx=15,
                pady=5
            )

    # =========================
    # CONTENT
    # =========================

    def create_content(self):

        self.content = tk.Frame(
            self.root,
            bg="#EAF4FF"
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # =========================
    # DASHBOARD
    # =========================

    def show_dashboard(self):

        self.clear_content()

        title = tk.Label(
            self.content,
            text="Savings Dashboard",
            font=("Arial", 26, "bold"),
            fg="#0B2A5B",
            bg="#EAF4FF"
        )

        title.pack(
            anchor="w",
            padx=35,
            pady=(30, 20)
        )

        cards = tk.Frame(
            self.content,
            bg="#EAF4FF"
        )

        cards.pack(
            fill="x",
            padx=30
        )

        income = get_total_income()
        expense = get_total_expense()
        savings = get_total_savings()

        self.create_card(
            cards,
            "รายรับทั้งหมด",
            f"฿ {income:,.2f}",
            "#2E86DE"
        ).pack(
            side="left",
            expand=True,
            fill="both",
            padx=8
        )

        self.create_card(
            cards,
            "รายจ่ายทั้งหมด",
            f"฿ {expense:,.2f}",
            "#E74C3C"
        ).pack(
            side="left",
            expand=True,
            fill="both",
            padx=8
        )

        self.create_card(
            cards,
            "เงินออมทั้งหมด",
            f"฿ {savings:,.2f}",
            "#20BF6B"
        ).pack(
            side="left",
            expand=True,
            fill="both",
            padx=8
        )

        # Saving rate

        if income > 0:
            rate = (savings / income) * 100
        else:
            rate = 0

        self.create_card(
            cards,
            "อัตราการออม",
            f"{rate:.1f}%",
            "#8E44AD"
        ).pack(
            side="left",
            expand=True,
            fill="both",
            padx=8
        )

        # Recent transactions

        tk.Label(
            self.content,
            text="รายการล่าสุด",
            font=("Arial", 18, "bold"),
            fg="#0B2A5B",
            bg="#EAF4FF"
        ).pack(
            anchor="w",
            padx=40,
            pady=(40, 10)
        )

        table = ttk.Treeview(
            self.content,
            columns=("type", "category", "amount", "date"),
            show="headings"
        )

        table.heading("type", text="ประเภท")
        table.heading("category", text="หมวดหมู่")
        table.heading("amount", text="จำนวนเงิน")
        table.heading("date", text="วันที่")

        table.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=10
        )

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT type, category, amount, date
            FROM transactions
            ORDER BY id DESC
            LIMIT 10
        """)

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            display_type = (
                "รายรับ"
                if row[0] == "income"
                else "รายจ่าย"
            )

            table.insert(
                "",
                "end",
                values=(
                    display_type,
                    row[1],
                    f"฿ {row[2]:,.2f}",
                    row[3]
                )
            )

    # =========================
    # CARD
    # =========================

    def create_card(self, parent, title, value, color):

        frame = tk.Frame(
            parent,
            bg="white",
            height=130
        )

        tk.Label(
            frame,
            text=title,
            font=("Arial", 11),
            fg="#607D9B",
            bg="white"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        tk.Label(
            frame,
            text=value,
            font=("Arial", 20, "bold"),
            fg=color,
            bg="white"
        ).pack(
            anchor="w",
            padx=20
        )

        return frame

    # =========================
    # TRANSACTIONS
    # =========================

    def show_transactions(self):

        self.clear_content()

        tk.Label(
            self.content,
            text="Income & Expense",
            font=("Arial", 25, "bold"),
            fg="#0B2A5B",
            bg="#EAF4FF"
        ).pack(
            anchor="w",
            padx=35,
            pady=30
        )

        form = tk.Frame(
            self.content,
            bg="white"
        )

        form.pack(
            padx=35,
            fill="x"
        )

        tk.Label(
            form,
            text="ประเภท",
            bg="white"
        ).grid(row=0, column=0, padx=10, pady=15)

        type_box = ttk.Combobox(
            form,
            values=["income", "expense"],
            state="readonly"
        )

        type_box.set("income")

        type_box.grid(
            row=0,
            column=1
        )

        tk.Label(
            form,
            text="หมวดหมู่",
            bg="white"
        ).grid(row=1, column=0, padx=10)

        category = tk.Entry(form)

        category.grid(
            row=1,
            column=1
        )

        tk.Label(
            form,
            text="จำนวนเงิน",
            bg="white"
        ).grid(row=2, column=0, padx=10)

        amount = tk.Entry(form)

        amount.grid(
            row=2,
            column=1
        )

        tk.Label(
            form,
            text="หมายเหตุ",
            bg="white"
        ).grid(row=3, column=0, padx=10)

        note = tk.Entry(form)

        note.grid(
            row=3,
            column=1
        )

        def save():

            try:

                value = float(amount.get())

                if value <= 0:
                    raise ValueError

                add_transaction(
                    type_box.get(),
                    category.get(),
                    value,
                    note.get()
                )

                messagebox.showinfo(
                    "สำเร็จ",
                    "บันทึกรายการเรียบร้อยแล้ว"
                )

                self.show_transactions()

            except ValueError:

                messagebox.showerror(
                    "ผิดพลาด",
                    "กรุณากรอกจำนวนเงินให้ถูกต้อง"
                )

        tk.Button(
            form,
            text="บันทึกรายการ",
            command=save,
            bg="#1769E0",
            fg="white",
            relief="flat",
            padx=20,
            pady=10
        ).grid(
            row=4,
            column=1,
            pady=20
        )

    # =========================
    # GOALS
    # =========================

    def show_goals(self):

        self.clear_content()

        tk.Label(
            self.content,
            text="Savings Goals",
            font=("Arial", 25, "bold"),
            fg="#0B2A5B",
            bg="#EAF4FF"
        ).pack(
            anchor="w",
            padx=35,
            pady=30
        )

        form = tk.Frame(
            self.content,
            bg="white"
        )

        form.pack(
            padx=35,
            fill="x"
        )

        tk.Label(
            form,
            text="ชื่อเป้าหมาย",
            bg="white"
        ).grid(row=0, column=0, padx=10, pady=15)

        name = tk.Entry(form)

        name.grid(row=0, column=1)

        tk.Label(
            form,
            text="จำนวนเป้าหมาย",
            bg="white"
        ).grid(row=1, column=0, padx=10)

        target = tk.Entry(form)

        target.grid(row=1, column=1)

        tk.Label(
            form,
            text="กำหนดเวลา",
            bg="white"
        ).grid(row=2, column=0, padx=10)

        deadline = tk.Entry(form)

        deadline.grid(row=2, column=1)

        def save_goal():

            try:

                target_value = float(target.get())

                add_goal(
                    name.get(),
                    target_value,
                    deadline.get()
                )

                messagebox.showinfo(
                    "สำเร็จ",
                    "สร้างเป้าหมายเรียบร้อยแล้ว"
                )

                self.show_goals()

            except ValueError:

                messagebox.showerror(
                    "ผิดพลาด",
                    "กรุณากรอกจำนวนเป้าหมายเป็นตัวเลข"
                )

        tk.Button(
            form,
            text="เพิ่มเป้าหมาย",
            command=save_goal,
            bg="#1769E0",
            fg="white",
            relief="flat",
            padx=20,
            pady=10
        ).grid(
            row=3,
            column=1,
            pady=20
        )

        # Goal list

        table = ttk.Treeview(
            self.content,
            columns=("name", "target", "saved", "deadline"),
            show="headings"
        )

        table.heading("name", text="เป้าหมาย")
        table.heading("target", text="เป้าหมายเงิน")
        table.heading("saved", text="ออมแล้ว")
        table.heading("deadline", text="กำหนดเวลา")

        table.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=25
        )

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name, target, saved, deadline
            FROM goals
        """)

        for row in cursor.fetchall():

            table.insert(
                "",
                "end",
                values=(
                    row[0],
                    f"฿ {row[1]:,.2f}",
                    f"฿ {row[2]:,.2f}",
                    row[3]
                )
            )

        conn.close()

    # =========================
    # ANALYTICS
    # =========================

    def show_analytics(self):

        self.clear_content()

        tk.Label(
            self.content,
            text="Savings Analytics",
            font=("Arial", 25, "bold"),
            fg="#0B2A5B",
            bg="#EAF4FF"
        ).pack(
            anchor="w",
            padx=35,
            pady=30
        )

        income = get_total_income()
        expense = get_total_expense()
        savings = get_total_savings()

        text = f"""
        📊 ภาพรวมการเงิน

        รายรับทั้งหมด       ฿ {income:,.2f}

        รายจ่ายทั้งหมด      ฿ {expense:,.2f}

        เงินออมทั้งหมด      ฿ {savings:,.2f}

        อัตราการออม        {(savings / income * 100) if income else 0:.2f}%

        💡 คำแนะนำ

        {"คุณมีอัตราการออมที่ดี" if savings > 0 else "ควรเริ่มบันทึกรายรับและรายจ่าย"}
        """

        tk.Label(
            self.content,
            text=text,
            font=("Arial", 16),
            justify="left",
            fg="#17365D",
            bg="white",
            padx=30,
            pady=30
        ).pack(
            padx=40,
            fill="x"
        )

    # =========================
    # REPORTS
    # =========================

    def show_reports(self):

        self.clear_content()

        tk.Label(
            self.content,
            text="Financial Reports",
            font=("Arial", 25, "bold"),
            fg="#0B2A5B",
            bg="#EAF4FF"
        ).pack(
            anchor="w",
            padx=35,
            pady=30
        )

        income = get_total_income()
        expense = get_total_expense()
        savings = get_total_savings()

        report = f"""
        SAVINGS SYSTEM REPORT
        ----------------------------

        วันที่: {datetime.now().strftime("%d/%m/%Y")}

        รายรับทั้งหมด:
        ฿ {income:,.2f}

        รายจ่ายทั้งหมด:
        ฿ {expense:,.2f}

        เงินออมทั้งหมด:
        ฿ {savings:,.2f}

        อัตราการออม:
        {(savings / income * 100) if income else 0:.2f} %

        ----------------------------

        สถานะ:
        {"มีเงินออม" if savings > 0 else "ควรเริ่มวางแผนการออม"}

        """

        tk.Label(
            self.content,
            text=report,
            font=("Consolas", 14),
            justify="left",
            bg="white",
            fg="#17365D",
            padx=30,
            pady=30
        ).pack(
            padx=40,
            fill="x"
        )


# =========================
# RUN
# =========================

if __name__ == "__main__":

    create_database()

    root = tk.Tk()

    app = SavingsApp(root)

    root.mainloop()