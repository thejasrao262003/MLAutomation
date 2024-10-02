import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import seaborn as sns
import base64
from flask import Flask, request, jsonify
app = Flask(__name__)
@app.route('/visualisation', methods=['GET', 'POST'])
def handleVisualisation():
    data = request.get_json()
    selectedOption = data['selected_option']
    print(selectedOption)
    df = pd.DataFrame(data['data'])
    if selectedOption == "Correlation matrix":
        image = drawCorr(df)
    elif selectedOption in ["Histogram", "Box Plot"]:
        feature = data['feature']
        if selectedOption == "Histogram":
            image = drawHistograms(df, feature)
        else:
            image = drawBoxPlots(df, feature)
    else:
        feature1 = data['feature1']
        feature2 = data["feature2"]
        image = drawPairPlots(df, feature1, feature2)

    img_str = convertImageToBase64(image)
    return jsonify({'image': img_str})

def drawHistograms(df, feature1:str):
    plt.figure(figsize=(10, 8), dpi=500)
    fig, ax = plt.subplots()
    df.hist(column=f"{feature1}", ax=ax)
    ax.set_title(f"Histogram of {feature1}")
    ax.set_xlabel("Values")
    ax.set_ylabel("Frequency")
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    image = Image.open(buf)
    return image


def drawBoxPlots(df, feature1:str):
    plt.figure(figsize=(10, 8), dpi=500)
    df.boxplot(column=feature1)
    plt.title(f"Box Plot for {feature1} feature")
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    image = Image.open(buf)
    return image

def drawPairPlots(df, feature1:str, feature2:str):
    plt.figure(figsize=(10, 8), dpi=500)
    sns.pairplot(df, vars=[feature1, feature2])
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    image = Image.open(buf)
    return image

def drawCorr(df):
    plt.figure(figsize=(10, 8), dpi=500)
    corr = df.corr(method="pearson")
    sns.heatmap(corr, annot=True, fmt=".2f", linewidth=.5)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    image = Image.open(buf)
    return image

def convertImageToBase64(image: Image.Image) -> str:
    """Convert a PIL Image to a Base64 string."""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5002)