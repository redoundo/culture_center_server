FROM python:3.12



RUN pip install python-dotenv mysql-connector-python torch transformers tqdm numpy scikit-learn huggingface-hub


ENV SAVEPATH=ml_model.pth
ENV DATALOACTION=train_sample.json

ENV DATABASE_NAME=culture-centers
ENV DATABASE_USERNAME=culturecenter

CMD ["python", "mlprocess.py"]