import os
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from helpers import create_logger

logger = create_logger(project_name="qa_model", level="INFO", json_logging=True)

model_name = "deepset/roberta-base-squad2"
logger.info(f"Loading model: {model_name}")
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
model_dir = os.path.join(root_dir, 'models')
save_path = os.path.join(model_dir, model_name)
print(f"Saving models in: {model_dir}")
print(f"Saving model: {model_name} in {save_path}")

tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)