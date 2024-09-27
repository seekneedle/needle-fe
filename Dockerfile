FROM python:3.10.14

RUN mkdir -p /home/needle-fe

COPY requirements.txt /home/needle-fe

WORKDIR /home/needle-fe

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

COPY . /home/needle-fe

CMD ["streamlit", "run", "webui.py"]
