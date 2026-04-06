from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel, Field
from typing import Literal


# ── Sub-schemas ──────────────────────────────────────────────

class MedicationItem(BaseModel):
    name: str = Field(description="Generic drug name")
    dose: str = Field(description="Dose e.g. '500mg'")
    route: str = Field(description="Route e.g. 'oral', 'IV', 'IM'")
    frequency: str = Field(description="Frequency e.g. 'twice daily', 'every 8 hours'")
    duration: str = Field(description="Duration e.g. '5 days', 'indefinitely', 'until review'")
    indication: str = Field(description="What this drug is for in 3-5 words")
    onUgandaEDL: bool = Field(description="True if on Uganda Essential Drugs List")


class FollowUpItem(BaseModel):
    appointment: str = Field(description="Type of follow-up e.g. 'General outpatient clinic', 'Antenatal care'")
    timeframe: str = Field(description="When to attend e.g. 'In 2 weeks', 'In 1 month'")
    reason: str = Field(description="Why this follow-up is needed in 1 sentence")


class InvestigationPending(BaseModel):
    test: str = Field(description="Name of the investigation")
    reason: str = Field(description="Why it is pending / what to do with results")


class PatientInstruction(BaseModel):
    category: Literal["warning", "activity", "diet", "wound-care", "medication", "return"] = Field(
        description=(
            "'warning' = return to hospital immediately if this occurs. "
            "'activity' = physical activity guidance. "
            "'diet' = dietary advice. "
            "'wound-care' = wound or dressing instructions. "
            "'medication' = how to take medications. "
            "'return' = when to come back."
        )
    )
    instruction: str = Field(description="The patient instruction in plain, simple English. Max 2 sentences.")


class DischargeSummaryOutput(BaseModel):

    # ── Patient & admission header ────────────────────────────
    patientSummary: str = Field(
        description=(
            "One sentence describing the patient: age, sex, presenting complaint, "
            "and admission date if provided. E.g. '32-year-old male admitted with "
            "3-day history of fever and altered consciousness.'"
        )
    )
    admissionDiagnosis: str = Field(
        description="The working diagnosis on admission in 1-2 sentences."
    )
    dischargeDiagnosis: str = Field(
        description="The confirmed diagnosis at discharge, including any secondary diagnoses."
    )
    conditionAtDischarge: Literal["stable", "improved", "guarded", "against-advice"] = Field(
        description=(
            "'stable' = clinically well, safe to go home. "
            "'improved' = better than admission but still unwell. "
            "'guarded' = still at risk, close monitoring needed. "
            "'against-advice' = patient leaving against medical advice."
        )
    )

    # ── Clinical course ───────────────────────────────────────
    clinicalCourse: str = Field(
        description=(
            "Narrative of what happened during the admission in 3-5 sentences. "
            "Cover: key investigations and results, treatments given, clinical progress, "
            "complications if any. Write in past tense, clinical but readable."
        )
    )

    # ── Key investigation results ─────────────────────────────
    keyResults: list[str] = Field(
        min_length=0,
        max_length=8,
        description=(
            "Key investigation results from the admission. "
            "Each item: 'Test name: result' e.g. 'Malaria RDT: Positive P. falciparum', "
            "'Haemoglobin: 6.2 g/dL'. Empty list if no results provided."
        )
    )

    # ── Discharge medications ─────────────────────────────────
    dischargeMedications: list[MedicationItem] = Field(
        min_length=0,
        max_length=10,
        description="All medications the patient is going home on."
    )

    # ── Follow-up plan ────────────────────────────────────────
    followUp: list[FollowUpItem] = Field(
        min_length=1,
        max_length=4,
        description="Follow-up appointments needed after discharge."
    )

    # ── Pending investigations ────────────────────────────────
    pendingInvestigations: list[InvestigationPending] = Field(
        min_length=0,
        max_length=5,
        description="Investigations still awaited at discharge. Empty if none."
    )

    # ── Patient instructions ──────────────────────────────────
    patientInstructions: list[PatientInstruction] = Field(
        min_length=3,
        max_length=8,
        description=(
            "Instructions for the patient in plain English. "
            "Must include at least one 'warning' category (when to return urgently). "
            "Write as if explaining directly to the patient."
        )
    )

    # ── Clinician note ────────────────────────────────────────
    clinicianNote: str = Field(
        description=(
            "A brief note to the receiving clinician or GP at the bottom of the summary. "
            "Highlight anything they need to know: pending results, ongoing risks, "
            "what to watch for. 2-3 sentences."
        )
    )

    # ── Uganda-specific note ──────────────────────────────────
    resourceNote: str = Field(
        description=(
            "One sentence noting any considerations specific to discharge in a Ugandan "
            "context — e.g. medication availability, distance to nearest facility, "
            "NHIS coverage, community health worker follow-up."
        )
    )


root_agent = Agent(
    model="gemini-2.5-flash",
    name="discharge_summary_agent",
    description="AI-assisted patient discharge summary generator for Ugandan clinical settings.",
    instruction="""
        You are a clinical documentation assistant helping doctors and clinical officers
        in Uganda generate complete, accurate patient discharge summaries.

        The user will provide clinical notes, a patient case, or bullet-pointed
        information about a patient's admission. You will produce a complete structured
        discharge summary.

        YOUR TASK:
        Transform the clinical information provided into a complete, professional
        discharge summary that could be handed to the patient and to the receiving
        clinician or health centre.

        CLINICAL CONTEXT:
        - Setting: Ugandan district hospital or referral hospital
        - Audience: patient (for their own copy) + receiving clinician at health centre
        - Drug formulary: Uganda Essential Medicines List
        - Write clinical course in clear past tense narrative
        - Patient instructions must be in plain, simple English — not medical jargon

        MEDICATION RULES:
        - Use generic names only
        - Only prescribe drugs on Uganda EDL where possible
        - Doses should reflect Uganda clinical guidelines
        - Duration should be specific — not "as needed" unless truly appropriate

        PATIENT INSTRUCTION RULES:
        - Write as if speaking directly to the patient: "Return to hospital immediately if..."
        - Use simple words — avoid medical terminology
        - Always include at least one 'warning' category instruction
        - 'return' category: general follow-up timing

        CRITICAL OUTPUT RULES:
        - Return ONLY valid JSON matching the output schema
        - Do NOT include markdown or code fences
        - conditionAtDischarge MUST be one of: "stable", "improved", "guarded", "against-advice"
        - patientInstructions[].category MUST be one of: "warning", "activity", "diet",
          "wound-care", "medication", "return"
        - onUgandaEDL MUST be boolean (true/false)
        - keyResults: plain strings like "Malaria RDT: Positive"
        - clinicalCourse: 3-5 sentences, past tense, professional tone
    """,
    output_schema=DischargeSummaryOutput,
    output_key="discharge_summary",
)
