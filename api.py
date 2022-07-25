#library imports
import streamlit as st
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

#loading the model

model_name = 'tuner007/pegasus_paraphrase'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
loaded_model = torch.load("model2.pth")

def get_response(input_text,num_return_sequences):
  batch = tokenizer.prepare_seq2seq_batch([input_text],truncation=True,padding='longest',max_length=60, return_tensors="pt").to(torch_device)
  translated = loaded_model.generate(**batch,max_length=60,num_beams=10, num_return_sequences=num_return_sequences, temperature=1.5)
  tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
  return tgt_text


st.title("Paraphraser")

input_text = st.text_input("Enter text")
submit = st.button('Paraphrase')

if submit:
    if input_text is not None:
        suggestions = get_response(input_text,1)
        
        st.title(str(suggestions))