import requests
from PIL import Image
import streamlit as st
import json

def generate_image():
    api_key = st.text_input("Please enter OpenAI API key", "")
    image_url = st.text_input("Please enter image url", "")
    img = Image.open(requests.get(image_url, stream=True).raw)
    st.image(img, caption='Original Image', use_column_width=True)
    prompt = st.text_input("Please enter the image you would like to generate", "")
    if api_key and prompt:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = """
        {
            """
        data += f'"prompt": "{prompt}",'
        data += f'"model": "image-alpha-001",'
        data += """
            "num_images":1,
            "size":"1024x1024",
            "response_format":"url"
        }
        """

        resp = requests.post('https://api.openai.com/v1/images/generations', headers=headers, data=data)

        if resp.status_code != 200:
            raise ValueError("Failed to generate image "+resp.text)
        response_text = json.loads(resp.text)
        image_url = response_text['data'][0]['url']
        img = Image.open(requests.get(image_url, stream=True).raw)
        st.image(img, caption='Generated Image', use_column_width=True)
    else:
        st.warning("API key or prompt is missing")

if __name__=="__main__":
    st.title("DALL-E 2 Image Generator")
    generate_image()
