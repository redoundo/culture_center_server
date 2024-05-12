FROM python:3.11

RUN pip install python-dotenv
RUN pip install mysql-connector-python
RUN pip install torch
RUN pip install transformers
RUN pip install tqdm
RUN pip install numpy
RUN pip instal scikit-learn
RUN pip install huggingface-hub


ENV SAVEPATH=ml_model.pth
ENV DATALOACTION=train_sample.json

ENV DATABASE_NAME=culture-centers
ENV DATABASE_USERNAME=culturecenter

ENTRYPOINT ["mlprocess.py"]