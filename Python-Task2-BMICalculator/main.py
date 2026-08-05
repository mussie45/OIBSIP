from tkinter import *
from tkinter import messagebox
import sqlite3


def init_db():
    conn = sqlite3.connect("Records.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gender TEXT,
            age INTEGER,
            height REAL,
            weight REAL,
            bmi REAL,
            category TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()

selected_gender = "Male"


def set_gender(gender_val):
    global selected_gender
    selected_gender = gender_val
    if gender_val == "Male":
        Male.config(bg="#3B82F6", fg="#FFFFFF")
        Female.config(bg="#1E293B", fg="#94A3B8")
    else:
        Female.config(bg="#EC4899", fg="#FFFFFF")
        Male.config(bg="#1E293B", fg="#94A3B8")


def Calculation():
    try:
        h = slide_h("c")
        w = slide_w("c")

        if h <= 0:
            return

        score = w / ((h / 100) ** 2)
        Score.config(text=f"{score:.1f}")

        if score < 18.5:
            Tag.config(text="UNDERWEIGHT", fg="#3B82F6")
            Score_sub.config(text="Below healthy range", fg="#3B82F6")
        elif score < 25:
            Tag.config(text="HEALTHY WEIGHT", fg="#10B981")
            Score_sub.config(text="Optimal range", fg="#10B981")
        elif score < 30:
            Tag.config(text="OVERWEIGHT", fg="#F59E0B")
            Score_sub.config(text="Above healthy range", fg="#F59E0B")
        else:
            Tag.config(text="OBESE", fg="#EF4444")
            Score_sub.config(text="Class I+ Obesity", fg="#EF4444")

    except Exception as e:
        messagebox.showerror("Error", f"Calculation failed: {e}")


def slide_h(var):
    val = Height_slider.get()
    Height_num.config(text=f"{val} cm")
    return val


def slide_w(var):
    val = Weight_slider.get()
    Weight_num.config(text=f"{val} kg")
    return val


def save_to_db():
    age_val = Age_e.get().strip()
    if not age_val.isdigit():
        messagebox.showwarning("Input Error", "Please enter a valid age.")
        return

    try:
        bmi_val = float(Score.cget("text"))
    except ValueError:
        messagebox.showwarning("Error", "Please calculate BMI first.")
        return

    conn = sqlite3.connect("Records.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bmi_records (gender, age, height, weight, bmi, category)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (selected_gender, int(age_val), Height_slider.get(), Weight_slider.get(), bmi_val, Tag.cget("text")))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Record saved successfully!")


BG_MAIN = "#0F172A"
BG_CARD = "#1E293B"
ACCENT_BLUE = "#3B82F6"
TEXT_PRIMARY = "#F8FAFC"
TEXT_MUTED = "#64748B"
BORDER_COLOR = "#334155"


root = Tk()
root.title("BioMetricPro - BMI Analytics")
root.geometry("900x500")
root.configure(bg=BG_MAIN)
root.resizable(False, False)

header = Frame(root, bg=BG_MAIN)
header.pack(fill=X, padx=40, pady=(20, 10))

Title = Label(
    header,
    text="BioMetricPro",
    font=("Segoe UI", 22, "bold"),
    fg=TEXT_PRIMARY,
    bg=BG_MAIN
)
Title.pack(anchor=W)

subTitle = Label(
    header,
    text="Health Analytics & Persistent Tracking",
    font=("Segoe UI", 10),
    fg=TEXT_MUTED,
    bg=BG_MAIN
)
subTitle.pack(anchor=W)


body_frame = Frame(root, bg=BG_MAIN)
body_frame.pack(fill=BOTH, expand=True, padx=40, pady=10)


Parameters = LabelFrame(
    body_frame,
    text="  INPUT PARAMETERS  ",
    font=("Segoe UI", 10, "bold"),
    fg=TEXT_MUTED,
    bg=BG_CARD,
    bd=1,
    relief=SOLID,
    padx=20,
    pady=15
)
Parameters.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 15))


Gender = Label(Parameters, text="GENDER", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=BG_CARD)
Gender.grid(row=0, column=0, columnspan=2, sticky=W, pady=(5, 5))

Age = Label(Parameters, text="AGE", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=BG_CARD)
Age.grid(row=0, column=2, sticky=W, pady=(5, 5), padx=(20, 0))


Male = Button(
    Parameters,
    text="Male",
    command=lambda: set_gender("Male"),
    font=("Segoe UI", 10, "bold"),
    bg=ACCENT_BLUE,
    fg="#FFFFFF",
    activebackground=ACCENT_BLUE,
    activeforeground="#FFFFFF",
    relief=FLAT,
    width=9,
    cursor="hand2"
)
Male.grid(row=1, column=0, sticky=W, pady=(0, 15))

Female = Button(
    Parameters,
    text="Female",
    command=lambda: set_gender("Female"),
    font=("Segoe UI", 10, "bold"),
    bg=BG_CARD,
    fg=TEXT_MUTED,
    activebackground="#EC4899",
    activeforeground="#FFFFFF",
    relief=FLAT,
    width=9,
    cursor="hand2"
)
Female.grid(row=1, column=1, sticky=W, padx=(5, 0), pady=(0, 15))

Age_e = Entry(
    Parameters,
    font=("Segoe UI", 11, "bold"),
    justify="center",
    relief=FLAT,
    bg="#0F172A",
    fg=TEXT_PRIMARY,
    insertbackground=TEXT_PRIMARY,
    width=8
)
Age_e.insert(0, "25")
Age_e.grid(row=1, column=2, sticky=W, padx=(20, 0), pady=(0, 15), ipady=4)

Height = Label(Parameters, text="HEIGHT", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=BG_CARD)
Height.grid(row=2, column=0, sticky=W, pady=(5, 0))

Height_num = Label(Parameters, text="170 cm", font=("Segoe UI", 10, "bold"), fg=ACCENT_BLUE, bg=BG_CARD)
Height_num.grid(row=2, column=2, sticky=E, pady=(5, 0))

Height_slider = Scale(
    Parameters,
    from_=0,
    to=230,
    orient=HORIZONTAL,
    command=slide_h,
    bg=BG_CARD,
    fg=TEXT_PRIMARY,
    bd=0,
    highlightthickness=0,
    troughcolor="#0F172A",
    activebackground=ACCENT_BLUE,
    showvalue=False
)
Height_slider.set(170)
Height_slider.grid(row=3, columnspan=3, sticky=EW, pady=(5, 15))

Weight = Label(Parameters, text="WEIGHT", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=BG_CARD)
Weight.grid(row=4, column=0, sticky=W, pady=(5, 0))

Weight_num = Label(Parameters, text="70 kg", font=("Segoe UI", 10, "bold"), fg=ACCENT_BLUE, bg=BG_CARD)
Weight_num.grid(row=4, column=2, sticky=E, pady=(5, 0))

Weight_slider = Scale(
    Parameters,
    from_=0,
    to=230,
    orient=HORIZONTAL,
    command=slide_w,
    bg=BG_CARD,
    fg=TEXT_PRIMARY,
    bd=0,
    highlightthickness=0,
    troughcolor="#0F172A",
    activebackground=ACCENT_BLUE,
    showvalue=False
)
Weight_slider.set(70)
Weight_slider.grid(row=5, columnspan=3, sticky=EW, pady=(5, 20))

Calculate = Button(
    Parameters,
    text="CALCULATE BMI",
    command=Calculation,
    font=("Segoe UI", 10, "bold"),
    bg=ACCENT_BLUE,
    fg="#FFFFFF",
    activebackground="#2563EB",
    activeforeground="#FFFFFF",
    relief=FLAT,
    pady=8,
    cursor="hand2"
)
Calculate.grid(row=6, columnspan=3, sticky=EW, pady=(5, 0))

Result = LabelFrame(
    body_frame,
    text="  ANALYTICS DISPLAY  ",
    font=("Segoe UI", 10, "bold"),
    fg=TEXT_MUTED,
    bg=BG_CARD,
    bd=1,
    relief=SOLID,
    padx=20,
    pady=15
)
Result.pack(side=RIGHT, fill=BOTH, expand=True, padx=(15, 0))

Tag = Label(Result, text="HEALTHY WEIGHT", font=("Segoe UI", 12, "bold"), fg="#10B981", bg=BG_CARD)
Tag.pack(anchor=CENTER, pady=(15, 0))

Score = Label(Result, text="21.8", font=("Segoe UI", 56, "bold"), fg=TEXT_PRIMARY, bg=BG_CARD)
Score.pack(anchor=CENTER)

Score_sub = Label(Result, text="Optimal range", font=("Segoe UI", 10, "bold"), fg="#10B981", bg=BG_CARD)
Score_sub.pack(anchor=CENTER, pady=(0, 20))

range_frame = Frame(Result, bg=BG_CARD)
range_frame.pack(fill=X, pady=(10, 20))

for i in range(4):
    range_frame.grid_columnconfigure(i, weight=1)

Underweight = Label(range_frame, text="< 18.5\nUnder", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD, justify=CENTER)
Underweight.grid(row=0, column=0)

Normal = Label(range_frame, text="18.5 - 24.9\nNormal", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD, justify=CENTER)
Normal.grid(row=0, column=1)

Overweight = Label(range_frame, text="25 - 29.9\nOver", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD, justify=CENTER)
Overweight.grid(row=0, column=2)

Obese = Label(range_frame, text="≥ 30\nObese", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD, justify=CENTER)
Obese.grid(row=0, column=3)


submit_btn = Button(
    Result,
    text="SAVE TO DATABASE",
    command=save_to_db,
    font=("Segoe UI", 10, "bold"),
    bg="#10B981",
    fg="#FFFFFF",
    activebackground="#059669",
    activeforeground="#FFFFFF",
    relief=FLAT,
    pady=8,
    cursor="hand2"
)
submit_btn.pack(fill=X, side=BOTTOM, pady=(10, 0))

Calculation()


root.mainloop()