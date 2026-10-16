WasteWise - Food Waste Reduction System
-----------------------------------------
A console-based inventory system that helps track food expiry dates,
warns about items nearing expiry, suggests recipes from a predefined
database based on available (non-expired) ingredients, and estimates
how much food waste (in cost) has been avoided by using items in time.

Concepts used: lists, sorting, date calculations (datetime/timedelta),
and file handling (JSON persistence).
"""

import json
import os
from datetime import datetime, date, timedelta

# ----------------------------------------------------------------------
# Configuration / Data files
# ----------------------------------------------------------------------
INVENTORY_FILE = "inventory.json"
HISTORY_FILE = "history.json"        # tracks items "used" and "wasted"
DATE_FORMAT = "%Y-%m-%d"
NEAR_EXPIRY_DAYS = 3                  # items expiring within this many days are flagged

# A small predefined recipe database: recipe name -> list of required ingredients
RECIPE_DB = {
    "Vegetable Stir Fry": ["carrot", "broccoli", "bell pepper", "onion", "garlic"],
    "Tomato Pasta": ["tomato", "pasta", "garlic", "onion", "basil"],
    "Fruit Salad": ["apple", "banana", "orange", "grapes"],
    "Omelette": ["egg", "onion", "tomato", "cheese"],
    "Vegetable Soup": ["carrot", "potato", "onion", "celery", "tomato"],
    "Grilled Cheese Sandwich": ["bread", "cheese", "butter"],
    "Fried Rice": ["rice", "egg", "carrot", "peas", "onion"],
    "Banana Milkshake": ["milk", "banana", "sugar"],
    "Chicken Curry": ["chicken", "onion", "tomato", "garlic", "ginger"],
    "Egg Sandwich": ["bread", "egg", "cheese", "lettuce"],
}


# ----------------------------------------------------------------------
# Persistence helpers (file handling)
# ----------------------------------------------------------------------
def load_json(filepath):
    """Load a list of dicts from a JSON file. Returns [] if file is missing/empty."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except (json.JSONDecodeError, OSError):
        return []


def save_json(filepath, data):
    """Write a list of dicts to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def load_inventory():
    return load_json(INVENTORY_FILE)


def save_inventory(items):
    save_json(INVENTORY_FILE, items)


def load_history():
    return load_json(HISTORY_FILE)


def save_history(history):
    save_json(HISTORY_FILE, history)


# ----------------------------------------------------------------------
# Date helpers
# ----------------------------------------------------------------------
def parse_date(date_str):
    return datetime.strptime(date_str, DATE_FORMAT).date()


def days_until(expiry_str):
    """Return number of days remaining until expiry (negative if already expired)."""
    expiry = parse_date(expiry_str)
    return (expiry - date.today()).days


def sort_by_expiry(items):
    """Return items sorted ascending by expiry date (soonest first)."""
    return sorted(items, key=lambda item: item["expiry_date"])


# ----------------------------------------------------------------------
# Core features
# ----------------------------------------------------------------------
def add_item():
    """Prompt the user for a new food item and append it to the inventory."""
    items = load_inventory()

    name = input("Food item name: ").strip().lower()
    while not name:
        name = input("Name cannot be empty. Food item name: ").strip().lower()

    while True:
        try:
            quantity = float(input("Quantity (e.g. 2 or 1.5): ").strip())
            break
        except ValueError:
            print("Please enter a valid number.")

    unit = input("Unit (e.g. pcs, kg, liters) [pcs]: ").strip() or "pcs"

    while True:
        expiry_str = input("Expiry date (YYYY-MM-DD): ").strip()
        try:
            parse_date(expiry_str)
            break
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")

    while True:
        price_str = input("Estimated total price for this item [0]: ").strip()
        if price_str == "":
            price = 0.0
            break
        try:
            price = float(price_str)
            break
        except ValueError:
            print("Please enter a valid number.")

    item = {
        "name": name,
        "quantity": quantity,
        "unit": unit,
        "expiry_date": expiry_str,
        "price": price,
        "added_on": date.today().strftime(DATE_FORMAT),
    }
    items.append(item)
    save_inventory(items)
    print(f"Added '{name}' ({quantity} {unit}), expiring {expiry_str}.\n")


def display_items(items=None, header="Current Inventory"):
    """Display all items, sorted by expiry date, with days remaining."""
    if items is None:
        items = load_inventory()
    if not items:
        print("Inventory is empty.\n")
        return

    items = sort_by_expiry(items)
    print(f"\n--- {header} ---")
    print(f"{'#':<3}{'Item':<18}{'Qty':<10}{'Expiry':<12}{'Status':<15}")
    print("-" * 58)
    for i, item in enumerate(items, start=1):
        remaining = days_until(item["expiry_date"])
        if remaining < 0:
            status = f"EXPIRED ({-remaining}d ago)"
        elif remaining <= NEAR_EXPIRY_DAYS:
            status = f"Near expiry ({remaining}d left)"
        else:
            status = f"OK ({remaining}d left)"
        qty_str = f"{item['quantity']} {item['unit']}"
        print(f"{i:<3}{item['name']:<18}{qty_str:<10}{item['expiry_date']:<12}{status:<15}")
    print()


def items_near_expiry(items=None, days=NEAR_EXPIRY_DAYS):
    """Return items expiring within `days` days (not yet expired)."""
    if items is None:
        items = load_inventory()
    near = [i for i in items if 0 <= days_until(i["expiry_date"]) <= days]
    return sort_by_expiry(near)


def expired_items(items=None):
    if items is None:
        items = load_inventory()
    return [i for i in items if days_until(i["expiry_date"]) < 0]


def suggest_recipes():
    """Suggest recipes from RECIPE_DB based on non-expired ingredients on hand,
    prioritizing recipes that use ingredients nearing expiry."""
    items = load_inventory()
    available = {i["name"] for i in items if days_until(i["expiry_date"]) >= 0}
    near_expiry_names = {i["name"] for i in items_near_expiry(items)}

    if not available:
        print("No available (non-expired) ingredients to suggest recipes from.\n")
        return

    results = []
    for recipe, required in RECIPE_DB.items():
        required_set = set(required)
        have = required_set & available
        missing = required_set - available
        match_ratio = len(have) / len(required_set)
        uses_urgent = bool(have & near_expiry_names)
        if match_ratio > 0:
            results.append((recipe, match_ratio, have, missing, uses_urgent))

    if not results:
        print("No matching recipes found for your current ingredients.\n")
        return

    # Sort by: uses ingredients near expiry first, then by highest match ratio
    results.sort(key=lambda r: (not r[4], -r[1]))

    print("\n--- Suggested Recipes ---")
    for recipe, ratio, have, missing, urgent in results[:6]:
        tag = " [uses items nearing expiry!]" if urgent else ""
        print(f"* {recipe} - {ratio*100:.0f}% match{tag}")
        print(f"    Have: {', '.join(sorted(have))}")
        if missing:
            print(f"    Missing: {', '.join(sorted(missing))}")
    print()


def mark_item_used(index=None):
    """Mark an item as used (consumed) before it expired, logging waste avoided."""
    items = load_inventory()
    sorted_items = sort_by_expiry(items)
    if not sorted_items:
        print("Inventory is empty.\n")
        return

    if index is None:
        display_items(items, header="Select an item to mark as used")
        try:
            choice = int(input("Enter item number to mark as used: ").strip())
            index = choice - 1
        except ValueError:
            print("Invalid input.\n")
            return

    if index < 0 or index >= len(sorted_items):
        print("Invalid item number.\n")
        return

    used_item = sorted_items[index]
    remaining_days = days_until(used_item["expiry_date"])
    outcome = "used_before_expiry" if remaining_days >= 0 else "used_after_expiry"

    history = load_history()
    history.append({
        "name": used_item["name"],
        "quantity": used_item["quantity"],
        "unit": used_item["unit"],
        "price": used_item.get("price", 0.0),
        "expiry_date": used_item["expiry_date"],
        "action_date": date.today().strftime(DATE_FORMAT),
        "outcome": outcome,
    })
    save_history(history)

    # Remove the used item from inventory (delete first exact match)
    for idx, i in enumerate(items):
        if i == used_item:
            del items[idx]
            break
    save_inventory(items)
    print(f"Marked '{used_item['name']}' as used. Waste avoided!\n" if remaining_days >= 0
          else f"'{used_item['name']}' was used after its expiry date.\n")


def remove_expired_items():
    """Move all expired items from inventory into history as 'wasted', then delete them."""
    items = load_inventory()
    expired = expired_items(items)
    if not expired:
        print("No expired items to remove.\n")
        return

    history = load_history()
    for item in expired:
        history.append({
            "name": item["name"],
            "quantity": item["quantity"],
            "unit": item["unit"],
            "price": item.get("price", 0.0),
            "expiry_date": item["expiry_date"],
            "action_date": date.today().strftime(DATE_FORMAT),
            "outcome": "wasted",
        })
    save_history(history)

    remaining = [i for i in items if days_until(i["expiry_date"]) >= 0]
    save_inventory(remaining)
    print(f"Removed {len(expired)} expired item(s) and logged them as wasted.\n")


def calculate_waste_avoided():
    """Summarize how much food (and estimated cost) was saved vs. wasted."""
    history = load_history()
    if not history:
        print("No usage history yet. Mark items as used or remove expired ones to build history.\n")
        return

    saved_count = sum(1 for h in history if h["outcome"] == "used_before_expiry")
    saved_value = sum(h["price"] for h in history if h["outcome"] == "used_before_expiry")

    wasted_count = sum(1 for h in history if h["outcome"] == "wasted")
    wasted_value = sum(h["price"] for h in history if h["outcome"] == "wasted")

    late_count = sum(1 for h in history if h["outcome"] == "used_after_expiry")

    total_handled = saved_count + wasted_count + late_count
    avoid_rate = (saved_count / total_handled * 100) if total_handled else 0

    print("\n--- Waste Avoided Summary ---")
    print(f"Items used before expiry : {saved_count}  (value saved: ${saved_value:.2f})")
    print(f"Items used after expiry  : {late_count}")
    print(f"Items wasted (expired)   : {wasted_count}  (value lost: ${wasted_value:.2f})")
    print(f"Waste-avoidance rate     : {avoid_rate:.1f}%")
    print(f"Estimated net savings    : ${saved_value - wasted_value:.2f}\n")


# ----------------------------------------------------------------------
# CLI Menu
# ----------------------------------------------------------------------
def print_menu():
    print("=" * 42)
    print("        WASTEWISE - Food Waste Tracker")
    print("=" * 42)
    print("1. Add a food item")
    print("2. View all inventory (sorted by expiry)")
    print("3. View items nearing expiry")
    print("4. Suggest recipes from available ingredients")
    print("5. Mark an item as used")
    print("6. Remove expired items (log as wasted)")
    print("7. View waste-avoided summary")
    print("8. Exit")
    print("=" * 42)


def main():
    while True:
        print_menu()
        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            add_item()
        elif choice == "2":
            display_items()
        elif choice == "3":
            near = items_near_expiry()
            if near:
                display_items(near, header=f"Items Expiring Within {NEAR_EXPIRY_DAYS} Days")
            else:
                print("No items are nearing expiry.\n")
        elif choice == "4":
            suggest_recipes()
        elif choice == "5":
            mark_item_used()
        elif choice == "6":
            remove_expired_items()
        elif choice == "7":
            calculate_waste_avoided()
        elif choice == "8":
            print("Goodbye! Keep reducing that food waste.")
            break
        else:
            print("Invalid option, please choose between 1 and 8.\n")


if __name__ == "__main__":
    main()
