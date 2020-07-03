FROM python:3.8.2
WORKDIR /chal
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY chal.py /chal
EXPOSE 8765
CMD ["python","chal.py"]