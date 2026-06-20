# MediSafeTracker


MediSafeTracker is a simple desktop medicine reminder app built with Python and Tkinter. It lets you add medicines, track quantity, set expiry dates, and receive alerts for expiring or low-stock medications.

## About

MediSafeTracker helps users manage personal medication information from their desktop. It stores medicine records locally in a CSV file and provides reminders for soon-to-expire and low-stock items.

## Features

- Add medicine details: name, dosage, quantity, expiry date, and description
- View saved medicines in a table
- Delete selected medicines
- Alerts for expiring medicines (within 3 days)
- Alerts for low stock (quantity ≤ 3)

## Requirements

- Python 3
- `tkinter` (usually included with Python)
- `plyer` for desktop notifications

## Install

```bash
python3 -m pip install -r requirements.txt
```

## Run

```bash
python3 MediSafeTracker.py
```

## Usage

1. Enter the medicine information in the form fields.
2. Click **Save Medicine** to store the record in `medicine_data.csv`.
3. Select a medicine row and click **Delete Selected** to remove it.
4. Click **View Medicine** to reload the table.
5. Click **View Summary** for a placeholder summary message.

## Packaging

You can package the app into a standalone executable using PyInstaller. A `MediSafeTracker.spec` file is already included in the repository.

## Notes

- This is a local desktop app, not a website or hosted web service.
- The app stores data in `medicine_data.csv` in the project folder.
- The summary feature is currently a placeholder and can be extended later.
