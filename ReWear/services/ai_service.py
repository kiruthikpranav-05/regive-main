import json
import os

from google import genai


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_bulk_donation(description):
    """
    Analyze a donor's bulk donation description
    and convert it into structured donation items.
    """

    prompt = f"""
You are an AI assistant for ReWear, a donation
management platform.

Analyze the donor's donation description and extract
each individual type of donated item.

For every item, determine:

- name
- category
- quantity
- condition

Allowed categories:
- clothing
- footwear
- bedding
- accessories
- children's_items
- household
- other

Allowed conditions:
- new
- excellent
- good
- fair
- poor
- unknown

Rules:
1. Never invent quantities.
2. If the quantity is not provided, use 1 only when
   the donor clearly describes a single item.
3. If condition is not provided, use "unknown".
4. Keep different types of items separate.
5. Return ONLY valid JSON.
6. The JSON must contain an "items" array.

Example format:

{{
    "items": [
        {{
            "name": "shirts",
            "category": "clothing",
            "quantity": 20,
            "condition": "good"
        }}
    ]
}}

Donor description:
{description}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        raise ValueError("AI returned invalid JSON")