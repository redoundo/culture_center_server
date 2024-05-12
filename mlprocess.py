from mysqlml import MySql
from trainmodel import TrainModel
from classifyingmodel import Classifying

label_number: int = 35

if __name__ == "__main__":
    my_sql: MySql = MySql()
    train_model: TrainModel = TrainModel(num=label_number)
    new_data: list | None = my_sql.classify_examples()
    if new_data is not None:
        classify_model: Classifying = Classifying(label_num=label_number)
        original, classified = classify_model.classify(new_data=new_data)
        my_sql.insert_classified_data(init_datas=original, classified_datas=classified)

    my_sql.connection.close()
