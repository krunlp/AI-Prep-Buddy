"""
roles_data.py — target role/designation → section coverage map.

Sections are referenced by NUMBER, never by title or question range, so this
file survives retitling and renumbering. Counts and ranges are resolved at
build time from questions.md via qa_lib.

Tiers:
    core       must complete — these are what the loop actually tests
    important  should complete — commonly probed, expected at senior level
    optional   nice to have — breadth/differentiation

Any section not listed for a role is treated as out of scope for that role.
"""

ROLES = [
    {
        "id": "ml-engineer",
        "name": "Machine Learning Engineer",
        "level": "Mid / Senior",
        "blurb": "Builds and ships production ML models. Loop is weighted to classic ML depth, "
                 "practical system design, and coding.",
        "core": [3, 4, 5, 14, 17, 18, 26, 52],
        "important": [2, 6, 7, 15, 16, 19, 24, 25, 39, 50, 51, 53, 55, 56],
        "optional": [8, 21, 34, 40, 41, 54],
    },
    {
        "id": "staff-mle",
        "name": "Staff / Senior Staff ML Engineer",
        "level": "Staff",
        "blurb": "Owns end-to-end ML systems and sets technical direction for a team. "
                 "Expect deep system design plus cross-functional judgement.",
        "core": [2, 3, 4, 5, 14, 15, 16, 17, 18, 26, 27, 50, 51, 52, 53, 55, 56],
        "important": [1, 6, 7, 8, 19, 20, 21, 24, 25, 39, 41, 54],
        "optional": [10, 13, 23, 34, 40, 42],
    },
    {
        "id": "principal-ai-lead",
        "name": "Principal AI/ML Lead / Architect",
        "level": "Principal",
        "blurb": "Sets AI strategy and architecture across an org. The loop tests breadth, "
                 "tradeoff judgement, governance and executive communication as much as depth.",
        "core": [1, 2, 8, 10, 12, 13, 16, 21, 22, 23, 27, 28, 29, 51, 53, 54, 56],
        "important": [3, 5, 9, 11, 15, 18, 19, 20, 30, 31, 43, 48, 49, 50, 52, 55],
        "optional": [14, 17, 32, 33, 34, 45, 46, 47],
    },
    {
        "id": "genai-engineer",
        "name": "GenAI / LLM Applied Engineer",
        "level": "Senior / Staff",
        "blurb": "Builds LLM-powered product features. Heavy on transformers, RAG, agents, "
                 "prompting and evaluation.",
        "core": [8, 9, 10, 11, 12, 13, 21, 43, 48, 50, 51, 52, 55, 56],
        "important": [5, 15, 16, 22, 26, 30, 32, 33, 46, 53, 54],
        "optional": [2, 19, 23, 35, 36, 45, 49],
    },
    {
        "id": "ai-platform-infra",
        "name": "AI Platform / Infrastructure Engineer",
        "level": "Senior / Staff",
        "blurb": "Owns the serving and training substrate. Performance, hardware, distributed "
                 "systems and cost are the whole job.",
        "core": [15, 16, 18, 19, 20, 38, 44, 46, 50, 52, 53],
        "important": [5, 8, 13, 17, 26, 31, 37, 49, 51, 54, 55, 56],
        "optional": [2, 21, 27, 43, 48],
    },
    {
        "id": "mlops-engineer",
        "name": "MLOps / ML Reliability Engineer",
        "level": "Mid / Senior",
        "blurb": "Keeps models healthy in production: pipelines, deployment, monitoring, "
                 "drift and rollback.",
        "core": [16, 17, 18, 19, 20, 21, 39, 50, 52],
        "important": [3, 5, 14, 15, 23, 34, 38, 51, 53, 54],
        "optional": [2, 13, 22, 26, 31, 49, 55, 56],
    },
    {
        "id": "research-engineer",
        "name": "AI Research Engineer (Frontier Lab)",
        "level": "Senior / Staff",
        "blurb": "Trains and improves models. Deepest maths and architecture bar of any track, "
                 "plus strong coding.",
        "core": [3, 4, 5, 8, 26, 33, 38, 46],
        "important": [6, 7, 21, 32, 35, 44, 51, 52, 53, 55, 56],
        "optional": [9, 12, 22, 36, 42, 47, 50, 54],
    },
    {
        "id": "ai-security",
        "name": "AI Security / Red Team Engineer",
        "level": "Senior / Staff",
        "blurb": "Attacks and defends AI systems: jailbreaks, prompt injection, agent abuse, "
                 "adversarial ML and guardrail design.",
        "core": [22, 23, 34, 45, 52],
        "important": [8, 9, 10, 12, 13, 20, 29, 30, 43, 50, 51, 54, 55, 56],
        "optional": [2, 16, 21, 31, 48, 49, 53],
    },
    {
        "id": "solutions-architect",
        "name": "Enterprise AI Solutions Architect",
        "level": "Senior / Principal",
        "blurb": "Designs AI systems inside enterprise constraints: cloud, compliance, "
                 "integration, procurement and cost.",
        "core": [13, 19, 23, 27, 29, 30, 31, 49, 51, 53, 54],
        "important": [1, 2, 10, 12, 16, 20, 22, 48, 50, 52, 55, 56],
        "optional": [8, 11, 15, 18, 21, 43],
    },
    {
        "id": "data-scientist",
        "name": "Data Scientist (ML-leaning)",
        "level": "Mid / Senior",
        "blurb": "Framing, measurement and inference. Statistics and experimentation carry "
                 "more weight than serving infrastructure.",
        "core": [3, 4, 24, 25, 26, 39, 41],
        "important": [5, 14, 18, 21, 34, 40, 51, 52],
        "optional": [2, 16, 17, 42, 50, 53, 54, 55, 56],
    },
    {
        "id": "ai-manager",
        "name": "Engineering Manager / Director, AI",
        "level": "Manager / Director",
        "blurb": "Leads AI teams. Judgement, prioritisation, governance and communication "
                 "dominate; technical depth is tested for credibility, not recall.",
        "core": [1, 2, 23, 27, 29, 51, 54],
        "important": [13, 16, 21, 22, 31, 49, 53],
        "optional": [3, 8, 10, 12, 19, 30, 50, 52, 55, 56],
    },
]
