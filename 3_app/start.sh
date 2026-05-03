#!/bin/bash
export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata
exec gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 1 main:app