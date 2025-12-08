# 🏎️ MyF1Garage — Fantasy Formula 1 Web Application

MyF1Garage is a full-stack Django web application that allows users to create their own fantasy Formula 1 teams, earn points based on real race results, and compete on a global leaderboard. Users strategically select two drivers and one constructor while managing a budget cap. The app dynamically assigns points after each race and updates both team standings and the seasonal leaderboard.

Video Demo : https://youtu.be/Xig3vI3bIa4


## Distinctiveness and Complexity

### **Why this project is distinctive**

This project is far more than a simple CRUD app. It introduces **game mechanics**, **dynamic scoring**, real-world inspired **budget management**, and an interactive leaderboard. Unlike typical Django projects (blogs, to-dos, wikis, etc.), MyF1Garage implements:

* A **fantasy sports scoring system**, dynamically generated from race data
* A **budget-constrained selection system** that recalculates remaining budget on the fly
* A **multi-level points architecture** (Driver → Constructor → Fantasy Team → Season Score)
* Automatic backend logic that updates all scores after each race result
* Conditional views that adapt based on whether the user has created a team
* A fully functional leaderboard system that aggregates season scores
* Admin-level scoring assignment with recalculation for all users

These features make the project structurally and conceptually more complex than standard Django exercises.

### **Why this project is complex**

This application involves multiple interconnected models and dynamic business logic, such as:

* Relationship-heavy models (`Driver`, `Constructor`, `Race`, `RaceResult`, `FantasyTeam`, `TeamScore`, `SeasonScore`)
* Chained recalculations where one model’s points depend on another’s
* A multi-step scoring pipeline implemented in the `assign_points` function
* Conditional views (e.g., redirecting to “Create Team” if no team exists)
* Race scheduling and automatic upcoming race detection
* Custom admin logic including leaderboard display
* High-level state management for user teams (create, edit, view)

Together, these reflect a high degree of technical complexity and backend logic well beyond basic CRUD apps.

---

## Project Structure & File Overview

Below is a clear overview of each important file you created:

### **Models (`models.py`)**

Defines all core entities:

* **Driver** — cost & points per race
* **Constructor** — links to drivers, collects points
* **Race** — race schedule
* **RaceResult** — driver-specific race outcome
* **FantasyTeam** — user’s selected driver/constructor lineup
* **TeamScore** — race-by-race fantasy score
* **SeasonScore** — aggregated leaderboard scoring

### **Views (`views.py`)**

Contains:

* `index` — home dashboard with constructors, races, and top leaderboard users
* `create_fantasy_team` & `edit_fantasy_team` — handles budget logic and team creation
* `assign_points` — recalculates every driver, constructor, team, and season score
* `leaderboard` — generates leaderboard data for rendering

### **Templates (`templates/fantasy/*.html`)**

User interface pages:

* Homepage, team creation, edit team, leaderboard, admin scoring success, etc.

### **Admin (`admin.py`)**

* Registers all models
* Adds custom leaderboard (SeasonScoreAdmin) with sorting, filtering, search

### **Static Files**

* CSS styling, F1-inspired layouts, icons, buttons, background images

### **Other Core Files**

* `urls.py` — all routing
* `requirements.txt` — packages required
* `README.md` — documentation

---

## How to Run the Application

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd <project-folder>
   ```

2. **Create & activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate       # Mac/Linux
   venv\Scripts\activate          # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**

   ```bash
   python manage.py runserver
   ```

7. Visit:
   **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## Additional Notes

* Only admins can assign points (via the backend scoring system).
* Users can create only **one fantasy team** per account.
* When a user edits or creates a team, their season score automatically syncs.
* Leaderboard updates instantly after `assign_points` is executed.
* The app follows real F1-inspired scoring structure and budget rules.

---