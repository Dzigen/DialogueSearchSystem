# Source: https://amitness.com/2020/08/information-retrieval-evaluation/

#Retrieval metrics
# - mAP
# - MRR
# - precision
# - recall
# - f1
#Reader metrics
# - BLEU presision
# - ROUGE recall
# - METEOR f1

from torchmetrics.text.rouge import ROUGEScore
from torchmetrics.text import BLEUScore
import evaluate
import numpy as np
from typing import List
from tqdm import tqdm

#
class RetrievalMetrics:
    def __init__(self):
        pass
    
    def precision(self, predicted_cands: List[int], gold_cands: List[int], k: int) -> float:
        true_positive = np.isin(predicted_cands[:k], gold_cands).sum()
        false_positive = k - true_positive
        return round(true_positive / (true_positive + false_positive),5)

    def recall(self, predicted_cands: List[int], gold_cands: List[int], k: int) -> float:
        true_positive = np.isin(predicted_cands[:k], gold_cands).sum()
        false_negative = len(gold_cands) - true_positive
        return round(true_positive / (true_positive + false_negative),5)

    def f1_score(self, pred_cands: List[int], gold_cands: List[int], k: int) -> float:
        return (2 * self.precision(pred_cands, gold_cands, k) * self.recall(pred_cands, gold_cands, k)) / (self.precision(pred_cands, gold_cands, k) + self.recall(pred_cands, gold_cands, k))

    def AP(self, predicted_cands: List[int], gold_cands: List[int]) -> float:
        indicators = np.isin(predicted_cands, gold_cands)

        numerator = np.sum([self.precision(predicted_cands, gold_cands, k+1) 
                            for k in range(len(predicted_cands)) if indicators[k]])

        return round(numerator / len(gold_cands), 5)

    def mAP(self, predicted_cands_batch: List[List[int]], gold_cands_batch: List[List[float]]) -> float:
        return np.mean([self.AP(pred_cands, gold_cands) 
                        for pred_cands, gold_cands in zip(predicted_cands_batch, gold_cands_batch)])

    def reciprocal_rank(self, predicted_cands: List[int], gold_cands: List[int]) -> float:
        indicators = np.isin(predicted_cands, gold_cands)
        first_occur = np.where(indicators == True)[0]
        return round(0 if first_occur.size == 0 else 1 / (first_occur[0] + 1), 5)
        
    def MRR(self, predicted_cands_batch: List[List[int]], gold_cands_batch: List[List[int]]):
        return np.mean([self.reciprocal_rank(pred_cands, gold_cands) 
                        for pred_cands, gold_cands in zip(predicted_cands_batch, gold_cands_batch)])
    

# 
class ReaderMetrics:
    def __init__(self, base_dir):
        self.rouge_obj = ROUGEScore()
        self.bleu_obj = BLEUScore(n_gram=2)
        print("Loading Meteor...")
        self.meteor_obj = evaluate.load(f"{base_dir}/src/metrics/meteor")
        print("Loading ExactMatch")
        self.em_obj = evaluate.load(f"{base_dir}/src/metrics/exact_match")

    def bertscore(self, predicted: List[str], targets: List[str]):
        pass

    def rouge(self, predicted: List[str], targets: List[str]):
        accum = []
        for i in range(len(targets)):
            accum.append(self.rouge_obj(predicted[i], targets[i])['rougeL_fmeasure'])
        return round(np.mean(accum),5)

    def bleu(self, predicted: List[str], targets: List[str]):
        accum = []
        for i in range(len(targets)):
            accum.append(self.bleu_obj([predicted[i]], [[targets[i]]]))
        return round(np.mean(accum),5)

    def meteor(self, predicted: List[str], targets: List[str]):
        accum = []
        for i in range(len(targets)):
            accum.append(
                self.meteor_obj.compute(
                    predictions=[predicted[i]], references=[targets[i]])['meteor'])
        return round(np.mean(accum),5)
    
    def exact_match(self, predicted: List[str], targets: List[str]):
        return round(self.em_obj.compute(predictions=predicted, references=targets)["exact_match"], 2)