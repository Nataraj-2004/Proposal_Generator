import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

SUPPORTED_LANGUAGES = ["english", "portuguese", "spanish"]


def get_language_profile_templates(language: str):
    """
    Return example and instruction templates for company profiles
    in the specified language. Defaults to English.
    """
    language = language.lower()
    templates = {
        "english": {
            "example": """
Example Company Profile:

**Alpha Consulting**
Alpha Consulting is a leading engineering firm with over 20 years of experience in infrastructure development.
Key Strengths:
- Expertise in smart city solutions
- ISO 9001 and ISO 14001 certified
- Proven track record with 50+ projects completed in 10 countries

Contact: contact@alphaconsulting.com | +1-555-1234
""",
            "instructions": """
You are an expert technical writer. Generate a concise, engaging company profile section for a proposal.

- Use the English language.
- Include company name, core competencies, certifications, and notable achievements.
- Highlight relevance to the current project.
- Keep it under 200 words.
- Format with headings and bullet points for clarity.
"""
        },
        "portuguese": {
            "example": """
Exemplo de Perfil da Empresa:

**Alpha Consulting**
A Alpha Consulting é uma empresa líder em engenharia com mais de 20 anos de experiência em desenvolvimento de infraestrutura.
Principais Pontos Fortes:
- Especialização em soluções de cidades inteligentes
- Certificações ISO 9001 e ISO 14001
- Histórico comprovado com mais de 50 projetos concluídos em 10 países

Contato: contato@alphaconsulting.com | +55-11-5555-1234
""",
            "instructions": """
Você é um redator técnico especializado. Gere uma seção de perfil da empresa concisa e envolvente para uma proposta.

- Use a língua portuguesa.
- Inclua nome da empresa, competências principais, certificações e conquistas notáveis.
- Destaque a relevância para o projeto atual.
- Mantenha abaixo de 200 palavras.
- Formate com títulos e marcadores para clareza.
"""
        },
        "spanish": {
            "example": """
Ejemplo de Perfil de la Empresa:

**Alpha Consulting**
Alpha Consulting es una firma de ingeniería líder con más de 20 años de experiencia en desarrollo de infraestructura.
Puntos Fuertes:
- Experiencia en soluciones de ciudades inteligentes
- Certificaciones ISO 9001 e ISO 14001
- Historial comprobado con más de 50 proyectos completados en 10 países

Contacto: contacto@alphaconsulting.com | +34-555-123-456
""",
            "instructions": """
Eres un redactor técnico experto. Genera una sección de perfil de empresa concisa y atractiva para una propuesta.

- Usa el idioma español.
- Incluye nombre de la empresa, competencias clave, certificaciones y logros destacados.
- Resalta la relevancia para el proyecto actual.
- Mantén menos de 200 palabras.
- Formatea con encabezados y viñetas para claridad.
"""
        }
    }
    return templates.get(language, templates["english"])


def build_prompt(firm: dict, project_relevance: str, language: str = "english") -> str:
    """
    Construct the prompt for generating a tailored company profile.
    firm: {
        "name": str,
        "description": str,
        "certifications": List[str],
        "achievements": List[str]
    }
    project_relevance: short text explaining how this firm relates to the project
    """
    language = language.lower() if language.lower() in SUPPORTED_LANGUAGES else "english"
    tpl = get_language_profile_templates(language)
    example = tpl["example"]
    instructions = tpl["instructions"]

    certs = "\n".join(f"- {c}" for c in firm.get("certifications", []))
    achievements = "\n".join(f"- {a}" for a in firm.get("achievements", []))

    prompt = f"""
{instructions}

Generate a company profile using the data below.

Company Name: {firm['name']}
Description: {firm['description']}
Certifications:
{certs or '- None provided'}
Key Achievements:
{achievements or '- None provided'}
Relevance to Project: {project_relevance}

{example}

Now produce the tailored company profile.
"""
    return prompt.strip()


def generate_company_profile(firm: dict, project_relevance: str, language: str = "english") -> str:
    """
    Call OpenAI to generate a company profile.
    """
    prompt = build_prompt(firm, project_relevance, language)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You write clear, professional company profiles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=400,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        profile = response.choices[0].message.content.strip()
        return profile
    except Exception as e:
        return f"Error generating company profile: {e}"


# Manual test
if __name__ == "__main__":
    sample_firm = {
        "name": "Alpha Consulting",
        "description": "A multidisciplinary engineering firm specializing in urban infrastructure.",
        "certifications": ["ISO 9001", "ISO 14001"],
        "achievements": ["Completed 50+ international projects", "Awarded Best Green Design 2023"]
    }
    relevance = "Their expertise in urban infrastructure directly supports the Smart City project objectives."
    print(generate_company_profile(sample_firm, relevance, language="english"))
