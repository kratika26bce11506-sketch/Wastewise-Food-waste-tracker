# WasteWise Project Report

## Title

WasteWise: Food Waste Reduction System

## Abstract

WasteWise is a Python application designed to reduce household food waste by tracking inventory, monitoring expiry dates, recommending recipes, and calculating waste savings.

The system stores data using JSON files and provides an easy-to-use console interface.

---

## Objectives

* Reduce food wastage.
* Monitor food expiry dates.
* Suggest recipes.
* Calculate money saved.
* Practice Python programming concepts.

---

## Problem Statement

Households frequently waste food because expiry dates are overlooked.

WasteWise addresses this by organizing food inventory and providing timely reminders.

---

## Technologies Used

| Technology    | Purpose           |
| ------------- | ----------------- |
| Python        | Programming       |
| JSON          | Data Storage      |
| datetime      | Date Calculations |
| File Handling | Persistence       |

---

## Modules

### 1. Inventory Management

Users can:

* Add items
* Store quantity
* Store unit
* Store expiry date
* Store estimated price

### 2. Expiry Tracking

The system calculates remaining days before expiry and classifies items as:

* OK
* Near Expiry
* Expired

### 3. Recipe Recommendation

A predefined recipe database compares available ingredients and suggests matching recipes.

### 4. Waste Tracking

Users can:

* Mark items as used
* Remove expired items
* Generate savings reports

---

## Data Flow

User Input

↓

Inventory Storage (JSON)

↓

Expiry Analysis

↓

Recipe Engine

↓

Waste Analytics

---

## Algorithm

1. Load inventory.
2. Accept user input.
3. Save data.
4. Sort by expiry.
5. Detect near-expiry items.
6. Recommend recipes.
7. Log used/wasted items.
8. Calculate savings.

---

## Advantages

* Easy to use
* Offline
* Lightweight
* Educational
* Real-world application

---

## Limitations

* Console only
* Manual data entry
* Limited recipe database
* No barcode scanner

---

## Future Scope

* AI recommendations
* Barcode scanning
* OCR receipt scanning
* Cloud synchronization
* Mobile application

---

## Conclusion

WasteWise demonstrates practical use of Python programming while solving a real-world sustainability problem.
