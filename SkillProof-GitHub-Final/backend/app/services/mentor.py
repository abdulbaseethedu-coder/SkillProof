import os
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

SYSTEM_PROMPT = """You are SkillGuide, the practical mentor inside SkillProof.
Help the student demonstrate a skill through their own work. Use the exact task, workspace, current work and recent conversation. Never give a submit-ready solution or complete code/query/formula/lab answer. Give targeted hints, concepts, debugging guidance, checks and guiding questions. Adapt to the student's exact query. If the student shares an error, address that error. Use progressive hints and ask one useful next question when appropriate. Be concise and practical."""

def _fallback(message, task, code="", state=None):
    text = message.lower().strip(); title = task.get("title", "this task"); skill = task.get("skill", "the skill"); wt = task.get("workspace_type", "general")
    if not text: return f"Tell me the exact part of {title} you are working on. I can guide your next step without doing the task for you."
    if any(x in text for x in ["error", "exception", "wrong", "not working", "issue"]):
        return f"Let's debug the specific issue in your {wt} workspace. What does the error/output show, and what value or step immediately precedes it? Check that first before changing multiple things."
    if "why" in text:
        return f"For {title}, compare your current choice with one reasonable alternative. What evidence from the task supports your choice, and what would change if you used the alternative?"
    if any(x in text for x in ["start", "begin", "first", "how do i"]):
        req = (task.get("requirements") or ["the first requirement"])[0]
        return f"Start with one small checkpoint: {req}. Identify the input/observation you need first, then decide what evidence would show that checkpoint is complete."
    if any(x in text for x in ["formula", "calculate", "calculation"]):
        return f"Before calculating, name the quantity you need and list the inputs that represent it. Which relationship or formula connects those inputs? Write that down first, then substitute values."
    if "duplicate" in text:
        return f"Define what makes two records the same real-world item in {title}. Which field or combination should be unique? Inspect the count before removing anything."
    if any(x in text for x in ["missing", "null", "blank"]):
        return f"Profile where the missing values occur and whether they follow a pattern. What does a missing value mean in this task? Decide that before choosing how to handle it."
    if any(x in text for x in ["explain", "concept"]):
        return f"Break the {skill} idea into: what the input means, what transformation/relationship you apply, and what evidence should appear in the result. Which of those three is unclear?"
    if "result" in text or "output" in text:
        return f"Treat the output as evidence. Pick one result that looks important and trace it back to the input and step that produced it. Does the reasoning match the task requirement?"
    return f"I can help with that. For {title}, point me to the exact step or part of your current work that you are unsure about. I'll give you the next useful hint rather than the final answer."

def mentor_reply(message, task, code="", history=None, state=None):
    api_key = os.getenv("OPENAI_API_KEY", "").strip(); model = os.getenv("OPENAI_MODEL", "gpt-5.6-luna").strip()
    if not api_key or OpenAI is None:
        return _fallback(message, task, code, state), "demo-fallback"
    recent = (history or [])[-8:]
    context = f"Task: {task}\nWorkspace state: {state or {}}\nCurrent work:\n{code[-12000:]}\nRecent conversation: {recent}\nQuestion: {message}"
    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(model=model, instructions=SYSTEM_PROMPT, input=context, store=False)
        out = getattr(response, "output_text", "").strip()
        return (out or _fallback(message, task, code, state)), "openai"
    except Exception:
        return _fallback(message, task, code, state), "demo-fallback-api-error"
