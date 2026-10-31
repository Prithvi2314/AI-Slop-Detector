
from detector import detect_text
from datasets import load_dataset


test_data = [
    # ---------------- HUMAN ----------------

    {
        "text": "bro I completely forgot to reply to you yesterday 😂",
        "label": "human"
    },
    {
        "text": "Hey, can you send me the notes? I missed class today.",
        "label": "human"
    },
    {
        "text": "ugh my internet is so slow today 😭",
        "label": "human"
    },
    {
        "text": "I was gonna study but ended up watching reels for two hours lol.",
        "label": "human"
    },
    {
        "text": "Can you call me when you're free? I need to ask you something.",
        "label": "human"
    },
    {
        "text": "I don't really agree with that tbh, but I understand what you're saying.",
        "label": "human"
    },
    {
        "text": "Yesterday I went to the market and somehow came back with a bunch of snacks I never planned to buy.",
        "label": "human"
    },
    {
        "text": "Honestly I was so tired last night that I just ate dinner and went straight to bed.",
        "label": "human"
    },
    {
        "text": "My exam is next week and I still haven't finished half of the syllabus.",
        "label": "human"
    },
    {
        "text": "The weather was nice today so I went outside for a while.",
        "label": "human"
    },


    # ---------------- AI ----------------

    {
        "text": "In today's rapidly evolving society, effective communication plays a crucial role in fostering meaningful relationships and achieving long-term success.",
        "label": "ai"
    },
    {
        "text": "Artificial intelligence has transformed numerous industries by enabling organizations to automate tasks, improve efficiency, and make data-driven decisions.",
        "label": "ai"
    },
    {
        "text": "Maintaining a healthy lifestyle requires a balanced combination of nutritious food, regular physical activity, adequate sleep, and effective stress management.",
        "label": "ai"
    },
    {
        "text": "Technology continues to shape the modern world by providing individuals with innovative tools that enhance productivity, communication, and access to information.",
        "label": "ai"
    },
    {
        "text": "Developing effective study habits can significantly improve academic performance by helping students manage their time, retain information, and remain focused on their educational objectives.",
        "label": "ai"
    },
    {
        "text": "Honestly, I think the easiest way to approach this problem is to break it down into smaller and more manageable steps.",
        "label": "ai"
    },
    {
        "text": "If you're feeling overwhelmed, taking a short break can help you return to the task with greater clarity and concentration.",
        "label": "ai"
    },
    {
        "text": "There are several factors to consider when making an important decision, including the available options, potential consequences, and your long-term goals.",
        "label": "ai"
    },
    {
        "text": "Learning consistently over time is generally more effective than attempting to memorize a large amount of information in a single session.",
        "label": "ai"
    },
    {
        "text": "A balanced approach can help individuals improve their productivity while also maintaining their overall well-being and reducing unnecessary stress.",
        "label": "ai"
    }
]

# dataset = load_dataset(
#     "abhi099k/machine-and-human-text",
#     split="train[:50]"
# )

# test_data = [
#     {
#         "text": item["text"],
#         "label": str(item["label"])
#     }
#     for item in dataset
# ]

print("Dataset loaded:", len(test_data), "examples")



texts = [item["text"] for item in test_data]

results = detect_text(texts)

print(results)

TP = 0
TN = 0 
FP = 0
FN = 0

for item , result in zip(test_data, results):
    actual = item["label"]
    predicted = result["label"]
    score = result["score"]
    # treating ai as a positive class

    if actual == "ai" and predicted == "ai":
        TP += 1

    elif actual =="human" and predicted == "human":
        TN += 1

    elif actual == "human" and predicted == "ai":
        FP += 1

    elif actual == "ai" and predicted == "human":
        FN += 1


    if actual != predicted:
        print("\n--- MISCLASSIFIED ---")
        print("Text:", item ["text"])
        print("Actual:" , actual)
        print("Predicted:", predicted)
        print("confidence:", score)


print("TP:", TP)
print("TN:", TN)
print("FP:", FP)
print("FN:", FN)


accuracy = (TP + TN) / (TP + TN + FP + FN)

precision = TP /(TP + FP) if (TP + FP) > 0 else 0

recall = TP /(TP + FN) if (TP + FN) > 0 else 0

f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0



print("Accuracy:" , accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)