from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.transaction_model import Transaction

suspicious_reasons = []

def is_suspicious(transaction, db: Session):
    """
    Simple rule-based anomaly detection.
    Returns (is_suspicious: bool, reason: str)
    """

    user_transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == transaction.user_id)
        .order_by(Transaction.tx_date.desc())
        .all()
    )

    if user_transactions:
        avg_amount = sum(tx.amount for tx in user_transactions) / len(user_transactions)
        home_country = user_transactions[0].country
    else:
        avg_amount = 0
        home_country = None

    # 1. High-value or abnormal amount
    if transaction.amount > 5000:
        suspicious_reasons.append(f"High transaction amount ({transaction.amount}) exceeds safe limit.")
    elif avg_amount > 0 and transaction.amount > 3 * avg_amount:
        suspicious_reasons.append(
            f"Amount ({transaction.amount}) much higher than user’s usual spending (avg {avg_amount:.2f})."
        )

    # 2. Unusual transaction timing
    hour = getattr(transaction.tx_date, "hour", datetime.now().hour)
    if hour < 5 or hour > 23:
        suspicious_reasons.append(f"Transaction made at unusual hour ({hour}:00).")

    # 3. Location anomaly
    if home_country and transaction.country and home_country != transaction.country:
        suspicious_reasons.append(
            f"Transaction from different country ({transaction.country}) vs user's home ({home_country})."
        )


    # 4. Frequency spike (too many recent transactions)
    ten_minutes_ago = transaction.tx_date - timedelta(minutes=10)
    recent_txns = (
        db.query(Transaction)
        .filter(Transaction.user_id == transaction.user_id)
        .filter(Transaction.tx_date >= ten_minutes_ago)
        .filter(Transaction.tx_date < transaction.tx_date)
        .all()
    )
    if len(recent_txns) >= 5:
        suspicious_reasons.append(f"Unusual burst: {len(recent_txns)} transactions in 10 minutes.")


    high_risk_categories = ["crypto", "gambling", "giftcards", "electronics"]
    if getattr(transaction, "category", "").lower() in high_risk_categories:
        suspicious_reasons.append(f"High-risk merchant category: {transaction.category}.")

        
    # Final decision
    if suspicious_reasons:
        return True, "; ".join(suspicious_reasons)
    return False, "Transaction appears normal"
