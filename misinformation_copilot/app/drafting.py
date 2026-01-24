"""Draft rebuttal generation using LLM or templates"""

import re
from typing import List, Dict, Any
from .config import Config


class RebuttalDrafter:
    """Generates rebuttal drafts in different styles"""

    def __init__(self):
        self.llm_config = Config.get_llm_config()

    def generate_drafts(self, post_text: str, tags: List[str] = None, rationale: str = "") -> List[str]:
        """
        Generate 3 rebuttal drafts:
        1. Short punchy
        2. Factual calm
        3. Snarky but appropriate

        Returns list of 3 draft strings
        """
        if not post_text:
            return ["No content to respond to."] * 3

        # If LLM is available, use it
        if self.llm_config['enabled'] and self.llm_config['provider'] != 'mock':
            try:
                return self._generate_with_llm(post_text, tags, rationale)
            except Exception as e:
                print(f"LLM drafting failed, using templates: {e}")

        # Fallback to template-based drafts
        return self._generate_with_templates(post_text, tags, rationale)

    def _generate_with_llm(self, post_text: str, tags: List[str], rationale: str) -> List[str]:
        """Generate drafts using LLM"""
        provider = self.llm_config['provider']

        if provider == 'openai':
            return self._draft_with_openai(post_text, tags, rationale)
        elif provider == 'anthropic':
            return self._draft_with_anthropic(post_text, tags, rationale)
        elif provider == 'ollama':
            return self._draft_with_ollama(post_text, tags, rationale)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def _draft_with_openai(self, post_text: str, tags: List[str], rationale: str) -> List[str]:
        """Generate drafts using OpenAI"""
        import openai

        openai.api_key = self.llm_config['api_key']

        prompt = self._build_drafting_prompt(post_text, tags, rationale)

        response = openai.chat.completions.create(
            model=self.llm_config['model'],
            messages=[
                {"role": "system", "content": "You are a fact-checker helping draft respectful but firm rebuttals to misinformation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        return self._parse_drafts(response.choices[0].message.content)

    def _draft_with_anthropic(self, post_text: str, tags: List[str], rationale: str) -> List[str]:
        """Generate drafts using Anthropic"""
        import anthropic

        client = anthropic.Anthropic(api_key=self.llm_config['api_key'])

        prompt = self._build_drafting_prompt(post_text, tags, rationale)

        message = client.messages.create(
            model=self.llm_config['model'],
            max_tokens=800,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ],
            system="You are a fact-checker helping draft respectful but firm rebuttals to misinformation."
        )

        return self._parse_drafts(message.content[0].text)

    def _draft_with_ollama(self, post_text: str, tags: List[str], rationale: str) -> List[str]:
        """Generate drafts using Ollama"""
        import requests

        prompt = self._build_drafting_prompt(post_text, tags, rationale)

        response = requests.post(
            f"{self.llm_config['url']}/api/generate",
            json={
                "model": self.llm_config['model'],
                "prompt": f"You are a fact-checker.\n\n{prompt}",
                "stream": False,
                "options": {
                    "temperature": 0.7
                }
            },
            timeout=60
        )

        response.raise_for_status()
        return self._parse_drafts(response.json()['response'])

    def _build_drafting_prompt(self, post_text: str, tags: List[str], rationale: str) -> str:
        """Build prompt for draft generation"""
        tags_str = ', '.join(tags) if tags else 'none identified'

        return f"""Generate 3 different rebuttal drafts for this social media post that contains potential misinformation.

Original post:
{post_text[:800]}

Analysis: {rationale}
Tags: {tags_str}

Generate exactly 3 drafts with these styles:

DRAFT 1 - Short Punchy:
A brief, direct response (2-3 sentences max). Cut through the nonsense quickly. No fluff.

DRAFT 2 - Factual Calm:
A measured, evidence-based response. Use "what we know / what we don't know" framework. Calm and educational tone. 3-4 sentences.

DRAFT 3 - Snarky But Appropriate:
A response with personality and a bit of snark, but NO slurs, threats, or personal attacks. Sound like a real person, not corporate. Still fact-based. 3-4 sentences.

IMPORTANT FORMATTING:
- NO bullet points or dashes
- Use short paragraphs only
- Sound natural and conversational
- Separate each draft with "---"

Generate the 3 drafts now:"""

    def _parse_drafts(self, response: str) -> List[str]:
        """Parse LLM response into 3 drafts"""
        # Split by common separators
        parts = re.split(r'---+|DRAFT \d+[:\-]', response)
        drafts = [p.strip() for p in parts if p.strip() and len(p.strip()) > 20]

        # Ensure we have exactly 3 drafts
        if len(drafts) >= 3:
            return drafts[:3]
        elif len(drafts) > 0:
            # Pad with variations
            while len(drafts) < 3:
                drafts.append(drafts[0])
            return drafts[:3]
        else:
            # Fallback if parsing failed
            return [
                "This claim needs verification. Do you have credible sources?",
                "I'm skeptical of this claim. Here's what we actually know based on reliable sources.",
                "Cool story, but gonna need some actual evidence on this one."
            ]

    def _generate_with_templates(self, post_text: str, tags: List[str], rationale: str) -> List[str]:
        """Generate template-based drafts when LLM is not available"""
        tags = tags or []

        # Extract a key claim if possible
        sentences = [s.strip() for s in post_text.split('.') if s.strip()]
        key_claim = sentences[0][:150] if sentences else "this claim"

        # Draft 1: Short Punchy
        draft1_options = [
            f"Got a source for that? This sounds like {tags[0] if tags else 'misinformation'}.",
            "That's not accurate. Please verify your sources before sharing.",
            "Hold up. Where's the evidence for this claim?",
            "This has been debunked multiple times. Check reputable fact-checkers."
        ]
        draft1 = draft1_options[len(post_text) % len(draft1_options)]

        # Draft 2: Factual Calm
        if 'vague_sources' in tags or 'conspiracy_theory' in tags:
            draft2 = f"I'd like to see the evidence for this claim. What we know from credible sources is often different from what gets shared on social media. What we don't know is whether this specific claim has been verified by reputable fact-checkers. Can you share your sources?"
        elif 'sensational_language' in tags:
            draft2 = f"This appears to use sensational language to grab attention. When checking claims like these, it's important to look for peer-reviewed research, statements from domain experts, and fact-checker analysis. What credible sources support this?"
        else:
            draft2 = f"This claim warrants skepticism. What we know is that extraordinary claims require extraordinary evidence. What we don't know is whether this has been verified by reliable sources. I'd encourage everyone to fact-check before sharing."

        # Draft 3: Snarky But Appropriate
        draft3_options = [
            "My dude, you can't just say stuff like this without receipts. Where's the actual proof?",
            "Yeah, I'm gonna need to see some real sources here because this sounds completely made up.",
            "Love how this conveniently has zero credible sources. Almost like it's not true. Wild.",
            "This is the kind of thing that sounds dramatic but falls apart the second you actually look into it. Try fact-checking.",
        ]
        if 'conspiracy_theory' in tags:
            draft3 = "Okay so this is conspiracy theory territory. If there's actual evidence, please share it from credible sources. Otherwise this is just creative fiction."
        elif 'emotional_manipulation' in tags:
            draft3 = "The emotional manipulation here is pretty obvious. Real facts don't need this much drama. Got any actual evidence?"
        else:
            draft3 = draft3_options[len(post_text) % len(draft3_options)]

        return [draft1, draft2, draft3]


def generate_drafts(post_text: str, tags: List[str] = None, rationale: str = "") -> List[str]:
    """Convenience function to generate drafts"""
    drafter = RebuttalDrafter()
    return drafter.generate_drafts(post_text, tags, rationale)
