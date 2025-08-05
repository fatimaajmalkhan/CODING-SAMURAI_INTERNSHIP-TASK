import streamlit as st
import torch
from torchvision import models, transforms
from PIL import Image
import urllib.request
import os
st.set_page_config(page_title="Image Classifier", layout="centered")
st.title("Image Classifier")
st.write("Please upload the picture here :)")
@st.cache_resource
def load_model():
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
    model.eval()
    return model
model = load_model()
@st.cache_data
def load_labels():
    url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
    labels_path = "labels.txt"
    if not os.path.exists(labels_path):
        urllib.request.urlretrieve(url, labels_path)
    with open(labels_path, "r") as f:
        categories = [s.strip() for s in f.readlines()]
    return categories
categories = load_labels()
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225])
])
uploaded_file = st.file_uploader("Please choose an image", type=["jpg", "jpeg", "png", "webp"])
if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_column_width=True)
    except:
        st.error("Unable to open the image... Please upload a valid image file :)")
    else:
        with st.spinner("Analyzing image..."):
            try:
                input_tensor = transform(image).unsqueeze(0)
                with torch.no_grad():
                    output = model(input_tensor)
                    probs = torch.nn.functional.softmax(output[0], dim=0)
                    top5_prob, top5_catid = torch.topk(probs, 5)
                st.success("Prediction complete :)")
                st.markdown("Top 5 Predictions:")
                for i in range(top5_prob.size(0)):
                    label = categories[top5_catid[i]]
                    confidence = top5_prob[i].item()
                    st.write(f"**{i+1}. {label}** — {confidence*100:.2f}%")
                    st.progress(min(int(confidence*100), 100))
            except Exception as e:
                st.error(f"Error during prediction: {str(e)}")
else:
    st.warning("Please upload a picture ")
