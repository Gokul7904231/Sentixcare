FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y git git-lfs wget libgl1-mesa-glx libglib2.0-0

# Copy project first
COPY . .

# Create weights folder BEFORE downloading
RUN mkdir -p emotion/weights

# Download weights
RUN wget -O emotion/weights/yolov7-tiny.pt https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-tiny.pt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 7860

CMD ["streamlit", "run", "src/app.py", "--server.port=7860", "--server.address=0.0.0.0"]