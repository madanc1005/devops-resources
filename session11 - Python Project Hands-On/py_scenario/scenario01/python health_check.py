import requests
import csv
from datetime import datetime
import time
import os


def check_web_service(url):
    """Check the health of a web service."""
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        end_time = time.time()

        response_time = end_time - start_time
        status_code = response.status_code

        if status_code == 200:
            return "UP", status_code, f"{response_time:.2f}"
        else:
            return "DOWN", status_code, f"{response_time:.2f}"

    except requests.exceptions.RequestException as e:
        return "ERROR", str(e), "N/A"


def main():
    """Read URLs, check services, and generate a report."""

    input_csv_file = "web_services.csv"
    output_csv_file = "health_check_report.csv"

    if not os.path.exists(input_csv_file):
        print(f"Error: Input CSV file '{input_csv_file}' not found.")
        return

    web_services = []

    try:
        with open(input_csv_file, "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)

            for row in reader:
                if row and row[0].strip():
                    web_services.append(row[0].strip())

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    report_data = [
        ["Timestamp", "URL", "Status", "Status Code", "Response Time (s)"]
    ]

    for url in web_services:
        status, code, response_time = check_web_service(url)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report_data.append(
            [timestamp, url, status, code, response_time]
        )

        print(
            f"Checked {url}: Status={status}, "
            f"Code={code}, Response Time={response_time}s"
        )

        time.sleep(1)

    try:
        with open(output_csv_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(report_data)

        print(f"Health check report written to '{output_csv_file}'")

    except Exception as e:
        print(f"Error writing to CSV file: {e}")


if __name__ == "__main__":
    main()