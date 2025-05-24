# cover_letter.py
"""
Module to build and invoke Gemini-based cover letter generation prompt templates.
"""
import os
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def get_language_templates(language: str):
    """
    Return language-specific example and instruction templates.
    """
    language = language.lower()
    templates = {
        "english": {
            "example": """
Example Cover Letter:

Dear Review Committee,

We are pleased to submit our Expression of Interest for the project titled \"{project_name}\".
Our consortium, led by {lead_firm}, includes {firms}.
With a combined experience of over 50 years in sustainable energy projects, we are confident in delivering exceptional results aligned with the funding institution's objectives.

We look forward to collaborating on this transformative project.

Sincerely,
{lead_firm}
""",
            "instructions": """
You are a professional proposal writer tasked with creating a formal, clear, and engaging cover letter for a consulting or engineering project proposal.

- Use the English language.
- Address the funding institution respectfully.
- Mention the project name and a concise summary.
- Highlight the participating firms by name and emphasize the leadership of the lead firm.
- Showcase the strengths, experience, and relevance of the consortium.
- Match the tone expected by funding bodies: formal, confident, and precise.
- Avoid overly technical jargon but maintain professionalism.
- Format the letter as a standard business letter.
"""
        },
        "portuguese": {
            "example": """
Exemplo de Carta de Apresentação:

Prezada Comissão Avaliadora,

Temos o prazer de submeter nossa Manifestação de Interesse para o projeto intitulado \"{project_name}\".
Nosso consórcio, liderado pela {lead_firm}, inclui {firms}.
Com uma experiência combinada de mais de 50 anos em projetos de energia sustentável, estamos confiantes em entregar resultados excepcionais alinhados aos objetivos da instituição financiadora.

Esperamos colaborar neste projeto transformador.

Atenciosamente,
{lead_firm}
""",
            "instructions": """
Você é um redator profissional de propostas encarregado de criar uma carta de apresentação formal, clara e envolvente para uma proposta de projeto de consultoria ou engenharia.

- Use a língua portuguesa.
- Dirija-se respeitosamente à instituição financiadora.
- Mencione o nome do projeto e um resumo conciso.
- Destaque as empresas participantes pelo nome e enfatize a liderança da empresa líder.
- Apresente os pontos fortes, a experiência e a relevância do consórcio.
- Adote o tom esperado pelas instituições financiadoras: formal, confiante e preciso.
- Evite jargões técnicos excessivos, mas mantenha o profissionalismo.
- Formate a carta como uma carta comercial padrão.
"""
        },
        "spanish": {
            "example": """
Ejemplo de Carta de Presentación:

Estimado Comité Evaluador,

Nos complace presentar nuestra Manifestación de Interés para el proyecto titulado \"{project_name}\".
Nuestro consorcio, liderado por {lead_firm}, incluye a {firms}.
Con una experiencia combinada de más de 50 años en proyectos de energía sostenible, confiamos en ofrecer resultados excepcionales alineados con los objetivos de la institución financiadora.

Esperamos colaborar en este proyecto transformador.

Atentamente,
{lead_firm}
""",
            "instructions": """
Eres un redactor profesional de propuestas encargado de crear una carta de presentación formal, clara y atractiva para una propuesta de proyecto de consultoría o ingeniería.

- Usa el idioma español.
- Dirígete respetuosamente a la institución financiadora.
- Menciona el nombre del proyecto y un resumen conciso.
- Destaca las empresas participantes por nombre y enfatiza el liderazgo de la empresa líder.
- Muestra las fortalezas, experiencia y relevancia del consorcio.
- Adopta el tono esperado por las instituciones financiadoras: formal, confiado y preciso.
- Evita la jerga técnica excesiva pero mantén el profesionalismo.
- Formatea la carta como una carta comercial estándar.
"""
        }
    }
    return templates.get(language, templates["english"])


def build_prompt(project_name, project_description, funding_institution, firms, lead_firm, language="english"):
    """
    Construct the full prompt by combining instructions, project facts, and example.
    """
    language_templates = get_language_templates(language)
    firm_names = ", ".join(firm["name"] for firm in firms)

    example = language_templates["example"].format(
        project_name=project_name,
        lead_firm=lead_firm,
        firms=firm_names
    )

    instructions = language_templates["instructions"]

    prompt = f"""
{instructions}

Here is the project information you must incorporate:

Project Name: {project_name}
Project Description: {project_description}
Funding Institution: {funding_institution}
Participating Firms: {firm_names}
Lead Firm: {lead_firm}

{example}

Now generate the cover letter following these guidelines.
"""
    return prompt.strip()


def generate_cover_letter(project_name, project_description, funding_institution, firms, lead_firm, language="english"):
    """
    Call Gemini API to generate the cover letter based on the constructed prompt.
    """
    prompt = build_prompt(
        project_name,
        project_description,
        funding_institution,
        firms,
        lead_firm,
        language
    )

    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        response = model.generate_content(prompts=[{"text": prompt}])
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Cover letter generation failed: {e}")


# Example usage (remove or wrap under `if __name__ == '__main__'` in production)
if __name__ == "__main__":
    sample_firms = [{"name": "Alpha Consulting"}, {"name": "Beta Engineers"}]
    letter = generate_cover_letter(
        project_name="Iniciativa de Energía Sostenible",
        project_description="Un proyecto para desarrollar soluciones de energía renovable.",
        funding_institution="Fondo Global de Energía",
        firms=sample_firms,
        lead_firm="Alpha Consulting",
        language="spanish"
    )
    print(letter)

# legal_documents.py
"""
Module to generate legal document prompts: Power of Attorney & Letter of Association
"""

POWER_OF_ATTORNEY_TEMPLATE = """You are a legal document specialist.
Draft a Power of Attorney document using only the details below.
Do not hallucinate any legal clauses—use standard, generic language.

Firm Granting Power: {grantor_firm}
Authorized Representative: {representative_name}, {representative_title}
Scope of Authority: {scope_of_authority}
Effective Date: {effective_date}

Structure:
1. Title: POWER OF ATTORNEY
2. Identification of grantor and representative
3. Statement of authority granted
4. Duration and limitations
5. Signatures and notarization block
"""

LETTER_OF_ASSOCIATION_TEMPLATE = """You are a legal document specialist.
Draft a Letter of Association with the details below.
Use only provided information; do not add details.

Lead Firm: {lead_firm}
Associate Firm: {associate_firm}
Purpose of Association: {association_purpose}
Effective Date: {effective_date}

Structure:
1. Title: LETTER OF ASSOCIATION
2. Introductory statement of purpose
3. Roles and responsibilities of each firm
4. Duration and termination clauses
5. Signature block for both firms
"""

def get_poaw_prompt(grantor_firm, representative_name, representative_title, scope_of_authority, effective_date):
    return POWER_OF_ATTORNEY_TEMPLATE.format(
        grantor_firm=grantor_firm,
        representative_name=representative_name,
        representative_title=representative_title,
        scope_of_authority=scope_of_authority,
        effective_date=effective_date
    )


def get_loa_prompt(lead_firm, associate_firm, association_purpose, effective_date):
    return LETTER_OF_ASSOCIATION_TEMPLATE.format(
        lead_firm=lead_firm,
        associate_firm=associate_firm,
        association_purpose=association_purpose,
        effective_date=effective_date
    )

# company_profiles.py
"""
Module to generate company profile prompts
"""

COMPANY_PROFILE_TEMPLATE = """You are a marketing copywriter.
Create a concise company profile section using only the data below.

Firm Name: {firm_name}
Established: {year_established}
Headquarters: {headquarters_location}
Core Competencies: {core_competencies}
Key Projects (with dates): {key_projects}

Structure:
1. Company Overview (1–2 sentences)
2. Core Competencies (bullet points)
3. Highlighted Past Projects (bullet points with dates)
4. Unique Value Proposition specific to the current project requirements
"""

def get_company_profile_prompt(firm_name, year_established, headquarters_location, core_competencies, key_projects):
    return COMPANY_PROFILE_TEMPLATE.format(
        firm_name=firm_name,
        year_established=year_established,
        headquarters_location=headquarters_location,
        core_competencies=core_competencies,
        key_projects=key_projects
    )

# contacts.py
"""
Module to generate contact information prompt
"""

CONTACT_INFO_TEMPLATE = """You are a detail-oriented assistant.
Compile the contact information into a neatly formatted table or list,
using only the fields given. Do not add or omit fields.

Contacts:
{contacts_list}

Output as:
| Name               | Title             | Email               | Phone       |
|--------------------|-------------------|---------------------|-------------|
| ...                | ...               | ...                 | ...         |
"""

def get_contacts_prompt(contacts_list):
    return CONTACT_INFO_TEMPLATE.format(contacts_list=contacts_list)

# project_list.py
"""
Module to generate project list scoring prompt
"""

PROJECT_LIST_ENTRY_TEMPLATE = """You are an analytical reviewer.
For each past project provided, score its relevance (1–5) to the current project,
and generate a short justification. Use only these inputs—no extra info.

Current Project Requirements: {current_requirements}

Past Project:
- Name: {past_project_name}
- Description: {past_project_description}
- Year: {past_project_year}

Output Format:
- Project Name: …
- Relevance Score (1–5): …
- Justification: … (1–2 sentences)
"""

def get_project_list_entry_prompt(current_requirements, past_project_name, past_project_description, past_project_year):
    return PROJECT_LIST_ENTRY_TEMPLATE.format(
        current_requirements=current_requirements,
        past_project_name=past_project_name,
        past_project_description=past_project_description,
        past_project_year=past_project_year
    )
