if __name__ == "__main__":
    from openai import OpenAI
    from os import getenv
    import private
    import os
    import json
    import tqdm

    # gets API Key from environment variable OPENAI_API_KEY
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=private.OPENROUTER_API_KEY,
    )


    def gen_fact(subject: str, model: str):
        completion = client.chat.completions.create(
        model=model,
        messages=[
            {
            "role": "user",
            "content": f"Please tell me a fun four-sentence fact about {subject}. No greetings or confirmation, just fact.",
            },
        ],
        )
        return completion.choices[0].message.content

    def gen_facts(subjects: list[str], dest_file: str, model: str):
        current: dict[str, str] = {}
        if os.path.exists(dest_file):
            with open(dest_file, "r", encoding="utf-8") as file:
                current = json.load(file)
                
        missing = [subject for subject in subjects if subject not in current]
        for subject in tqdm.tqdm(missing):
            fact = gen_fact(subject, model)
            current[subject] = fact
            with open(dest_file, "w", encoding="utf-8") as file:
                json.dump(current, file)
        return current

    
    with open("popular_pages.txt", "r", encoding="utf-8") as file:
        pages = [x.strip() for x in file.readlines()]
    # print(gen_fact(pages[0]))
    
    # gen_facts(pages[:500], "facts_deepseek-chat.json", "deepseek/deepseek-chat")
    # gen_facts(pages[:500], "facts_claude-3.5-sonnet.json", "anthropic/claude-3.5-sonnet")
    gen_facts(pages[:500], "facts_gpt-4o.json", "openai/gpt-4o")
    