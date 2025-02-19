from flask import Flask, request, render_template_string
from datetime import date
import calendar

app = Flask(__name__)

# Function to calculate age
def calculate_age(birth_date, given_date):
    years = given_date.year - birth_date.year
    months = given_date.month - birth_date.month
    days = given_date.day - birth_date.day

    if days < 0:
        months -= 1
        days += 30  # Approximate month days

    if months < 0:
        years -= 1
        months += 12

    return years, months, days

# HTML Template (Fixes "Were" vs "Will Be")
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Age Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        form { display: inline-block; text-align: left; padding: 20px; border: 1px solid #ddd; }
        input, select, button { padding: 10px; margin: 5px; }
        .error { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Age Calculator</h1>
    <form method="POST">
        <label>First Name:</label>
        <input type="text" name="first_name" value="{{ first_name }}" required><br>
        
        <label>Last Name:</label>
        <input type="text" name="last_name" value="{{ last_name }}" required><br>
        
        <label>Birth Year:</label>
        <input type="number" name="year" value="{{ year }}" min="1900" max="2100" required><br>
        
        <label>Birth Month:</label>
        <input type="number" name="month" value="{{ month }}" min="1" max="12" required><br>
        
        <label>Birth Day:</label>
        <input type="number" name="day" value="{{ day }}" min="1" max="31" required><br>

        <label>Choose Calculation Type:</label>
        <select name="choice" id="choice">
            <option value="1" {% if choice == "1" %}selected{% endif %}>My Age Today</option>
            <option value="2" {% if choice == "2" %}selected{% endif %}>My Age on a Past Date</option>
            <option value="3" {% if choice == "3" %}selected{% endif %}>My Age on a Future Date</option>
        </select><br>

        <div id="extra_inputs" style="{% if choice == '2' or choice == '3' %}display:block{% else %}display:none{% endif %};">
            <label>Year:</label>
            <input type="number" name="check_year" value="{{ check_year }}" min="1900" max="2100"><br>
            
            <label>Month:</label>
            <input type="number" name="check_month" value="{{ check_month }}" min="1" max="12"><br>
            
            <label>Day:</label>
            <input type="number" name="check_day" value="{{ check_day }}" min="1" max="31"><br>
        </div>

        <button type="submit">Calculate Age</button>
    </form>

    <h2>{{ result }}</h2>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    first_name = last_name = ""
    year = month = day = ""
    check_year = check_month = check_day = ""
    choice = "1"

    if request.method == "POST":
        first_name = request.form.get("first_name", "")
        last_name = request.form.get("last_name", "")
        year = request.form.get("year", "")
        month = request.form.get("month", "")
        day = request.form.get("day", "")
        choice = request.form.get("choice", "1")

        try:
            if year and month and day:
                max_day = calendar.monthrange(int(year), int(month))[1]  # Get max days in that month

                if int(day) > max_day:
                    result = f"Invalid Date! The maximum valid day for {month}/{year} is {max_day}."
                else:
                    birth_date = date(int(year), int(month), int(day))
                    today = date.today()

                    if choice == "1":  # Age Today
                        years, months, days = calculate_age(birth_date, today)
                        result = f"Hello {first_name} {last_name}. Today, your age is {years} years, {months} months, and {days} days."

                    elif choice in ["2", "3"]:  # Past or Future Age
                        check_year = request.form.get("check_year", "")
                        check_month = request.form.get("check_month", "")
                        check_day = request.form.get("check_day", "")

                        if check_year and check_month and check_day:
                            check_date = date(int(check_year), int(check_month), int(check_day))

                            if choice == "2" and check_date < birth_date:
                                result = "You were not born on this date!"
                            else:
                                years, months, days = calculate_age(birth_date, check_date)

                                # 🟢 Determine whether to use "were" or "will be"
                                if check_date < today:
                                    verb = "were"
                                else:
                                    verb = "will be"

                                result = f"On {check_day}/{check_month}/{check_year}, you {verb} {years} years, {months} months, and {days} days old."

        except ValueError:
            result = "Invalid Date! Please enter a correct day for the selected month and year."

    return render_template_string(html_template, result=result, first_name=first_name, last_name=last_name, 
                                  year=year, month=month, day=day, check_year=check_year, 
                                  check_month=check_month, check_day=check_day, choice=choice)

if __name__ == "__main__":
    app.run(debug=True)
