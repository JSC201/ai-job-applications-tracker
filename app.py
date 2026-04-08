from flask import Flask, render_template, request, redirect, url_for, flash
from core.config import load_config
from loguru import logger
from src.job_intake.handlers.parse_job import parse_job_posting
from src.job_intake.handlers.write_to_sheet import get_or_create_sheet, add_job

app = Flask(__name__)
app.secret_key = 'job-tracker-secret'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse():
    text = request.form.get('job_text', '').strip()
    if not text:
        flash('Please paste a job posting.')
        return redirect(url_for('index'))
    try:
        job = parse_job_posting(text)
        return render_template('confirm.html', job=job)
    except Exception as e:
        logger.error(f"Parsing failed: {e}")
        flash('Failed to parse job posting. Please try again.')
        return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add():
    job = {
        'company':      request.form.get('company', ''),
        'title':        request.form.get('title', ''),
        'location':     request.form.get('location', ''),
        'salary':       request.form.get('salary', ''),
        'url':          request.form.get('url', ''),
        'summary':      request.form.get('summary', ''),
        'requirements': request.form.get('requirements', ''),
        'date_applied': request.form.get('date_applied', ''),
        'status':       'Applied',
        'notes':        '',
    }
    try:
        config = load_config()
        sheet_id = get_or_create_sheet(config)
        add_job(sheet_id, job)
        logger.info(f"Added: {job['title']} at {job['company']}")
        flash(f"Added {job['title']} at {job['company']} to your tracker.")
    except Exception as e:
        logger.error(f"Failed to add job: {e}")
        flash('Failed to add job to sheet. Please try again.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
