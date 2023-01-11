# import requests
# from PIL import Image
# import streamlit as st
# import json

# def generate_image():
#     api_key = st.text_input("Please enter OpenAI API key", "")
#     image_url = st.text_input("Please enter image url", "")
#     img = Image.open(requests.get(image_url, stream=True).raw)
#     st.image(img, caption='Original Image', use_column_width=True)
#     prompt = st.text_input("Please enter the image you would like to generate", "")
#     if api_key and prompt:
#         headers = {
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {api_key}"
#         }
#         data = """
#         {
#             """
#         data += f'"prompt": "{prompt}",'
#         data += f'"model": "image-alpha-001",'
#         data += """
#             "num_images":1,
#             "size":"1024x1024",
#             "response_format":"url"
#         }
#         """

#         resp = requests.post('https://api.openai.com/v1/images/generations', headers=headers, data=data)

#         if resp.status_code != 200:
#             raise ValueError("Failed to generate image "+resp.text)
#         response_text = json.loads(resp.text)
#         image_url = response_text['data'][0]['url']
#         img = Image.open(requests.get(image_url, stream=True).raw)
#         st.image(img, caption='Generated Image', use_column_width=True)
#     else:
#         st.warning("API key or prompt is missing")

# if __name__=="__main__":
#     st.title("DALL-E 2 Image Generator")
#     generate_image()
import streamlit as st
import requests
from PIL import Image

dalle_api_key = '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'

def generate_image(prompt):
    # Use DALL-E API to generate image
    url = f"https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {dalle_api_key}"
    }
    data = {
      "model": "image-alpha-001",
      "prompt": prompt,
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        raise ValueError("Failed to generate image "+response.text)
    image_url = response.json()['data'][0]['url']
    return image_url

st.set_page_config(page_title="DALL-E Image Generator", page_icon=":camera:", layout="wide")

st.title("DALL-E Image Generator")

prompt = st.text_input("Enter a description for the image you want to generate:")
if prompt:
    image_url = generate_image(prompt)
    response = requests.get(image_url)
    img = Image.open(response.content)
    st.image(img, caption="Generated Image", use_column_width=True)
