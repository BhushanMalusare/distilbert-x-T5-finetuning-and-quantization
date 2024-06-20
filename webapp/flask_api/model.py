import os
import config
from transformers import AutoTokenizer, pipeline
from optimum.onnxruntime import ORTModelForSequenceClassification
from optimum.onnxruntime import ORTModelForSeq2SeqLM

# Loading models and tokenizers
distil_bert_tokenizer = AutoTokenizer.from_pretrained(config.DISTIL_BERT_TOKENIZER_CHECKPOINT)
distil_bert_model =  ORTModelForSequenceClassification.from_pretrained(config.DISTIL_BERT_MODEL_CHECKPOINT)
T5_tokenizer = AutoTokenizer.from_pretrained(config.T5_TOKENIZER_CHECKPOINT)
T5_model = ORTModelForSeq2SeqLM.from_pretrained(config.T5_MODEL_CHECKPOINT)

def get_class_names():
    return distil_bert_model.config.id2label


# Define the intent labels
def predict_intent(text):

    classifier = pipeline(
        "text-classification",
        model=distil_bert_model,
        tokenizer=distil_bert_tokenizer,
    )

    # Example inference
    result = classifier(text)
    if result[0]["score"] > 0.5:
        return result[0]["label"]
    else:
        return False


# Define the summarization function
def summarize_text(text):
    summarizer = pipeline(
        "summarization",
        model=T5_model,
        tokenizer=T5_tokenizer,
    )

    # Example inference
    result = summarizer(text)
    return result[0]["summary_text"]