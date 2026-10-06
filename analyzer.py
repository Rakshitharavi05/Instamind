from google import genai
import os
import json


# Connect to Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_ai_analysis(business):

    prompt = f"""
You are an AI business intelligence analyst.

Analyze this business:

Business name: {business["business_name"]}
Category: {business["category"]}
Location: {business["location"]}
Business type: {business["business_type"]}
Description: {business["description"]}
Services: {", ".join(business["services"])}
Target audience: {", ".join(business["target_audience"])}

Return ONLY valid JSON in exactly this format:

{{
    "content_themes": [
        {{
            "theme": "string",
            "percentage": 0
        }},
        {{
            "theme": "string",
            "percentage": 0
        }},
        {{
            "theme": "string",
            "percentage": 0
        }},
        {{
            "theme": "string",
            "percentage": 0
        }}
    ],
    "brand_personality": "string",
    "ai_insight": "string",
    "recommendations": [
        "string",
        "string",
        "string"
    ]
}}

Rules:
- Give exactly 4 content themes.
- Percentages must add up to 100.
- Give exactly 3 recommendations.
- Make the recommendations practical.
- Do not use markdown.
- Return JSON only.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    # Remove possible markdown code fences
    response_text = response.text.strip()

    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

    return json.loads(response_text)


def load_business_data():

    data_path = os.path.join(
        os.path.dirname(__file__),
        "data.json"
    )

    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


def analyze_profile(url):

    url_lower = url.lower()

    businesses = load_business_data()

    selected_business = None

    # Find matching business
    for business in businesses:

        if business["username"] in url_lower:
            selected_business = business
            break

    # If no business matches, use the first profile
    if selected_business is None:
        selected_business = businesses[0]

    # Send business information to Gemini
    ai_result = generate_ai_analysis(selected_business)

    return {

        "profile_url": url,

        "business_name": selected_business["business_name"],

        "category": selected_business["category"],

        "location": selected_business["location"],

        "business_type": selected_business["business_type"],

        "description": selected_business["description"],

        "services": selected_business["services"],

        "target_audience": selected_business["target_audience"],

        "content_themes": ai_result["content_themes"],

        "brand_personality": ai_result["brand_personality"],

        "ai_insight": ai_result["ai_insight"],

        "recommendations": ai_result["recommendations"]
    }