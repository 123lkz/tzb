import json, httpx, re, random
from agents.agent2.config import DEEPSEEK_API_KEY, DEEPSEEK_API_BASE, DEEPSEEK_MODEL
from loguru import logger

_mock_responses = [
    '{"valid":true,"confidence":0.85,"explanation":"Based on NL profile analysis, this skill is commonly required for the position.","evidence":[{"type":"industry","detail":"Common requirement across job postings"}],"counter_evidence":[],"recommendation":"include"}',
    '{"valid":true,"confidence":0.72,"explanation":"This skill is relevant but not strictly required for this position.","evidence":[{"type":"context","detail":"Skill mentioned in some but not all postings"}],"counter_evidence":[{"type":"alternative","detail":"Can be substituted with similar technologies"}],"recommendation":"weakly_include"}',
    '{"valid":false,"confidence":0.35,"explanation":"This skill does not have a clear relationship with the core responsibilities of this position.","evidence":[],"counter_evidence":[{"type":"mismatch","detail":"Skill domain differs from position domain"}],"recommendation":"exclude"}',
    '{"valid":true,"confidence":0.91,"explanation":"Direct match: this is a core technology for the position.","evidence":[{"type":"direct","detail":"Listed as required skill in multiple job descriptions"}],"counter_evidence":[],"recommendation":"strongly_include"}',
    '{"summary":"A widely-used technology in the industry.","prerequisites":["Basic programming"],"related_technologies":["Tech A","Tech B"],"typical_applications":["Application 1","Application 2"],"industry_trend":"Growing demand expected.","proficiency_levels":{"beginner":"Can perform basic tasks","intermediate":"Can work independently","advanced":"Can optimize and innovate"}}}',
    '{"summary":"A common position in the job market.","core_responsibilities":["Responsibility 1","Responsibility 2"],"required_skills":["Skill A","Skill B"],"optional_skills":["Skill C"],"industry_domain":"Technology","typical_salary_range":"Competitive","experience_level":"2-5 years"}',
]
_mock_idx = [0]
def _get_mock():
    resp = _mock_responses[_mock_idx[0] % len(_mock_responses)]
    _mock_idx[0] = (_mock_idx[0] + 1) % len(_mock_responses)
    return resp

class LLMClient:
    def __init__(self, api_key=DEEPSEEK_API_KEY, api_base=DEEPSEEK_API_BASE, model=DEEPSEEK_MODEL):
        self.api_key = api_key
        self.api_base = api_base.rstrip("/")
        self.model = model
        logger.info(f"LLMClient: model={model}, base={api_base}")

    def chat(self, messages, temperature=0.3):
        if not self.api_key:
            logger.warning("DeepSeek API key not configured, using mock")
            return _get_mock()
        url = f"{self.api_base}/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": self.model, "messages": messages, "temperature": temperature, "max_tokens": 4096}
        for attempt in range(2):
            try:
                resp = httpx.post(url, headers=headers, json=payload, timeout=30)
                if resp.status_code != 200:
                    logger.warning(f"DeepSeek API error: {resp.status_code} {resp.text[:200]}")
                    if attempt == 0: continue
                    return _get_mock()
                result = resp.json()
                return result["choices"][0]["message"]["content"]
            except Exception as e:
                logger.warning(f"DeepSeek call failed (attempt {attempt+1}): {e}")
                if attempt == 0: continue
                logger.warning("Falling back to mock")
                return _get_mock()

    def chat_with_json(self, messages, temperature=0.1):
        result = self.chat(messages, temperature)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", result, re.DOTALL)
            if m:
                try: return json.loads(m.group(1))
                except: pass
            return {"raw": result, "error": "parse_failed"}

SparkLLMClient = LLMClient
__all__ = ["LLMClient", "SparkLLMClient"]
