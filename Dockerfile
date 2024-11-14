#抓image
FROM python:3.11

#進入資料夾，如不存在，Dockerfile會自動建立
WORKDIR /code

#從自己電腦的資料夾中 複製資料到container
COPY ./requirements.txt /code/requirements.txt

#執行指令pip install
#--no-cache-dir 防止container被cache影響
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

#啟動API，等於 fastapi run app/main.py --port 80
CMD [ "fastapi", "run", "app/main.py", "--port", "80" ]