from backend.db.db import get_db


def fetch_recent_transactions():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT merchant, amount, category, transaction_date
        FROM hist_transactions
        WHERE transaction_date >= CURDATE() - INTERVAL 2 DAY
        ORDER BY transaction_date DESC
        LIMIT 3
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def fetch_personal_details():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT first_name, last_name, dob, mother_maiden_name, first_car_make, first_pet_name 
        FROM personal_details_plaintext
        LIMIT 1
    """)
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def format_personal_details_context(details):
    if not details:
        return ""
    fields = [
        ("First Name", details.get("first_name")),
        ("Last Name", details.get("last_name")),
        ("Date of Birth", str(details.get("dob")) if details.get("dob") else None),
        ("Mother's Maiden Name", details.get("mother_maiden_name")),
        ("First Car Make", details.get("first_car_make")),
        ("First Pet Name", details.get("first_pet_name"))
    ]
    return "\n".join(f"{k}: {v}" for k, v in fields if v is not None and v != "")

def format_personal_details_context(details):
    if not details:
        return ""
    fields = [
        ("First Name", details.get("first_name")),
        ("Last Name", details.get("last_name")),
        ("Date of Birth", str(details.get("dob")) if details.get("dob") else None),
        ("Mother's Maiden Name", details.get("mother_maiden_name")),
        ("First Car Make", details.get("first_car_make")),
        ("First Pet Name", details.get("first_pet_name"))
    ]
    return "\n".join(f"{k}: {v}" for k, v in fields if v is not None and v != "")
