from openai import OpenAI
import json
from core.config import get_openai_key
from loguru import logger

client = OpenAI(api_key=get_openai_key())

def extract_job_fields(text):
    prompt = f"""Extract the following fields from this job posting and return ONLY a JSON object with no markdown or extra text.

For summary: write a detailed, specific summary of the role. Include what makes this role and company unique, key responsibilities, team context, and what kind of candidate they are looking for. Do not copy the posting — synthesize it. Be thorough, no length limit.

For requirements: extract the key requirements that stand out for this specific role. Include must-haves, preferred skills, and anything unique or notable. Be specific and detailed, not a generic list.

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
