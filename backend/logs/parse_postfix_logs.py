import re
import datetime
from sqlalchemy.orm import Session
from app.models.correct_deliveries import CorrectDelivery
from app.models.failed_deliveries import FailedDelivery
from app.core.database import get_db

LOG_FILE_PATH = "/path/to/your/postfix.log"


def parse_log_line(line):
    timestamp = extract_timestamp(line)

    if "status=sent" in line:
        from_address, to_address = extract_addresses(line)
        return CorrectDelivery(
            timestamp=timestamp,
            from_address=from_address,
            to_address=to_address,
            status="Sent",
        )

    if "reject:" in line:
        from_address, to_address, reason = extract_rejection_data(line)
        return FailedDelivery(
            timestamp=timestamp,
            from_address=from_address,
            to_address=to_address,
            status="Rejected",
            reason=reason,
        )


def extract_timestamp(line):
    match = re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", line)
    return datetime.datetime.fromisoformat(match.group()) if match else None


def extract_addresses(line):
    from_match = re.search(r"from=<([^>]+)>", line)
    to_match = re.search(r"to=<([^>]+)>", line)
    return (
        from_match.group(1) if from_match else None,
        to_match.group(1) if to_match else None,
    )


def extract_rejection_data(line):
    from_address, to_address = extract_addresses(line)
    reason_match = re.search(
        r"reject: RCPT from [^:]+: \d{3} [\d.]+ <[^>]+>: (.+); from=", line
    )
    reason = reason_match.group(1) if reason_match else "Unknown reason"
    return from_address, to_address, reason


def process_log_file():
    with open(LOG_FILE_PATH, "r+") as file:
        lines = file.readlines()
        db = next(get_db())
        for line in lines:
            record = parse_log_line(line)
            if record:
                db.add(record)
        db.commit()
        # Truncate the file after processing
        file.truncate(0)


if __name__ == "__main__":
    process_log_file()
