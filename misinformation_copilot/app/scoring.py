"""Misinformation scoring using heuristics and LLM"""

import re
from typing import Dict, List, Any, Tuple
from .config import Config


class MisinfoScorer:
    """Scores posts for misinformation likelihood"""

    # Heuristic patterns
    SENSATIONAL_PHRASES = [
        r"they don't want you to know",
        r"msm won't (report|cover|tell)",
        r"share before (deleted|removed|banned)",
        r"doctors hate (this|him|her)",
        r"one weird trick",
        r"you won't believe",
        r"shocking truth",
        r"wake up (people|sheeple|sheep)",
        r"do your own research",
        r"the truth they're hiding",
        r"mainstream media (won't|refuses|ignores)",
        r"big pharma doesn't want",
        r"follow the money",
        r"open your eyes",
    ]

    LACK_OF_SOURCES = [
        r"someone said",
        r"people are saying",
        r"i heard that",
        r"word on the street",
        r"sources say",
        r"according to (sources|insiders)",
        r"trust me",
    ]

    CONSPIRACY_MARKERS = [
        r"false flag",
        r"crisis actor",
        r"paid (shill|actor)s?",
        r"deep state",
        r"new world order",
        r"agenda \d+",
        r"they're trying to",
        r"wake up",
    ]

    def __init__(self):
        self.llm_config = Config.get_llm_config()

    def score_post(self, text: str) -> Dict[str, Any]:
        """
        Score a post for misinformation likelihood

        Returns:
            {
                'score': int (0-100),
                'tags': List[str],
                'rationale': str,
                'fact_check_questions': List[str]
            }
        """
        if not text:
            return {
                'score': 0,
                'tags': [],
                'rationale': 'No text content to analyze',
                'fact_check_questions': []
            }

        # Start with heuristic scoring
        heuristic_score, heuristic_tags = self._heuristic_score(text)

        # If LLM is available, use it for more nuanced scoring
        if self.llm_config['enabled'] and self.llm_config['provider'] != 'mock':
            try:
                llm_result = self._llm_score(text, heuristic_score, heuristic_tags)
                # Blend scores: 40% heuristic, 60% LLM
                final_score = int(heuristic_score * 0.4 + llm_result['score'] * 0.6)
                return {
                    'score': final_score,
                    'tags': list(set(heuristic_tags + llm_result.get('tags', []))),
                    'rationale': llm_result.get('rationale', ''),
                    'fact_check_questions': llm_result.get('fact_check_questions', [])
                }
            except Exception as e:
                print(f"LLM scoring failed, using heuristics only: {e}")

        # Fallback to heuristics only
        return {
            'score': heuristic_score,
            'tags': heuristic_tags,
            'rationale': self._generate_heuristic_rationale(heuristic_tags),
            'fact_check_questions': self._generate_heuristic_questions(text, heuristic_tags)
        }

    def _heuristic_score(self, text: str) -> Tuple[int, List[str]]:
        """Calculate heuristic-based score"""
        text_lower = text.lower()
        score = 0
        tags = []

        # Check for ALL CAPS (excessive)
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if caps_ratio > 0.3:
            score += 15
            tags.append('excessive_caps')

        # Check for excessive punctuation
        exclamation_count = text.count('!')
        if exclamation_count > 3:
            score += min(10 + exclamation_count * 2, 25)
            tags.append('excessive_punctuation')

        # Check sensational phrases
        for pattern in self.SENSATIONAL_PHRASES:
            if re.search(pattern, text_lower):
                score += 20
                tags.append('sensational_language')
                break

        # Check lack of sources
        for pattern in self.LACK_OF_SOURCES:
            if re.search(pattern, text_lower):
                score += 15
                tags.append('vague_sources')
                break

        # Check conspiracy markers
        conspiracy_matches = 0
        for pattern in self.CONSPIRACY_MARKERS:
            if re.search(pattern, text_lower):
                conspiracy_matches += 1
        if conspiracy_matches > 0:
            score += min(conspiracy_matches * 15, 30)
            tags.append('conspiracy_theory')

        # Check for urgency manipulation
        urgency_patterns = [
            r"act now", r"time is running out", r"before it's too late",
            r"hurry", r"limited time"
        ]
        for pattern in urgency_patterns:
            if re.search(pattern, text_lower):
                score += 10
                tags.append('urgency_manipulation')
                break

        # Check for emotional manipulation
        emotion_patterns = [
            r"horrifying", r"terrifying", r"outrageous", r"disgusting",
            r"unbelievable", r"shocking"
        ]
        emotion_count = sum(1 for p in emotion_patterns if re.search(p, text_lower))
        if emotion_count >= 2:
            score += 15
            tags.append('emotional_manipulation')

        # Normalize to 0-100
        score = min(score, 100)

        return score, tags

    def _generate_heuristic_rationale(self, tags: List[str]) -> str:
        """Generate rationale based on heuristic tags"""
        if not tags:
            return "No significant misinformation indicators detected."

        tag_explanations = {
            'excessive_caps': "Contains excessive capitalization",
            'excessive_punctuation': "Uses excessive punctuation marks",
            'sensational_language': "Uses sensational or clickbait language",
            'vague_sources': "Lacks specific credible sources",
            'conspiracy_theory': "Contains conspiracy theory markers",
            'urgency_manipulation': "Uses urgency to pressure action",
            'emotional_manipulation': "Uses emotional manipulation tactics"
        }

        explanations = [tag_explanations.get(tag, tag) for tag in tags[:3]]
        return ". ".join(explanations) + "."

    def _generate_heuristic_questions(self, text: str, tags: List[str]) -> List[str]:
        """Generate fact-check questions based on heuristics"""
        questions = []

        if 'vague_sources' in tags:
            questions.append("What are the specific, named sources for these claims?")

        if 'conspiracy_theory' in tags or 'sensational_language' in tags:
            questions.append("What credible evidence supports this claim?")
            questions.append("Have mainstream fact-checkers investigated this?")

        # Extract potential claims (sentences with strong assertions)
        sentences = text.split('.')
        for sent in sentences[:2]:
            if any(word in sent.lower() for word in ['proof', 'evidence', 'study', 'research']):
                questions.append(f"Can you verify: {sent.strip()[:100]}?")
                break

        return questions[:3]

    def _llm_score(self, text: str, heuristic_score: int, heuristic_tags: List[str]) -> Dict[str, Any]:
        """Use LLM for scoring"""
        provider = self.llm_config['provider']

        if provider == 'openai':
            return self._score_with_openai(text, heuristic_score, heuristic_tags)
        elif provider == 'anthropic':
            return self._score_with_anthropic(text, heuristic_score, heuristic_tags)
        elif provider == 'ollama':
            return self._score_with_ollama(text, heuristic_score, heuristic_tags)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def _score_with_openai(self, text: str, heuristic_score: int, heuristic_tags: List[str]) -> Dict[str, Any]:
        """Score using OpenAI API"""
        import openai

        openai.api_key = self.llm_config['api_key']

        prompt = self._build_scoring_prompt(text, heuristic_score, heuristic_tags)

        response = openai.chat.completions.create(
            model=self.llm_config['model'],
            messages=[
                {"role": "system", "content": "You are a fact-checking assistant. Analyze social media posts for misinformation indicators and respond ONLY with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )

        return self._parse_llm_response(response.choices[0].message.content)

    def _score_with_anthropic(self, text: str, heuristic_score: int, heuristic_tags: List[str]) -> Dict[str, Any]:
        """Score using Anthropic API"""
        import anthropic

        client = anthropic.Anthropic(api_key=self.llm_config['api_key'])

        prompt = self._build_scoring_prompt(text, heuristic_score, heuristic_tags)

        message = client.messages.create(
            model=self.llm_config['model'],
            max_tokens=500,
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt}
            ],
            system="You are a fact-checking assistant. Analyze social media posts for misinformation indicators and respond ONLY with valid JSON."
        )

        return self._parse_llm_response(message.content[0].text)

    def _score_with_ollama(self, text: str, heuristic_score: int, heuristic_tags: List[str]) -> Dict[str, Any]:
        """Score using Ollama"""
        import requests

        prompt = self._build_scoring_prompt(text, heuristic_score, heuristic_tags)

        response = requests.post(
            f"{self.llm_config['url']}/api/generate",
            json={
                "model": self.llm_config['model'],
                "prompt": f"You are a fact-checking assistant.\n\n{prompt}",
                "stream": False,
                "options": {
                    "temperature": 0.3
                }
            },
            timeout=30
        )

        response.raise_for_status()
        return self._parse_llm_response(response.json()['response'])

    def _build_scoring_prompt(self, text: str, heuristic_score: int, heuristic_tags: List[str]) -> str:
        """Build prompt for LLM scoring"""
        return f"""Analyze this social media post for misinformation indicators.

Post content:
{text[:1000]}

Heuristic analysis found a score of {heuristic_score}/100 with tags: {', '.join(heuristic_tags)}

Provide your analysis as JSON with:
- score (0-100): likelihood of misinformation
- tags (array): descriptive tags like "unverified_claim", "misleading_statistics", etc.
- rationale (string): 1-2 sentences explaining the score
- fact_check_questions (array): 3 specific questions to verify claims

Respond with ONLY valid JSON, no other text."""

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM JSON response"""
        import json

        # Try to extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())

        # Fallback
        return {
            'score': 50,
            'tags': ['llm_parse_error'],
            'rationale': 'Failed to parse LLM response',
            'fact_check_questions': []
        }
