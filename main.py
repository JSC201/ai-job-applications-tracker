from core.config import load_config
from loguru import logger
from src.parser.handler import parse_job_posting
from src.tracker.handler import get_or_create_sheet, add_job



def add_job_flow(config):
    print("\nPaste the job posting below (URL and/or full description).")
    print("When done, type END on a new line and press Enter:\n")
    lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        lines.append(line)
    text = '\n'.join(lines)
    if not text.strip():
        logger.warning("No content entered")
        return
    job = parse_job_posting(text)
    print(f"\nExtracted:")
    print(f"  Company:      {job['company']}")
    print(f"  Title:        {job['title']}")
    print(f"  Location:     {job['location']}")
    print(f"  Salary:       {job['salary'] or 'Not listed'}")
    print(f"  Date Applied: {job['date_applied']}")
    confirm = input("\nLook good? Add to sheet? (y/n): ").strip().lower()
    if confirm == 'y':
        sheet_id = get_or_create_sheet(config)
        add_job(sheet_id, job)
        print("Added to your job tracker.")
    else:
        logger.info("Job discarded by user")

def main():
    config = load_config()
    while True:
        print("\n--- Job Tracker ---")
        print("1. Add a job application")
        print("2. Open tracker sheet")
        print("3. Exit")
        choice = input("\nChoice: ").strip()
        if choice == '1':
            add_job_flow(config)
        elif choice == '2':
            sheet_id = get_or_create_sheet(config)
            print(f"\nhttps://docs.google.com/spreadsheets/d/{sheet_id}")
        elif choice == '3':
            break

if __name__ == '__main__':
    main()
