import re
import datetime
from sqlalchemy.orm import Session
from app.models.correct_deliveries import CorrectDelivery
from app.models.failed_deliveries import FailedDelivery
from app.core.database import get_db

LOG_FILE_PATH = "logs/postfix.log"


def parse_log_lines(lines):
    queued_emails = {}

    for line in lines:
        if "postfix/qmgr" in line:
            queued_email = extract_queued_email(line)
            if queued_email:
                queued_emails[queued_email["id"]] = queued_email

        elif "postfix/smtp" in line and "status=sent" in line:
            sent_email = extract_sent_email(line, queued_emails)
            if sent_email:
                yield CorrectDelivery(**sent_email)

        elif "postfix/smtpd" in line and "reject:" in line:
            failed_email = extract_failed_email(line)
            if failed_email:
                yield FailedDelivery(**failed_email)


def extract_queued_email(line):
    pattern = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).*postfix/qmgr\[\d+\]: (\w+): from=<([^>]+)>,"
    match = re.search(pattern, line)
    if match:
        timestamp, email_id, from_address = match.groups()
        return {
            "id": email_id,
            "from_address": from_address,
            "timestamp": datetime.datetime.fromisoformat(timestamp),
        }


def extract_failed_email(line):
    pattern = (
        r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).*postfix/smtpd\[\d+\]: NOQUEUE: reject: "
        r"RCPT from .*: (\d{3} \d\.\d\.\d) <([^>]+)>: Recipient address rejected: "
        r"(User unknown in virtual alias table|Access denied); from=<([^>]+)> to=<([^>]+)>"
    )
    match = re.search(pattern, line)
    if match:
        (
            timestamp,
            error_code,
            rejected_address,
            error_message,
            from_address,
            to_address,
        ) = match.groups()
        reason = (
            "Disabled"
            if "User unknown in virtual alias table" in error_message
            else "Does Not Exist"
        )
        return {
            "timestamp": datetime.datetime.fromisoformat(timestamp),
            "from_address": from_address,
            "to_address": to_address,
            "status": "Rejected",
            "reason": reason,
        }


def extract_sent_email(line, queued_emails):
    pattern = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).*postfix/smtp\[\d+\]: (\w+): to=<([^>]+)>, orig_to=<([^>]+)>,"
    match = re.search(pattern, line)
    if match:
        timestamp, email_id, to_address, orig_to = match.groups()
        if email_id in queued_emails:
            queued_email = queued_emails[email_id]
            return {
                "timestamp": queued_email["timestamp"],
                "from_address": queued_email["from_address"],
                "to_address": orig_to,
                "status": "Sent",
            }


def process_log_file():
    with open(LOG_FILE_PATH, "r+") as file:
        lines = file.readlines()
        db = next(get_db())
        for record in parse_log_lines(lines):
            db.add(record)
        db.commit()
        file.truncate(0)


if __name__ == "__main__":
    process_log_file()
