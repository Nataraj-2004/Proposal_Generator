import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Please set GEMINI_API_KEY in your environment or .env file")

# Configure the Gemini client
genai.configure(api_key=GEMINI_API_KEY)


def get_language_legal_templates(language: str):
    """
    Return template instructions for legal docs in different languages.
    """
    language = language.lower()
    templates = {
        "english": {
            "power_of_attorney": """
You are a legal document assistant.

Generate a formal, clear, and professional Power of Attorney document.

- Include the parties' full names and roles.
- Specify the authority granted clearly.
- Use formal legal language.
- Include date and place placeholders.
- The tone should be respectful, precise, and legally binding.
""",
            "letter_of_association": """
You are a legal document assistant.

Generate a formal Letter of Association for a consortium of firms joining for a project.

- List all participating firms with roles.
- Specify the purpose of association.
- Include obligations and collaboration terms briefly.
- Use formal legal language.
- Include date and place placeholders.
"""
        },
        "portuguese": {
            "power_of_attorney": """
Você é um assistente de documentos legais.

Gere uma procuração formal, clara e profissional.

- Inclua os nomes completos das partes e seus papéis.
- Especifique claramente os poderes concedidos.
- Use linguagem jurídica formal.
- Inclua espaços para data e local.
- O tom deve ser respeitoso, preciso e juridicamente vinculativo.
""",
            "letter_of_association": """
Você é um assistente de documentos legais.

Gere uma Carta de Associação formal para um consórcio de empresas que se unem para um projeto.

- Liste todas as empresas participantes com seus papéis.
- Especifique o propósito da associação.
- Inclua brevemente obrigações e termos de colaboração.
- Use linguagem jurídica formal.
- Inclua espaços para data e local.
"""
        },
        "spanish": {
            "power_of_attorney": """
Eres un asistente de documentos legales.

Genera un poder notarial formal, claro y profesional.

- Incluye los nombres completos de las partes y sus roles.
- Especifica claramente la autoridad otorgada.
- Usa lenguaje legal formal.
- Incluye espacios para fecha y lugar.
- El tono debe ser respetuoso, preciso y legalmente vinculante.
""",
            "letter_of_association": """
Eres un asistente de documentos legales.

Genera una Carta de Asociación formal para un consorcio de empresas que se unen para un proyecto.

- Enumera todas las empresas participantes con roles.
- Especifica el propósito de la asociación.
- Incluye brevemente las obligaciones y términos de colaboración.
- Usa lenguaje legal formal.
- Incluye espacios para fecha y lugar.
"""
        },
    }
    return templates.get(language, templates["english"])


def build_prompt(doc_type, parties, project_name, language="english"):
    """
    Build prompt for Power of Attorney or Letter of Association.
    parties: list of dicts with keys 'name' and 'role'
    """
    language_templates = get_language_legal_templates(language)

    if doc_type == "power_of_attorney":
        instructions = language_templates["power_of_attorney"]
        prompt = f"""
{instructions}

Project Name: {project_name}

Principal: {parties[0]['name']} ({parties[0]['role']})
Attorney-in-fact: {parties[1]['name']} ({parties[1]['role']})

Generate the full legal Power of Attorney document below:
"""
    elif doc_type == "letter_of_association":
        instructions = language_templates["letter_of_association"]
        firms_list = "\n".join([f"- {p['name']} ({p['role']})" for p in parties])
        prompt = f"""
{instructions}

Project Name: {project_name}

Participating Firms:
{firms_list}

Generate the full legal Letter of Association document below:
"""
    else:
        raise ValueError("Unsupported document type")

    return prompt.strip()


def generate_legal_document(doc_type, parties, project_name, language="english"):
    """
    Generate legal document text using Gemini 1.5 Flash model.
    doc_type: 'power_of_attorney' or 'letter_of_association'
    parties: list of dicts [{'name': ..., 'role': ...}, ...]
    """
    prompt = build_prompt(doc_type, parties, project_name, language)

    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating legal document: {str(e)}"


# Example manual test
if __name__ == "__main__":
    power_of_attorney_parties = [
        {"name": "John Doe", "role": "Principal"},
        {"name": "Jane Smith", "role": "Attorney-in-fact"}
    ]
    letter_of_association_parties = [
        {"name": "Alpha Consulting", "role": "Lead Firm"},
        {"name": "Beta Engineering", "role": "Partner"},
        {"name": "Gamma Solutions", "role": "Partner"}
    ]

    print("=== Power of Attorney ===\n")
    poa = generate_legal_document(
        "power_of_attorney",
        power_of_attorney_parties,
        "Renewable Energy Project",
        language="english"
    )
    print(poa)

    print("\n=== Letter of Association ===\n")
    loa = generate_legal_document(
        "letter_of_association",
        letter_of_association_parties,
        "Renewable Energy Project",
        language="english"
    )
    print(loa)
