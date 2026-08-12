name: 🐛 Bug Report / Typo Correction
description: Report a broken link, formatting error, typo, or simulator issue
title: '[BUG]: '
labels: ['bug', 'triage']
assignees: ''

body:
  - type: textarea
    id: bug_description
    attributes:
      label: Description of the Bug
      description: What is broken or incorrect?
      placeholder: e.g., Broken link in answers.md pointing to diagram 12.
    validations:
      required: true
  - type: input
    id: file_location
    attributes:
      label: File Location / URL
      description: Which file or web URL contains the issue?
      placeholder: e.g., questions.md Section 14 Q245
    validations:
      required: true
  - type: textarea
    id: suggested_fix
    attributes:
      label: Suggested Fix (Optional)
      description: How should this issue be fixed?
