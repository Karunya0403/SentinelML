\# SuperAnnotate → Hugging Face → Evaluation Gate



A lightweight proof-of-work exploring an annotation-to-model-evaluation workflow.



\## Workflow



SuperAnnotate

↓

Structured NLP training data

↓

Hugging Face model

↓

Model evaluation

↓

Per-category quality checks

↓

PROMOTE / REJECT



\## Why this matters



A model can achieve strong aggregate metrics while still performing poorly on individual categories.



This experiment therefore evaluates both:



\- Overall accuracy

\- Overall F1

\- Per-category F1



A model is approved only when every required quality gate passes.



\# SuperAnnotate → Hugging Face → Evaluation Gate



A lightweight proof-of-work exploring an annotation-to-model-evaluation workflow.



\## Workflow



SuperAnnotate

↓

Structured NLP training data

↓

Hugging Face model

↓

Model evaluation

↓

Per-category quality checks

↓

PROMOTE / REJECT



\## Why this matters



A model can achieve strong aggregate metrics while still performing poorly on individual categories.



This experiment therefore evaluates both:



\- Overall accuracy

\- Overall F1

\- Per-category F1



A model is approved only when every required quality gate passes.



\## Example Evaluation



| Metric | Result |

|---|---:|

| Accuracy | 96% |

| Overall F1 | 94% |

| Toxic F1 | 95% |

| Insult F1 | 93% |

| Threat F1 | 91% |

| Identity Hate F1 | 94% |

| Obscene F1 | 96% |



\### Decision



```text

Overall F1: 94% >= 90%  PASS



Toxic:         95% >= 90% PASS

Insult:        93% >= 90% PASS

Threat:        91% >= 90% PASS

Identity Hate: 94% >= 90% PASS

Obscene:       96% >= 90% PASS



Decision: APPROVED

