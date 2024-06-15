from BERTClasses import BERTDataset
from torch.utils.data import DataLoader
from dotenv import load_dotenv
from multiprocessing import freeze_support
from transformers import AutoTokenizer, AutoConfig, PreTrainedTokenizerFast, AutoModel
import numpy as np
from collections import OrderedDict
import torch
import json

load_dotenv()


class Classifying:
    # savePath: str = os.getenv('SAVEPATH')
    savePath: str = "C:/Users/admin/mlcicd/ml_model.pth"
    dataLocation: str = "C:/Users/admin/mlcicd/train_sample.json"
    model: any
    tokenizer: PreTrainedTokenizerFast
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    vocab: dict[str, int]
    maxLen: int = 64
    batchSize: int = 64

    def __init__(self, label_num: int):
        config = AutoConfig.from_pretrained("skt/kobert-base-v1")
        config.num_labels = label_num
        config.return_dict = False
        self.model = torch.load(self.savePath)
        # self.model = AutoModel.from_pretrained("skt/kobert-base-v1", config=config)
        # self.model.to(self.device)
        # state_dict = self.delete_prefix(torch.load(self.savePath))
        # self.model.load()
        # self.model.load_state_dict(state_dict=state_dict)
        self.tokenizer = AutoTokenizer.from_pretrained("skt/kobert-base-v1", use_fast=False, config=config)

        self.vocab = self.tokenizer.get_vocab()
        return

    def delete_prefix(self, state):
        new_state_dict: OrderedDict = OrderedDict()
        for key in list(state.keys()):
            new_state_dict[key.replace("bert.", "")] = state[key]
        return new_state_dict

    def data_to_arr(self, data: list[dict]) -> list:
        """
        라벨링한 내용을 가져 온다. [["제목",20],["제목",11]...] 같은 형식으로 self.data 에 저장 된다.
        :return:
        """
        dataset: list = []
        for arr in data:
            if arr["Classify"] is not None:
                if type(arr["Classify"]) is int:
                    dataset.append([arr["title"], arr["Classify"]])
                else:
                    continue
            else:
                continue
        return dataset

    def classify(self, new_data: list) -> tuple | None:
        if len(new_data) < 1:
            return None
        else:
            to_dataset = BERTDataset(self.data_to_arr(new_data), 0, 1, self.tokenizer, self.vocab, self.maxLen, True, False)
            dataloader = DataLoader(to_dataset, batch_size=self.batchSize, num_workers=5)

            self.model.eval()
            classified = []

            for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(dataloader):
                freeze_support()
                token_ids = token_ids.long().to(self.device)
                segment_ids = segment_ids.long().to(self.device)

                valid_length = valid_length
                label = label.long().to(self.device)
                print("batch_id=", batch_id)  # 아마 testset의 index일거라 추측
                out = self.model(token_ids, valid_length, segment_ids)

                for i in out:
                    logits = i
                    logits = logits.detach().cpu().numpy()
                    print(np.argmax(logits))  # 임시로 넣은 0대신 라벨 12가 나옴
                    classified.append(np.argmax(logits))

        return new_data, classified

    # def return_target_category(self, new_data: list[LectureType], classified: list):
    #     """
    #     처리된 내용인 classified 를 db 에 저장하기 위해서 강좌 정보인 new_data 받아와 순서대로 category, target 내용을 처리한 내용을 바꾼다.
    #     :param new_data: 크롤링한 강좌 내용
    #     :param classified: self.classify 에서 처리된 내용.
    #     2X: 영유아(5세까지) , 3X: 아동(6세 이상)
    #     :return:
    #     """
    #     classify_tag = {
    #         0: [20, 30], 1: [21, 31], 2: [22, 32], 3: [23, 33], 4: [24, 34], 5: [25, 35],
    #         6: [12, 31], 7: [14, 33], 8: [15, 32], 9: [19, 34], 10: [11, 33],
    #         11: "육아·자녀교육", 12: "음악·악기", 13: "미술·공예", 14: "라이프스타일", 15: "댄스·피트니스",
    #         16: "어학", 17: "인문학", 18: "재테크", 19: "요리",
    #         20: "공연·놀이", 21: "음악·악기", 22: "신체활동", 23: "교육·체험", 24: "요리", 25: "미술·공예",
    #         30: "공연·놀이", 31: "음악·악기", 32: "신체활동", 33: "교육·체험", 34: "요리", 35: "미술·공예"
    #     }
    #     target_dict: dict = {1: "Adult", 2: "Baby", 3: "Kid"}
    #     for data in classified:
    #         lecture_type: LectureType = new_data[classified.index(data)]
    #         if data <= 10:  # 10 이하는 두개의 카테고리를 의미 한다.
    #             data_tags: list[int] = classify_tag[data]
    #
    #             lecture_type.category = classify_tag[data_tags[0]]  # 카테고리 숫자의 이름을 가져온다.
    #             lecture_type.target = target_dict[data_tags[0] // 10]  # 카테고리 숫자 /10 의 몫을 가지고 대상을 가져온다.
    #
    #             # 두개의 카테고리가 하나의 값에 포함되어 있으므로 다른 카테고리를 가지고 있는 동일한 내용을 추가해준다.
    #             different_lecture_type = copy.deepcopy(lecture_type)
    #             different_lecture_type.target = target_dict[data_tags[1] // 10]
    #             different_lecture_type.category = classify_tag[data_tags[2]]
    #         else:
    #             lecture_type.target = target_dict[data // 10]
    #             lecture_type.category = classify_tag[data]
    #
    #     return new_data
