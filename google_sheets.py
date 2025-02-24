import gspread
from google.oauth2.service_account import Credentials

# Set up Google Sheets API
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
SERVICE_ACCOUNT_FILE = "/home/valery/Documents/Event_Plan/event-planning-450514-7a81bb7afb99.json"

# Authenticate with Google Sheets
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Open the Google Sheet
SHEET_NAME = "Event_Planner"
spreadsheet = client.open(SHEET_NAME)
worksheet = spreadsheet.sheet1  # First sheet

def add_guest(name, phone, status="Pending"):
    """Add a new guest to the Google Sheet."""
    worksheet.append_row([name, phone, status])
    return f"✅ Guest {name} added with phone {phone} (Status: {status})."

def update_rsvp(name, status):
    """Update RSVP status of a guest."""
    data = worksheet.get_all_values()
    for i, row in enumerate(data):
        if row[0].lower() == name.lower():  # Match name (case insensitive)
            worksheet.update(f"C{i+1}", [[status]])  # Update RSVP column
            return f"✅ RSVP status for {name} updated to {status}."
    return f"⚠ Guest {name} not found."

def list_guests():
    """Retrieve and return all guest details."""
    data = worksheet.get_all_values()
    if len(data) > 1:
        return "\n".join([" | ".join(row) for row in data])
    return "⚠ No guests found in the list."

if __name__ == "__main__":
    print("Google Sheets Handler Ready!")

