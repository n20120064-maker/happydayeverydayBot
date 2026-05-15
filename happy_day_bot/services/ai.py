from openai import AsyncOpenAI


CRISIS_PHRASES = (
    "ничего не получилось",
    "я устала",
    "я плохая",
    "всё плохо",
    "все плохо",
    "ненавижу себя",
)

CRISIS_RESPONSE = (
    "Похоже, тебе сейчас правда тяжело. Давай сегодня не будем требовать от себя невозможного. "
    "Иногда уже то, что ты выдержала день, - это сила."
)


class AIService:
    def __init__(self, api_key: str, model: str) -> None:
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "https://local.happy-day-bot",
                "X-Title": "Happy Day Telegram Bot",
            },
        )
        self.model = model

    @staticmethod
    def has_crisis_phrase(text: str) -> bool:
        normalized = text.lower()
        return any(phrase in normalized for phrase in CRISIS_PHRASES)

    async def generate_diary_response(
        self,
        name: str,
        style: str,
        mood: str,
        wins: str,
        gratitude: str,
        difficulties: str,
        support_type: str,
    ) -> str:
        combined = "\n".join([mood, wins, gratitude, difficulties, support_type])
        if self.has_crisis_phrase(combined):
            return CRISIS_RESPONSE

        prompt = f"""
Ты - Happy Day, теплый AI-дневник силы. Поддержи пользователя на основе его ответов.
Заметь его успехи, благодарности и устойчивость. Не обесценивай трудности.
Пиши по-женски мягко, коротко, искренне, без пафоса.
Не используй токсичную мотивацию и фразы вроде "просто думай позитивно".

Имя пользователя: {name}
Стиль общения: {style}
Как прошел день: {mood}
Что получилось: {wins}
Благодарность: {gratitude}
Что было сложным: {difficulties}
Пользователь хочет услышать: {support_type}
""".strip()

        return await self._chat(prompt, fallback=CRISIS_RESPONSE)

    async def generate_week_summary(self, name: str, style: str, entries_text: str) -> str:
        prompt = f"""
Ты - Happy Day, теплый AI-дневник силы. Сделай короткий бережный итог недели для пользователя.
Структура:
Главные победы:
Повторяющиеся благодарности:
Что было сложным:
Мягкий вывод:

Не обесценивай трудности. Пиши коротко, тепло и конкретно.
Имя пользователя: {name}
Стиль общения: {style}
Записи недели:
{entries_text}
""".strip()

        return await self._chat(
            prompt,
            fallback="Эта неделя уже содержит важное: ты замечала себя, свои усилия и то, что помогало держаться. Это правда ценно.",
        )

    async def _chat(self, prompt: str, fallback: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Ты бережный русскоязычный дневник поддержки Happy Day."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=500,
            )
            text = response.choices[0].message.content
            return text.strip() if text else fallback
        except Exception:
            return fallback
