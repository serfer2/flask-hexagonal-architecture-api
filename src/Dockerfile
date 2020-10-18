FROM python:3.8
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt \
    && mkdir -p /usr/src/app/tmp
VOLUME ["/usr/src/app/tmp"]
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
EXPOSE 8000
CMD ["python", "controller/app.py"]
