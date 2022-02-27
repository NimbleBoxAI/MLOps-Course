"""This file contains the code for question answering system

"""

from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import torch

model_name = "deepset/roberta-base-squad2"
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


def get_answer_using_pipeline(question: str, context: str) -> str:
    """Retrieves the answer for the question from the context provided using huggingface pipeline

    Args:
        question (str): String indicating the question.
        context (str): String indicating the context

    Returns:
        str: Answer from the context.
    """
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    QA_input = {
        'question': 'Why is model conversion important?',
        'context': 'The option to convert models between FARM and transformers gives freedom to the user and let people easily switch between frameworks.'
    }
    answer = nlp(QA_input)
    return answer


def get_answer(question: str, context: str) -> str:
    """Retrieves the answer for the question from the context provided.

    Args:
        question (str): String indicating the question.
        context (str): String indicating the context

    Returns:
        str: Answer from the context.
    """
    encoding = tokenizer.encode_plus(question, context)
    input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

    output = model(torch.tensor([input_ids]), attention_mask=torch.tensor([attention_mask]))

    ans_tokens = input_ids[torch.argmax(output['start_logits']) : torch.argmax(output['end_logits']) + 1]
    answer_tokens = tokenizer.convert_ids_to_tokens(ans_tokens , skip_special_tokens=True)
    answer = tokenizer.convert_tokens_to_string(answer_tokens)
    return answer


if __name__ == "__main__":
    context = 'The option to convert models between FARM and transformers gives freedom to the user and let people easily switch between frameworks.'
    question = "Why is model conversion important?"

    answer = get_answer(question, context)
    print ("\nQuestion: ", question)
    print ("\nContext: ", context)
    print ("\nAnswer: ", answer)