#!/bin/bash
set -x
echo "=== Starting app ==="
echo "PORT is: $PORT"
echo "Python version:"
python --version
echo "=== Testing imports ==="
python -c "import flask; print('Flask OK')"
python -c "import cv2; print('OpenCV OK')"
python -c "import spacy; print('spaCy OK')"
python -c "import pytesseract; print('pytesseract OK')"
echo "=== Checking tesseract binary ==="
which tesseract || echo "tesseract NOT FOUND"
tesseract --version || echo "tesseract version check failed"
echo "=== Starting gunicorn ==="
exec gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 1 --log-level debug main:app