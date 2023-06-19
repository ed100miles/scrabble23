FROM ubuntu:latest

COPY . .

RUN apt update && apt upgrade -y
RUN apt install python3 -y && apt install pip -y 
RUN pip install numpy uvicorn fastapi

EXPOSE 80

CMD ["uvicorn", "api:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
