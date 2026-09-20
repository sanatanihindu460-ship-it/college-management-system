import json
from pathlib import Path
from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk, messagebox

# ============================================================
# BACKEND
# ============================================================

DATABASE = "college_data.json"
data = {"students": [], "teachers": []}

if Path(DATABASE).exists():
    try:
        with open(DATABASE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                data = json.loads(content)
    except (json.JSONDecodeError, OSError):
        data = {"students": [], "teachers": []}

# Make sure old/incomplete JSON files don't crash the application.
data.setdefault("students", [])
data.setdefault("teachers", [])


def save():
    with open(DATABASE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


class Persons(ABC):
    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def show_details(self):
        pass

    @staticmethod
    def valid_email(email):
        return "@" in email and "." in email.split("@")[-1]


class Student(Persons):
    def get_roles(self):
        return "Student"

    def register(self, name, age, email, roll_no):
        if not Persons.valid_email(email):
            raise ValueError("Please enter a valid email address.")

        for student in data["students"]:
            if student["Roll_No"] == roll_no:
                raise ValueError("A student with this roll number already exists.")

        data["students"].append({
            "Name": name,
            "Age": age,
            "Email": email,
            "Roll_No": roll_no,
            "Grades": {}
        })
        save()

    def show_details(self):
        pass

    def add_grades(self, roll_no, grades):
        student = self._find(roll_no)
        if student is None:
            raise ValueError("Student not found.")

        for subject, marks in grades.items():
            student["Grades"][subject] = marks
        save()

    def update_grades(self, roll_no, subject, marks):
        student = self._find(roll_no)
        if student is None:
            raise ValueError("Student not found.")

        student["Grades"][subject] = marks
        save()

    @staticmethod
    def _find(roll_no):
        for student in data["students"]:
            if student.get("Roll_No") == roll_no:
                return student
        return None


class Teacher(Persons):
    def get_roles(self):
        return "Teacher"

    def register(self, name, age, email, teacher_id, department, salary):
        if not Persons.valid_email(email):
            raise ValueError("Please enter a valid email address.")

        for teacher in data["teachers"]:
            if teacher["Id"] == teacher_id:
                raise ValueError("A teacher with this ID already exists.")

        data["teachers"].append({
            "Name": name,
            "Age": age,
            "Email": email,
            "Id": teacher_id,
            "Department": department,
            "Salary": salary
        })
        save()

    def show_details(self):
        pass

    def update_salary(self, teacher_id, salary):
        teacher = self._find(teacher_id)
        if teacher is None:
            raise ValueError("Teacher not found.")

        teacher["Salary"] = salary
        save()

    @staticmethod
    def _find(teacher_id):
        for teacher in data["teachers"]:
            if teacher.get("Id") == teacher_id:
                return teacher
        return None


student_backend = Student()
teacher_backend = Teacher()


# ============================================================
# PROFESSIONAL TKINTER UI
# ============================================================

class CollegeManagementApp(tk.Tk):
    BG = "#F4F7FB"
    CARD = "#FFFFFF"
    SIDEBAR = "#172033"
    SIDEBAR_HOVER = "#25324A"
    TEXT = "#172033"
    MUTED = "#68758A"
    PRIMARY = "#4F46E5"
    PRIMARY_HOVER = "#4338CA"
    SUCCESS = "#059669"
    DANGER = "#DC2626"
    BORDER = "#DCE2EA"

    def __init__(self):
        super().__init__()

        self.title("College Management System")
        self.geometry("1180x720")
        self.minsize(1000, 650)
        self.configure(bg=self.BG)

        self.current_page = None

        self.setup_styles()
        self.build_layout()
        self.show_dashboard()

    # -------------------- Styling --------------------

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=self.CARD,
            fieldbackground=self.CARD,
            foreground=self.TEXT,
            rowheight=38,
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background="#EEF1F6",
            foreground=self.TEXT,
            font=("Segoe UI Semibold", 10),
            padding=10,
            relief="flat"
        )
        style.map(
            "Treeview",
            background=[("selected", "#E0E7FF")],
            foreground=[("selected", self.TEXT)]
        )

        style.configure(
            "TCombobox",
            padding=8,
            fieldbackground=self.CARD,
            background=self.CARD
        )

    # -------------------- Main Layout --------------------

    def build_layout(self):
        self.sidebar = tk.Frame(self, bg=self.SIDEBAR, width=245)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(self, bg=self.BG)
        self.content.pack(side="right", fill="both", expand=True)

        self.build_sidebar()

    def build_sidebar(self):
        brand = tk.Frame(self.sidebar, bg=self.SIDEBAR)
        brand.pack(fill="x", padx=22, pady=(25, 35))

        logo = tk.Label(
            brand,
            text="CM",
            bg=self.PRIMARY,
            fg="white",
            font=("Segoe UI Bold", 18),
            width=3,
            height=1
        )
        logo.pack(side="left")

        title_box = tk.Frame(brand, bg=self.SIDEBAR)
        title_box.pack(side="left", padx=12)

        tk.Label(
            title_box,
            text="College",
            bg=self.SIDEBAR,
            fg="white",
            font=("Segoe UI Semibold", 14)
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="Management",
            bg=self.SIDEBAR,
            fg="#9DA9BC",
            font=("Segoe UI", 9)
        ).pack(anchor="w")

        self.nav_buttons = {}

        items = [
            ("⌂", "Dashboard", self.show_dashboard),
            ("♙", "Students", self.show_students),
            ("♧", "Teachers", self.show_teachers),
            ("＋", "Add Student", self.show_add_student),
            ("＋", "Add Teacher", self.show_add_teacher),
            ("★", "Manage Grades", self.show_grades),
            ("$", "Update Salary", self.show_salary),
        ]

        for icon, text, command in items:
            self.add_nav_button(icon, text, command)

        bottom = tk.Frame(self.sidebar, bg=self.SIDEBAR)
        bottom.pack(side="bottom", fill="x", padx=20, pady=20)

        tk.Label(
            bottom,
            text="College Management System",
            bg=self.SIDEBAR,
            fg="#718096",
            font=("Segoe UI", 8)
        ).pack(anchor="w")

        tk.Label(
            bottom,
            text="Local JSON Database",
            bg=self.SIDEBAR,
            fg="#718096",
            font=("Segoe UI", 8)
        ).pack(anchor="w", pady=(3, 0))

    def add_nav_button(self, icon, text, command):
        btn = tk.Button(
            self.sidebar,
            text=f"  {icon}   {text}",
            command=command,
            anchor="w",
            bg=self.SIDEBAR,
            fg="#DCE3EF",
            activebackground=self.SIDEBAR_HOVER,
            activeforeground="white",
            bd=0,
            relief="flat",
            font=("Segoe UI", 10),
            padx=20,
            pady=12,
            cursor="hand2"
        )
        btn.pack(fill="x", padx=10, pady=2)
        self.nav_buttons[text] = btn

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def page_header(self, title, subtitle):
        header = tk.Frame(self.content, bg=self.BG)
        header.pack(fill="x", padx=35, pady=(28, 18))

        tk.Label(
            header,
            text=title,
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI Bold", 24)
        ).pack(anchor="w")

        tk.Label(
            header,
            text=subtitle,
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 0))

    def card(self, parent, width=None, height=None):
        frame = tk.Frame(
            parent,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )
        if width:
            frame.config(width=width)
        if height:
            frame.config(height=height)
        return frame

    def stat_card(self, parent, title, value, icon, accent):
        frame = self.card(parent)
        frame.pack(side="left", fill="both", expand=True, padx=7)

        inner = tk.Frame(frame, bg=self.CARD)
        inner.pack(fill="both", expand=True, padx=18, pady=18)

        top = tk.Frame(inner, bg=self.CARD)
        top.pack(fill="x")

        tk.Label(
            top,
            text=icon,
            bg=accent,
            fg="white",
            font=("Segoe UI Bold", 15),
            width=3,
            height=1
        ).pack(side="left")

        tk.Label(
            top,
            text=title,
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI Semibold", 10)
        ).pack(side="left", padx=12)

        tk.Label(
            inner,
            text=str(value),
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI Bold", 25)
        ).pack(anchor="w", pady=(14, 0))

        return frame

    def entry(self, parent, label, variable, show=None):
        box = tk.Frame(parent, bg=self.CARD)
        box.pack(fill="x", pady=7)

        tk.Label(
            box,
            text=label,
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI Semibold", 9)
        ).pack(anchor="w", pady=(0, 5))

        ent = tk.Entry(
            box,
            textvariable=variable,
            show=show or "",
            bg="#FAFBFD",
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.PRIMARY,
            font=("Segoe UI", 10)
        )
        ent.pack(fill="x", ipady=9)
        return ent

    def button(self, parent, text, command, primary=True):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.PRIMARY if primary else "#EEF1F6",
            fg="white" if primary else self.TEXT,
            activebackground=self.PRIMARY_HOVER if primary else "#E2E6ED",
            activeforeground="white" if primary else self.TEXT,
            bd=0,
            relief="flat",
            font=("Segoe UI Semibold", 10),
            padx=18,
            pady=10,
            cursor="hand2"
        )

    # -------------------- Dashboard --------------------

    def show_dashboard(self):
        self.clear_content()
        self.page_header(
            "Dashboard",
            "Welcome back. Here's an overview of your college management system."
        )

        stats = tk.Frame(self.content, bg=self.BG)
        stats.pack(fill="x", padx=28)

        self.stat_card(
            stats, "Total Students", len(data["students"]), "S", self.PRIMARY
        )
        self.stat_card(
            stats, "Total Teachers", len(data["teachers"]), "T", self.SUCCESS
        )

        total_grades = sum(
            len(student.get("Grades", {})) for student in data["students"]
        )
        self.stat_card(
            stats, "Grades Recorded", total_grades, "G", "#D97706"
        )

        departments = len({
            teacher.get("Department", "").strip()
            for teacher in data["teachers"]
            if teacher.get("Department", "").strip()
        })
        self.stat_card(
            stats, "Departments", departments, "D", "#7C3AED"
        )

        recent = self.card(self.content)
        recent.pack(fill="both", expand=True, padx=35, pady=25)

        top = tk.Frame(recent, bg=self.CARD)
        top.pack(fill="x", padx=20, pady=18)

        tk.Label(
            top,
            text="Quick Actions",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI Bold", 14)
        ).pack(side="left")

        actions = tk.Frame(recent, bg=self.CARD)
        actions.pack(fill="x", padx=20, pady=5)

        quick = [
            ("＋  Register Student", self.show_add_student),
            ("＋  Register Teacher", self.show_add_teacher),
            ("★  Manage Grades", self.show_grades),
            ("$  Update Salary", self.show_salary),
        ]

        for text, cmd in quick:
            self.button(actions, text, cmd).pack(
                side="left", padx=(0, 10), pady=10
            )

        info = tk.Frame(recent, bg="#F8FAFC")
        info.pack(fill="x", padx=20, pady=20)

        tk.Label(
            info,
            text="Tip",
            bg="#F8FAFC",
            fg=self.PRIMARY,
            font=("Segoe UI Bold", 10)
        ).pack(side="left", padx=15, pady=14)

        tk.Label(
            info,
            text="Use the sidebar to manage students, teachers, grades and salaries.",
            bg="#F8FAFC",
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).pack(side="left")

    # -------------------- Students --------------------

    def show_students(self):
        self.clear_content()
        self.page_header(
            "Students",
            "View registered students and their academic information."
        )

        top = tk.Frame(self.content, bg=self.BG)
        top.pack(fill="x", padx=35)

        self.button(top, "+ Add Student", self.show_add_student).pack(side="right")

        search_var = tk.StringVar()

        search_frame = tk.Frame(top, bg=self.BG)
        search_frame.pack(side="left", fill="x", expand=True)

        tk.Label(
            search_frame, text="Search:", bg=self.BG,
            fg=self.MUTED, font=("Segoe UI Semibold", 9)
        ).pack(side="left", padx=(0, 8))

        search = tk.Entry(
            search_frame, textvariable=search_var,
            bg=self.CARD, fg=self.TEXT, relief="flat",
            highlightthickness=1, highlightbackground=self.BORDER,
            font=("Segoe UI", 10)
        )
        search.pack(side="left", fill="x", expand=True, ipady=8)

        table_card = self.card(self.content)
        table_card.pack(fill="both", expand=True, padx=35, pady=18)

        columns = ("Roll No", "Name", "Age", "Email", "Subjects")
        tree = ttk.Treeview(table_card, columns=columns, show="headings")

        widths = {"Roll No": 100, "Name": 180, "Age": 70, "Email": 300, "Subjects": 100}
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=widths[col], anchor="w")

        scrollbar = ttk.Scrollbar(table_card, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        def refresh(*_):
            query = search_var.get().lower().strip()
            for item in tree.get_children():
                tree.delete(item)

            for student in data["students"]:
                text = f'{student.get("Name", "")} {student.get("Email", "")} {student.get("Roll_No", "")}'.lower()
                if query and query not in text:
                    continue

                tree.insert(
                    "",
                    "end",
                    values=(
                        student.get("Roll_No", ""),
                        student.get("Name", ""),
                        student.get("Age", ""),
                        student.get("Email", ""),
                        len(student.get("Grades", {}))
                    )
                )

        search_var.trace_add("write", refresh)
        refresh()

    # -------------------- Teachers --------------------

    def show_teachers(self):
        self.clear_content()
        self.page_header(
            "Teachers",
            "View registered faculty members and their departments."
        )

        top = tk.Frame(self.content, bg=self.BG)
        top.pack(fill="x", padx=35)

        self.button(top, "+ Add Teacher", self.show_add_teacher).pack(side="right")

        table_card = self.card(self.content)
        table_card.pack(fill="both", expand=True, padx=35, pady=18)

        columns = ("ID", "Name", "Age", "Email", "Department", "Salary")
        tree = ttk.Treeview(table_card, columns=columns, show="headings")

        widths = {
            "ID": 80, "Name": 180, "Age": 70,
            "Email": 260, "Department": 160, "Salary": 130
        }

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=widths[col], anchor="w")

        scrollbar = ttk.Scrollbar(table_card, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        for teacher in data["teachers"]:
            tree.insert(
                "",
                "end",
                values=(
                    teacher.get("Id", ""),
                    teacher.get("Name", ""),
                    teacher.get("Age", ""),
                    teacher.get("Email", ""),
                    teacher.get("Department", ""),
                    f'₹ {teacher.get("Salary", 0):,}'
                )
            )

    # -------------------- Add Student --------------------

    def show_add_student(self):
        self.clear_content()
        self.page_header(
            "Register Student",
            "Create a new student profile in the college database."
        )

        container = tk.Frame(self.content, bg=self.BG)
        container.pack(fill="both", expand=True, padx=35)

        form = self.card(container)
        form.pack(fill="x", padx=100, pady=10)

        tk.Label(
            form,
            text="Student Information",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI Bold", 14)
        ).pack(anchor="w", padx=25, pady=(22, 5))

        tk.Label(
            form,
            text="All fields are required.",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=25)

        fields = tk.Frame(form, bg=self.CARD)
        fields.pack(fill="x", padx=25, pady=15)

        name = tk.StringVar()
        age = tk.StringVar()
        email = tk.StringVar()
        roll = tk.StringVar()

        self.entry(fields, "Full Name", name)
        self.entry(fields, "Age", age)
        self.entry(fields, "Email", email)
        self.entry(fields, "Roll Number", roll)

        actions = tk.Frame(form, bg=self.CARD)
        actions.pack(fill="x", padx=25, pady=(5, 25))

        def submit():
            if not all([name.get().strip(), age.get().strip(), email.get().strip(), roll.get().strip()]):
                messagebox.showwarning("Missing Information", "Please fill in all fields.")
                return

            try:
                student_backend.register(
                    name.get().strip(),
                    int(age.get()),
                    email.get().strip(),
                    int(roll.get())
                )
                messagebox.showinfo("Success", "Student registered successfully.")
                self.show_students()
            except ValueError as e:
                messagebox.showerror("Unable to Register", str(e))

        self.button(actions, "Register Student", submit).pack(side="right")
        self.button(actions, "Cancel", self.show_dashboard, primary=False).pack(
            side="right", padx=10
        )

    # -------------------- Add Teacher --------------------

    def show_add_teacher(self):
        self.clear_content()
        self.page_header(
            "Register Teacher",
            "Create a new faculty profile in the college database."
        )

        form = self.card(self.content)
        form.pack(fill="x", padx=135, pady=10)

        tk.Label(
            form,
            text="Teacher Information",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI Bold", 14)
        ).pack(anchor="w", padx=25, pady=(22, 5))

        tk.Label(
            form,
            text="All fields are required.",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=25)

        fields = tk.Frame(form, bg=self.CARD)
        fields.pack(fill="x", padx=25, pady=15)

        name = tk.StringVar()
        age = tk.StringVar()
        email = tk.StringVar()
        teacher_id = tk.StringVar()
        department = tk.StringVar()
        salary = tk.StringVar()

        self.entry(fields, "Full Name", name)
        self.entry(fields, "Age", age)
        self.entry(fields, "Email", email)
        self.entry(fields, "Teacher ID", teacher_id)
        self.entry(fields, "Department", department)
        self.entry(fields, "Salary", salary)

        actions = tk.Frame(form, bg=self.CARD)
        actions.pack(fill="x", padx=25, pady=(5, 25))

        def submit():
            values = [
                name.get().strip(), age.get().strip(), email.get().strip(),
                teacher_id.get().strip(), department.get().strip(), salary.get().strip()
            ]

            if not all(values):
                messagebox.showwarning("Missing Information", "Please fill in all fields.")
                return

            try:
                teacher_backend.register(
                    values[0],
                    int(values[1]),
                    values[2],
                    int(values[3]),
                    values[4],
                    int(values[5])
                )
                messagebox.showinfo("Success", "Teacher registered successfully.")
                self.show_teachers()
            except ValueError as e:
                messagebox.showerror("Unable to Register", str(e))

        self.button(actions, "Register Teacher", submit).pack(side="right")
        self.button(actions, "Cancel", self.show_dashboard, primary=False).pack(
            side="right", padx=10
        )

    # -------------------- Grades --------------------

    def show_grades(self):
        self.clear_content()
        self.page_header(
            "Manage Grades",
            "Add new grades or update grades for an existing student."
        )

        outer = tk.Frame(self.content, bg=self.BG)
        outer.pack(fill="both", expand=True, padx=35)

        selector = self.card(outer)
        selector.pack(fill="x")

        tk.Label(
            selector,
            text="Select Student",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI Bold", 13)
        ).pack(anchor="w", padx=20, pady=(18, 5))

        student_map = {
            f'{s.get("Roll_No")} — {s.get("Name")}': s.get("Roll_No")
            for s in data["students"]
        }

        selected = tk.StringVar()
        combo = ttk.Combobox(
            selector,
            textvariable=selected,
            values=list(student_map.keys()),
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo.pack(fill="x", padx=20, pady=(5, 20), ipady=4)

        details = self.card(outer)
        details.pack(fill="both", expand=True, pady=18)

        tk.Label(
            details,
            text="Grade Entry",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI Bold", 13)
        ).pack(anchor="w", padx=20, pady=(18, 5))

        form = tk.Frame(details, bg=self.CARD)
        form.pack(fill="x", padx=20)

        subject = tk.StringVar()
        marks = tk.StringVar()

        self.entry(form, "Subject", subject)
        self.entry(form, "Grade / Marks", marks)

        grades_list = tk.Listbox(
            details,
            bg="#FAFBFD",
            fg=self.TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.BORDER,
            font=("Segoe UI", 10),
            height=7
        )
        grades_list.pack(fill="both", expand=True, padx=20, pady=10)

        def refresh_grades(_=None):
            grades_list.delete(0, "end")
            key = selected.get()
            if not key:
                return

            roll = student_map.get(key)
            student = Student._find(roll)

            if student:
                grades = student.get("Grades", {})
                if grades:
                    for sub, mark in grades.items():
                        grades_list.insert("end", f"{sub}    —    {mark}")
                else:
                    grades_list.insert("end", "No grades recorded yet.")

        combo.bind("<<ComboboxSelected>>", refresh_grades)

        actions = tk.Frame(details, bg=self.CARD)
        actions.pack(fill="x", padx=20, pady=(5, 20))

        def save_grade():
            if not selected.get():
                messagebox.showwarning("Select Student", "Please select a student first.")
                return

            if not subject.get().strip() or not marks.get().strip():
                messagebox.showwarning("Missing Information", "Enter both subject and grade.")
                return

            try:
                mark = int(marks.get())
                if mark < 0 or mark > 100:
                    raise ValueError("Grade must be between 0 and 100.")

                roll = student_map[selected.get()]
                student_backend.update_grades(roll, subject.get().strip(), mark)

                subject.set("")
                marks.set("")
                refresh_grades()

                messagebox.showinfo("Success", "Grade saved successfully.")
            except ValueError as e:
                messagebox.showerror("Invalid Grade", str(e))

        self.button(actions, "Save Grade", save_grade).pack(side="right")
        self.button(
            actions, "Refresh", refresh_grades, primary=False
        ).pack(side="right", padx=10)

    # -------------------- Salary --------------------

    def show_salary(self):
        self.clear_content()
        self.page_header(
            "Update Teacher Salary",
            "Select a teacher and enter the new salary amount."
        )

        form = self.card(self.content)
        form.pack(fill="x", padx=160, pady=15)

        tk.Label(
            form,
            text="Salary Update",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI Bold", 14)
        ).pack(anchor="w", padx=25, pady=(22, 10))

        teacher_map = {
            f'{t.get("Id")} — {t.get("Name")}': t.get("Id")
            for t in data["teachers"]
        }

        selected = tk.StringVar()
        salary = tk.StringVar()

        tk.Label(
            form,
            text="Teacher",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI Semibold", 9)
        ).pack(anchor="w", padx=25, pady=(5, 5))

        combo = ttk.Combobox(
            form,
            textvariable=selected,
            values=list(teacher_map.keys()),
            state="readonly"
        )
        combo.pack(fill="x", padx=25, ipady=5)

        self.entry(form, "New Salary", salary)

        actions = tk.Frame(form, bg=self.CARD)
        actions.pack(fill="x", padx=25, pady=(5, 25))

        def update():
            if not selected.get() or not salary.get().strip():
                messagebox.showwarning(
                    "Missing Information",
                    "Select a teacher and enter the new salary."
                )
                return

            try:
                amount = int(salary.get())
                if amount < 0:
                    raise ValueError("Salary cannot be negative.")

                teacher_backend.update_salary(
                    teacher_map[selected.get()],
                    amount
                )
                salary.set("")
                messagebox.showinfo("Success", "Teacher salary updated successfully.")
                self.show_teachers()
            except ValueError as e:
                messagebox.showerror("Unable to Update", str(e))

        self.button(actions, "Update Salary", update).pack(side="right")

    # -------------------- Run --------------------


if __name__ == "__main__":
    app = CollegeManagementApp()
    app.mainloop()
