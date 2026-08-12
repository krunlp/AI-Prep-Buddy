name: 💡 New Question / Topic Proposal
description: Propose a new interview question, section, or topic for AI Prep Buddy
title: '[QUESTION]: '
labels: ['question-request', 'enhancement']
assignees: ''

body:
  - type: markdown
    attributes:
      value: Thank you for helping expand AI Prep Buddy! Please provide details about the proposed question or topic.
  - type: textarea
    id: question_text
    attributes:
      label: Proposed Question(s)
      description: What is the question or topic area you would like to add?
      placeholder: e.g., How do you design an evaluation harness for multimodality in vision-language models?
    validations:
      required: true
  - type: dropdown
    id: target_section
    attributes:
      label: Target Section
      description: Which section does this question fit best into?
      options:
        - Section 1–10 (ML/DL Fundamentals)
        - Section 13–21 (LLM & System Design)
        - Section 22–31 (Safety, Governance & Coding)
        - Section 32–42 (Frontier Topics: Multimodal, PEFT, Distributed, Causal)
        - Section 43–49 (Agentic Frameworks, Hardware, Security, Cloud AI)
        - New Section Proposal
    validations:
      required: true
  - type: textarea
    id: answer_framework
    attributes:
      label: Key Answer Points / Framework (Optional)
      description: What are the key points a Principal-level candidate should hit?
