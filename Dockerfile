# Dockerfile, Image, Container
FROM python:3.8
WORKDIR /app
ADD *task* .
COPY data/ data/
RUN pip install tabulate pandas

RUN ["chmod", "+x", "run_tasks.sh"]
ENTRYPOINT ["./run_tasks.sh"]