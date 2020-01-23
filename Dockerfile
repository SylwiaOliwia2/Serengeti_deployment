FROM python:3.6-slim
WORKDIR /deploy/
COPY requirements.txt /deploy/
RUN pip install -r requirements.txt

COPY static /deploy/static
COPY templates /deploy/templates
COPY app.py /deploy/
COPY predict.py /deploy/
COPY model.pkl /deploy/

EXPOSE 5000
RUN echo $(find)
ENTRYPOINT ["python", "app.py"]
