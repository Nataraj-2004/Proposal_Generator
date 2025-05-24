# project_lists.py

import os
import json
import openai
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def build_prompt(
    current_project: str, 
    past_projects: List[Dict[str, str]]
) -> str:
    """
    Build a prompt to have the model:
    1. Score each past project for relevancy to the current project (0–100).
    2. Provide brief rationale for each score.
    3. Suggest 3 additional project ideas that would strengthen the proposal.
    """

    project_list_text = "\n".join(
        [f"{i+1}. Title: {p['title']}\n   Description: {p['description']}"
         for i, p in enumerate(past_projects)]
    )

    prompt = f"""
You are a proposal analyst. Given the current project and a list of past projects, do the following:

1. For each past project, rate its relevancy to the CURRENT PROJECT on a scale of 0–100.
2. Provide a one-sentence rationale for each rating.
3. Suggest three additional project ideas or case studies (title + one-line description) that would strengthen our proposal.

Use this format in JSON (no extra text):
{{
  "evaluations": [
    {{
      "title": "Project Title",
      "score": 0–100,
      "rationale": "One sentence justification"
    }},
    ...
  ],
  "additional_recommendations": [
    {{
      "title": "Recommended Project Title",
      "description": "One-line description"
    }},
    ...
  ]
}}

CURRENT PROJECT:
\"\"\"{current_project}\"\"\"

PAST PROJECTS:
{project_list_text}
"""
    return prompt.strip()


def generate_project_list(
    current_project: str,
    past_projects: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    Call OpenAI API to evaluate and enhance the project list.

    Parameters:
    - current_project: Description of the current project.
    - past_projects: List of dicts [{ "title": str, "description": str }, ...].

    Returns:
    A dict with keys:
      - "evaluations": List of {title, score, rationale}
      - "additional_recommendations": List of {title, description}
    """

    prompt = build_prompt(current_project, past_projects)

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You analyze project relevancy and suggest improvements."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=600,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        content = resp.choices[0].message.content.strip()

        # Parse JSON out of the response
        data = json.loads(content)
        return data

    except json.JSONDecodeError as je:
        raise ValueError(f"Failed to parse JSON from model response: {je}\nRaw response:\n{content}")
    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {e}")


if __name__ == "__main__":
    # === Manual Test ===
    current = "Implementation of AI-based water conservation and distribution systems."
    past = [
        {
            "title": "Urban Smart Grid Deployment",
            "description": "Developed a city-wide smart grid to optimize energy consumption."
        },
        {
            "title": "IoT Environmental Monitoring",
            "description": "Built an IoT network to track air and water quality in real time."
        },
        {
            "title": "Rural Solar Expansion",
            "description": "Expanded solar panel installations in rural communities."
        }
    ]

    results = generate_project_list(current, past)
    print(json.dumps(results, indent=2, ensure_ascii=False))
