# 📇 Business Card OCR — AI-Powered Information Extractor

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Flask](https://img.shields.io/badge/Flask-2.0.2-lightgrey)
![spaCy](https://img.shields.io/badge/spaCy-3.1.3-09a3d5)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Spaces-FFD21E)
![License](https://img.shields.io/badge/License-MIT-green)

> 🚀 **Live Demo:** [https://subrat05-business-card-ocr.hf.space](https://subrat05-business-card-ocr.hf.space)

An end-to-end Machine Learning web application that scans business cards and automatically extracts key information using **Computer Vision + OCR + Named Entity Recognition (NER)**.

Built during my internship at **IPR (Institute for Plasma Research)** and later deployed live with full bug fixes and cloud deployment.

---

## 🎯 Features

- 📸 Upload any business card image (JPG, PNG, JPEG)
- 🔍 Auto-detects document corners using OpenCV
- ✋ Manually adjust corners by dragging corner points
- 🔄 Perspective transform to flatten & enhance the card
- 📝 OCR-powered text extraction using Tesseract
- 🧠 Custom-trained spaCy NER model to extract:
  - 👤 **NAME** — Person's name
  - 🏢 **ORG** — Organization / Company
  - 💼 **DES** — Designation / Job Title
  - 📞 **PHONE** — Phone numbers
  - 📧 **EMAIL** — Email address
  - 🌐 **WEB** — Website URL
- 🟩 Bounding boxes drawn around detected entities
- 🔁 Scan multiple cards easily

---

## 🖥️ Demo

| Step | Screenshot |
|------|-----------|
| Upload Card | Corner detection with draggable green points |
| Extract Text | Bounding boxes + entity table |

> ⚠️ **Note:** For best results, use **high quality, well-lit photos** with dark text on light background. The NER model is still being improved with more training data.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.9 | Core language |
| Flask | Web framework / Backend server |
| OpenCV | Image processing & document scanning |
| Tesseract OCR | Text extraction from images |
| spaCy | Custom NER model for entity recognition |
| pytesseract | Python wrapper for Tesseract |
| pandas + numpy | Data processing |
| Docker | Containerization with system dependencies |
| Hugging Face Spaces | Free cloud deployment |
| Git + Git LFS | Version control with large model files |

---

## 📁 Project Structure

```
Business-Card-OCR/
├── 3_app/                          ← Main deployable app
│   ├── main.py                     ← Flask routes & app logic
│   ├── predictions.py              ← OCR + NER prediction logic
│   ├── utils.py                    ← Image processing utilities
│   ├── settings.py                 ← Configuration & paths
│   ├── requirements.txt            ← Python dependencies
│   ├── Dockerfile                  ← Docker configuration
│   ├── Procfile                    ← Process file for deployment
│   ├── README.md                   ← HF Space configuration
│   ├── output/
│   │   └── model-best/             ← Trained spaCy NER model
│   ├── templates/
│   │   ├── index.html              ← Base template
│   │   ├── scanner.html            ← Upload & scan page
│   │   └── predictions.html       ← Results page
│   └── static/
│       ├── js/doc_scan.js          ← Canvas & corner detection JS
│       └── images/                 ← Static assets
├── 1_BusinnesCardNAR/              ← NER model training notebooks
├── 2_DocumentScanner/              ← Document scanner experiments
└── render.yaml                     ← Render deployment config
```

---

## ⚙️ How It Works

```
📸 Upload Image
      ↓
🔍 OpenCV detects 4 corners
      ↓
✋ User adjusts corners manually (drag & drop)
      ↓
🔄 Perspective transform flattens the card
      ↓
🖼️ Image preprocessing (upscale, contrast, sharpen)
      ↓
📝 Tesseract OCR extracts all text
      ↓
🧠 spaCy NER model classifies entities
      ↓
📊 Results displayed with bounding boxes + table
```

---

## 🚀 Run Locally

### Prerequisites
- Python 3.9
- Tesseract OCR installed on your system
  - Windows: [Download here](https://github.com/UB-Mannheim/tesseract/wiki)
  - Linux: `sudo apt-get install tesseract-ocr`
  - Mac: `brew install tesseract`

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/SubratGupta0506/Business-Card-OCR.git
cd Business-Card-OCR/3_app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python main.py
```

Open your browser at `http://localhost:5000`

---

## 🐳 Run with Docker

```bash
# Build the image
docker build -t business-card-ocr .

# Run the container
docker run -p 7860:7860 business-card-ocr
```

Open your browser at `http://localhost:7860`

---

## ☁️ Deployment

This app is deployed on **Hugging Face Spaces** using Docker.

Key deployment challenges solved:
- ✅ Installed Tesseract OCR as system package inside Docker
- ✅ Fixed pydantic + spaCy + thinc version conflicts
- ✅ Handled binary model files with Git LFS
- ✅ Used `/tmp` storage for file handling on serverless cloud
- ✅ Added image preprocessing for better OCR accuracy

---

## 📸 Image Tips for Best Results

| ✅ Do This | ❌ Avoid This |
|---|---|
| High resolution photo | Blurry or low quality image |
| Dark text on white/light background | Heavily designed colorful cards |
| Card fully visible, no cutoffs | Partial card in frame |
| Good lighting, no shadows | Dark or shadowy lighting |
| Flat card, no bending | Folded or bent cards |

---

## 🔮 Future Improvements

- [ ] Retrain NER model with 100+ labeled examples
- [ ] Support for multi-language business cards
- [ ] Export extracted data to CSV / vCard format
- [ ] Mobile-friendly UI improvements
- [ ] Batch processing of multiple cards
- [ ] Integration with CRM systems

---

## 👨‍💻 Author

**Subrat Gupta**
- 🌐 Live App: [https://subrat05-business-card-ocr.hf.space](https://subrat05-business-card-ocr.hf.space)
- 💼 LinkedIn: [linkedin.com/in/your-profile](https://linkedin.com/in/your-profile)
- 🐙 GitHub: [github.com/SubratGupta0506](https://github.com/SubratGupta0506)

---

## 🏛️ Acknowledgements

- Built during internship at **IPR (Institute for Plasma Research)**
- OCR powered by [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- NER powered by [spaCy](https://spacy.io/)
- Deployed on [Hugging Face Spaces](https://huggingface.co/spaces)

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify and distribute!

---

⭐ **If you find this project useful, please give it a star!** ⭐
