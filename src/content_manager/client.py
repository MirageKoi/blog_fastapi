import google.generativeai as genai
import os



def experiment_feature(key: str):
    
    genai.configure(api_key=key)



    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Write a story about a magic backpack.")
    # print(response.text)

    return response