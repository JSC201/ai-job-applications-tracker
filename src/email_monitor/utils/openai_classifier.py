from openai import OpenAI
import json
from core.config import get_openai_key
from loguru import logger

client = OpenAI(api_key=get_openai_key())

def is_job_related(email):
    prompt = f"""Is this email related to a job application? Reply with only 'yes' or 'no'.

From: {email['from']}
Subject: {email['subject']}
Body: {email['body'][:500]}"""

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0,
        max_tokens=5
    )
    return response.choices[0].message.content.strip().lower() == 'yes'

def classify_email(email):
    prompt = f"""Classify this job application email and return ONLY a JSON object with no markdown:

{{
  "category": "one of: rejection, interview_request, online_assessment, offer, application_confirmation, other",
  "company": "company name if identifiable, otherwise empty string",
  "interview_date": "date and time if interview is mentioned (format: YYYY-MM-DD HH:MM), otherwise empty string",
  "notes": "one sentence summary of the email"
}}

From: {email['from']}
Subject: {email['subject']}
Body: {email['body'][:1500]}"""

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(raw.strip())
