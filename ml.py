from transformers import pipeline

bot = pipeline("text-generation", model="gpt2")

while True:
    question = input("You: ")

    if question.lower() == "exit":
        break

    prompt = "\nQuestion: " + question + "\nAnswer:"

    result = bot(prompt, max_length=120, num_return_sequences=1)

    answer = result[0]["generated_text"].split("Answer:")[-1]

    print("Bot:", answer.strip())
    print()