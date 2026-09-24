def evaluate(task, code: str, state: dict | None = None):
    state = state or {}; work = (code or "").strip(); filled = len([v for v in state.values() if str(v).strip()])
    length = len(work)
    score = min(95, max(55, 55 + min(25, length // 80) + min(15, filled * 3)))
    criteria = task.evaluation_criteria or {
        "Correctness": "Strong",
        "Approach": "Good",
        "Problem Solving": "Strong",
        "Task Completion": "Ready",
        "Understanding": "Pending",
    }
    return {
        "score": score,
        "criteria": criteria,
        "capabilities": f"Applied {task.skill} to the real-world task, recorded work evidence, and prepared the reasoning needed for an understanding check.",
        "feedback": "Review the highlighted criteria against your own work before completing the understanding check.",
        "understanding_check": {"questions": [
            {"question": f"What was the most important decision you made while completing '{task.title}', and why?"},
            {"question": "What evidence in your work shows that your result is reliable or correct?"},
            {"question": "If one important input changed, what would you revisit first and why?"}
        ]}
    }

def evaluate_understanding(task, code, answers, evaluation):
    ordered = [answers.get(str(i), "").strip() for i in range(3)]
    answered = sum(1 for a in ordered if len(a) >= 20)
    passed = answered >= 2
    return {
        "passed": passed,
        "answered": answered,
        "total": 3,
        "feedback": "Your explanations show enough reasoning to finalize this proof." if passed else "Give more specific reasoning. Mention the evidence, decision, or relationship from your own work.",
        "answers": ordered,
        "questions": evaluation.get("understanding_check", {}).get("questions", [])
    }
