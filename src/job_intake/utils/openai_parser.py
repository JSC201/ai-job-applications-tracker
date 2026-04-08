from openai import OpenAI
import json
from core.config import get_openai_key
from loguru import logger

client = OpenAI(api_key=get_openai_key())

def extract_job_fields(text):
    prompt = f"""Extract the following fields from this job posting and return ONLY a JSON object with no markdown or extra text:

{{
  "company": "company name",
  "title": "job title",
  "location": "city, state or Remote",
  "salary": "salary range or empty string if not listed",
  "url": "job url if present in the text, otherwise empty string",
  "summary": "2-3 sentence summary of the role",
  "requirements": "top 3-5 key requirements as a comma-separated string"
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
