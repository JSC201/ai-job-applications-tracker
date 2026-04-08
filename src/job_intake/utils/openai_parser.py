from openai import OpenAI
import json
from core.config import get_openai_key
from loguru import logger

client = OpenAI(api_key=get_openai_key())

def extract_job_fields(text):
    prompt = f"""Extract the following fields from this job posting and return ONLY a JSON object with no markdown or extra text.

For summary: write 2-3 sentences covering what this job is about, what the person in this role will actually be doing day-to-day, and what matters most about this specific role. Be specific to this role and company — no generic filler.

For requirements: organize into three clear categories — what is necessary to be considered for the role, what is nice to have but not required, and anything unique or notable that stands out about what this company is specifically looking for. Return as a plain text string in this format: "Necessary: [list]. Nice-to-have: [list]. Notable: [list]."

{{
  "company": "company name",
  "title": "job title",
  "location": "city, state",
  "work_type": "one of: Remote, Hybrid, On-site, or empty string if unclear",
  "salary": "salary or OTE range, or empty string if not listed",
  "date_posted": "date the job was posted if mentioned, otherwise empty string",
  "job_post_id": "job posting ID if present in the text or URL, otherwise empty string",
  "source": "platform derived from URL (e.g. LinkedIn, Handshake, Indeed, Company Site), or empty string if unclear",
  "recruiter": "name of recruiter or hiring manager if mentioned anywhere in the posting, otherwise empty string",
  "url": "job url if present in the text, otherwise empty string",
  "summary": "detailed role summary as described above",
  "requirements": "detailed key requirements as described above"
}}

Job posting:
{text}"""

    logger.info("Sending job posting to OpenAI for parsing")
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(raw.strip())
