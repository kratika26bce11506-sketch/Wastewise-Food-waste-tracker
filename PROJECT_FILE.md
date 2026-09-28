# WasteWise Project Documentation

## Introduction

WasteWise is a household inventory management system focused on reducing food waste.

The application combines inventory tracking with expiry monitoring and recipe recommendations.

---

## Workflow

### Step 1

User adds food item.

### Step 2

System stores item in inventory.json.

### Step 3

System sorts inventory.

### Step 4

Near-expiry items are highlighted.

### Step 5

Recipes are suggested.

### Step 6

User marks food as used.

### Step 7

History is stored.

### Step 8

Waste summary is generated.

---

## Files Used

### wastewise.py

Main application.

### inventory.json

Stores active inventory.

Example

```json
[
  {
    "name":"milk",
    "quantity":1,
    "unit":"litre",
    "expiry_date":"2026-09-30",
    "price":60
  }
]
```

### history.json

Stores used and wasted items.

---

## Important Functions

| Function                  | Purpose         |
| ------------------------- | --------------- |
| load_json()               | Read JSON       |
| save_json()               | Save JSON       |
| add_item()                | Add inventory   |
| display_items()           | Show inventory  |
| items_near_expiry()       | Alerts          |
| suggest_recipes()         | Recommendations |
| mark_item_used()          | Consumption     |
| remove_expired_items()    | Cleanup         |
| calculate_waste_avoided() | Analytics       |

---

## Python Concepts Demonstrated

* Functions
* Lists
* Dictionaries
* JSON
* File Handling
* Sorting
* Date Operations
* Loops
* Conditions

---

## Sample Output

```text
WasteWise

1 Add Item
2 View Inventory
3 Near Expiry
4 Recipe Suggestions
5 Mark Used
6 Remove Expired
7 Summary
8 Exit
```

---

## Learning Outcomes

Students learn practical implementation of Python through a real-world sustainability application.
