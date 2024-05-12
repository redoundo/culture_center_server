import torch, json
from torch import nn
from torch.utils.data import DataLoader
from torch.optim import AdamW
from tqdm import notebook
from BERTClasses import BERTDataset, BERTClassifier
from transformers.optimization import get_cosine_schedule_with_warmup
from transformers import AutoModel, AutoTokenizer, AutoConfig, PreTrainedTokenizerFast
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
import os

load_dotenv()


class TrainModel:
    dataLocation: str = os.environ.get('DATALOACTION')
    savePath: str = os.environ.get('SAVEPATH')

    tokenizer: PreTrainedTokenizerFast
    model: any
    vocab: dict
    data: list

    testLoader: any
    trainLoader: any

    device = torch.device("cuda:0")
    maxLen: int = 64
    batchSize: int = 64
    warmupRatio: float = 0.1
    numEpochs: int = 20
    maxGradNorm: int = 1
    logInterval: int = 200
    learningRate = 5e-5
    labels: int = 76

    def __init__(self, num: int):
        self.tokenizer = AutoTokenizer.from_pretrained("skt/kobert-base-v1", use_fast=False)

        config = AutoConfig.from_pretrained("skt/kobert-base-v1")
        config.num_labels = num
        config.return_dict = False
        self.model = AutoModel.from_pretrained("skt/kobert-base-v1", config=config)

        self.vocab = self.tokenizer.get_vocab()
        self.data = self.get_data()
        return

    def set_data_loader(self):
        """
        모델 훈련과 훈련이 얼마나 잘 되었는지 테스트 하기 위해 라벨링 된 내용을 테스트 용, 훈련 용으로 나눈다.
        :return:
        """
        train, test = train_test_split(self.data, test_size=0.3, shuffle=True, random_state=34)

        data_train = BERTDataset(train, 0, 1, self.tokenizer, self.vocab, self.maxLen, True, False)
        data_test = BERTDataset(test, 0, 1, self.tokenizer, self.vocab, self.maxLen, True, False)

        self.trainLoader = DataLoader(data_train, batch_size=self.batchSize, num_workers=5)
        self.testLoader = DataLoader(data_test, batch_size=self.batchSize, num_workers=5)
        return

    def get_data(self) -> list:
        """
        라벨링한 내용을 가져 온다. [["제목",20],["제목",11]...] 같은 형식으로 self.data 에 저장 된다.
        :return:
        """
        with open(self.dataLocation, "r", encoding="utf-8-sig") as j:
            data = json.load(j)

        dataset: list = []
        for arr in data:
            if arr["Classify"] is not None:
                if type(arr["Classify"]) is int:
                    dataset.append([arr["Title"], arr["Classify"]])
                else:
                    continue
            else:
                continue
        return dataset

    def classify_model_else(self):
        model = BERTClassifier(self.model, num_classes=self.labels, dr_rate=0.5).to(self.device)

        no_decay = ['bias', 'LayerNorm.weight']
        optimizer_grouped_parameters = [
            {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
             'weight_decay': 0.01},
            {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
        ]

        optimizer = AdamW(optimizer_grouped_parameters, lr=self.learningRate)
        loss_fn = nn.CrossEntropyLoss()

        t_total = len(self.trainLoader) * self.numEpochs
        print("t_total={0}".format(str(t_total)))
        warmup_step = int(t_total * self.warmupRatio)

        scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=warmup_step, num_training_steps=t_total)
        return model, optimizer, loss_fn, scheduler

    def train_model(self):

        train_history = []
        test_history = []
        loss_history = []
        model, optimizer, loss_fn, scheduler = self.classify_model_else()
        for e in range(self.numEpochs):
            train_acc = 0.0
            test_acc = 0.0
            model.train()
            for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(notebook.tqdm(self.trainLoader)):
                optimizer.zero_grad()
                token_ids = token_ids.long().to(self.device)
                segment_ids = segment_ids.long().to(self.device)
                valid_length = valid_length
                label = label.long().to(self.device)
                out = model(token_ids, valid_length, segment_ids)
                print("batch_id=", batch_id)
                print(label.shape, out.shape)
                loss = loss_fn(out, label)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), self.maxGradNorm)
                optimizer.step()
                scheduler.step()  # Update learning rate schedule
                train_acc += self.calc_accuracy(out, label)
                if batch_id % self.logInterval == 0:
                    print(
                        "epoch {} batch id {} loss {} train acc {}".format(e + 1, batch_id + 1, loss.data.cpu().numpy(),
                                                                           train_acc / (batch_id + 1)))
                    train_history.append(train_acc / (batch_id + 1))
                    loss_history.append(loss.data.cpu().numpy())
                print("epoch {} train acc {}".format(e + 1, train_acc / (batch_id + 1)))
                train_history.append(train_acc / (batch_id+1))

            model.eval()
            for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(notebook.tqdm(self.testLoader)):
                token_ids = token_ids.long().to(self.device)
                segment_ids = segment_ids.long().to(self.device)
                valid_length = valid_length
                label = label.long().to(self.device)
                out = model(token_ids, valid_length, segment_ids)
                test_acc += self.calc_accuracy(out, label)
                print("epoch {} test acc {}".format(e + 1, test_acc / (batch_id + 1)))
                test_history.append(test_acc / (batch_id + 1))

        torch.save(model.state_dict(), self.savePath)
        return

    def calc_accuracy(self, x, y):
        max_vals, max_indices = torch.max(x, 1)
        train_acc = (max_indices == y).sum().data.cpu().numpy() / max_indices.size()[0]
        return train_acc
