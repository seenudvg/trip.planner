import requests
from datetime import datetime

NUMBEO_API_KEY = "YOUR_NUMBEO_API_KEY"


class TripPlannerAI:
    def __init__(self):
        self.india_average_daily_cost = 3000

        self.season_notes = {
            "January": "Winter season – pack warm clothes if needed",
            "February": "Pleasant climate in most regions",
            "March": "Moderate weather conditions",
            "April": "Warm weather – stay hydrated",
            "May": "Hot in many regions",
            "June": "Monsoon onset in some areas",
            "July": "Rainy season – carry rain protection",
            "August": "Heavy rainfall in some regions",
            "September": "Post-monsoon freshness",
            "October": "Mild and comfortable weather",
            "November": "Cool and pleasant climate",
            "December": "Winter season – festive period"
        }

    # ------------------ Date Logic ------------------
    def get_month_from_date(self, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%B")

    # ------------------ Season Note ------------------
    def get_season_note(self, month):
        return self.season_notes.get(month, "General travel conditions")

    # ------------------ Internet Cost Fetch ------------------
    def fetch_daily_cost_from_internet(self, place):
        try:
            url = "https://www.numbeo.com/api/cost_of_living_city"
            params = {
                "api_key": NUMBEO_API_KEY,
                "city": place,
                "country": "India"
            }

            response = requests.get(url, timeout=5)
            data = response.json()

            if "prices" in data:
                food = data["prices"].get("meal_inexpensive_restaurant", 300)
                transport = data["prices"].get("one_way_ticket_local_transport", 50)
                hotel_monthly = data["prices"].get(
                    "apartment_1bedroom_city_centre", 2000
                )

                hotel_daily = hotel_monthly / 30
                return int(food + transport + hotel_daily)

        except Exception:
            pass

        return None

    # ------------------ Budget Estimation ------------------
    def estimate_budget(self, place, days):
        daily_cost = self.fetch_daily_cost_from_internet(place)

        if not daily_cost:
            daily_cost = self.india_average_daily_cost

        return {
            "Per Day Estimated Cost (₹)": daily_cost,
            "Total Estimated Cost (₹)": daily_cost * days
        }

    # ------------------ Itinerary ------------------
    def generate_itinerary(self, place, days):
        itinerary = {}
        for day in range(1, days + 1):
            itinerary[f"Day {day}"] = f"Sightseeing and local experiences in {place}"
        return itinerary

    # ------------------ Trip Planner ------------------
    def plan_trip(self, start_date, place, days):
        month = self.get_month_from_date(start_date)

        return {
            "Destination": place,
            "Start Date": start_date,
            "Month": month,
            "Season Note": self.get_season_note(month),
            "Duration": f"{days} days",
            "Budget Estimation": self.estimate_budget(place, days),
            "Itinerary": self.generate_itinerary(place, days)
        }


# ------------------ Customer Input ------------------
if __name__ == "__main__":
    planner = TripPlannerAI()

    start_date = input("Enter trip start date (YYYY-MM-DD): ")
    place = input("Enter destination (City): ")
    days = int(input("Enter number of days: "))

    trip_plan = planner.plan_trip(start_date, place, days)

    print("\n🧳 Trip Plan Summary")
    print("-" * 40)
    for key, value in trip_plan.items():
        print(f"{key}: {value}")
