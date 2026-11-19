"""Conservative routing for project context, general requests and unclear input."""

import re
import unicodedata


def _normalize(value):
    text = unicodedata.normalize("NFD", value.lower().replace("đ", "d"))
    return " ".join("".join(ch for ch in text if unicodedata.category(ch) != "Mn").split())


_PROJECT_SYMBOL = re.compile(
    r"\b(?:coursemanagementsystem|coursemanagement|coursedaoimpl|studentdaoimpl|"
    r"documentserviceimpl|authrestimpl|hibernatepaginationsortingdao|findbypricerange|"
    r"course_db|app_detail_fk|enrollmentserviceimpl|genericspecification|genericspecificationsbuilder|"
    r"(?:course|student|document|enrollment|department|auth|dashboard)(?:dao|service|rest|controller|entity|requestdto|responsedto|dto)(?:impl)?)\b", re.IGNORECASE,
)
_CURRENT_PROJECT = re.compile(r"\b(?:du an|project|codebase|ma nguon|repo)(?:\s+(?:nay|hien tai|cua toi|cua minh|cms))?\b")
_OTHER_PROJECT = re.compile(r"\b(?:du an|project)\s+(?:moi\s+)?(?:flutter|python|react|vue|django|nodejs|node|angular|ios|android)\b")
_PROJECT_DOMAIN = re.compile(r"\b(?:giang vien|hoc vien|khoa hoc|sinh vien|ghi danh)\b")
_PROJECT_ACTION = re.compile(r"\b(?:module|dao|entity|dto|service|controller|api|tai lieu|quan ly)\b")
_FOLLOWUP = re.compile(r"^(?:giai thich them|noi ro hon|giai thich ro hon|tiep tuc|con cai nay(?: thi sao)?|cai nay|con no(?: thi sao)?|tai sao|vi sao)[?.!\s]*$")
_GENERAL_CUE = re.compile(r"\b(?:la gi|nhu the nao|vi sao|tai sao|the nao|bao nhieu|may|viet|tao|hay|giup|"
                          r"giai thich|cho|tinh|ke|tim|so sanh|kiem tra|sua|dich|what|why|how|explain|write|create)\b")
_GREETINGS = {"hi", "hello", "hey", "alo", "xin chao", "chao", "chao ban", "cam on", "thanks", "ok", "bye"}
_GREETING_START = re.compile(r"^(?:xin chao|chao|hello|hi|hey|alo)\b")


def classify_message(message, history=None):
    """Return project, general or clarify; history only resolves explicit follow-ups."""
    text = _normalize(message or "")
    if not text:
        return "clarify"
    if _FOLLOWUP.fullmatch(text):
        if isinstance(history, list):
            for turn in reversed(history):
                if isinstance(turn, dict) and turn.get("role") == "user" and isinstance(turn.get("content"), str):
                    previous = classify_message(turn["content"])
                    if previous != "clarify":
                        return previous
        return "clarify"
    if _PROJECT_SYMBOL.search(message) or (_CURRENT_PROJECT.search(text) and not _OTHER_PROJECT.search(text)):
        return "project"
    if _PROJECT_DOMAIN.search(text) and _PROJECT_ACTION.search(text):
        return "project"
    if text.strip("?.! ") in _GREETINGS or _GREETING_START.search(text) or _GENERAL_CUE.search(text) or "?" in text or re.search(r"\d\s*[+*/=-]\s*\d", text):
        return "general"
    if len(text.split()) <= 4:
        return "clarify"
    return "general"


def project_retrieval_query(message, history=None):
    """Include the last project question when an explicit follow-up has no topic."""
    if classify_message(message) != "clarify" or classify_message(message, history) != "project":
        return message
    for turn in reversed(history or []):
        if isinstance(turn, dict) and turn.get("role") == "user" and isinstance(turn.get("content"), str):
            if classify_message(turn["content"]) == "project":
                return f"{turn['content']}\n{message}"
    return message
