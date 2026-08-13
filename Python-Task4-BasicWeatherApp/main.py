from tkinter import *
from PIL import ImageTk, Image
import requests
import json

root = Tk()
root.title("Weather App")
root.iconbitmap()
root.geometry("700x180")
root.configure(bg="#f5f5f5")


#https://www.airnowapi.org/aq/observation/current/racode/?format=application/json&reportingAreaCode=wa008&API_KEY=A9B64DB0-8CBA-453A-8283-C0A45FCFDA7A

def ziplookup():
    try:
        api_requests = requests.get(
            "https://www.airnowapi.org/aq/forecast/current/?format=application/json&zipCode="
            + str(zip.get())
            + "&API_KEY=A9B64DB0-8CBA-453A-8283-C0A45FCFDA7A"
        )

        api = json.loads(api_requests.content)

        city = api[0]["reportingArea"]
        quality = api[0]["aqi"]
        category = api[0]["categoryName"]

        # Air Quality Colors
        if category == "Good":
            weather_color = "#00E400"

        elif category == "Moderate":
            weather_color = "#FFFF00"

        elif category == "Unhealthy for Sensitive Groups":
            weather_color = "#FF7E00"

        elif category == "Unhealthy":
            weather_color = "#FF0000"

        elif category == "Very Unhealthy":
            weather_color = "#8F3F97"

        elif category == "Hazardous":
            weather_color = "#7E0023"

        root.configure(bg=weather_color)

        myLabel = Label(
            root,
            text=city + " Air Quality " + str(quality) + " " + category,
            font=("Helvetica", 20, "bold"),
            bg=weather_color,
            fg="black",
            pady=20
        )

        myLabel.grid(row=1, column=0, columnspan=2, pady=20)

    except Exception as e:
        api = "Error..."
    zip.delete(0, END)


zip = Entry(
    root,
    font=("Helvetica", 16),
    justify="center",
    relief=FLAT,
    bd=8,
    width=20
)

zip.grid(row=0, column=0, padx=20, pady=20)


zibButton = Button(
    root,
    text="🔍 Lookup Zip Code",
    command=ziplookup,
    font=("Helvetica", 13, "bold"),
    bg="#1E88E5",
    fg="white",
    activebackground="#1565C0",
    activeforeground="white",
    relief=FLAT,
    padx=20,
    pady=8,
    cursor="hand2"
)

zibButton.grid(row=0, column=1, padx=10, pady=20, sticky=W+E)


root.mainloop()
