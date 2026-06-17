"""运行即训练：python src/entity_extraction/train.py"""

import sys
import os

# 把项目根目录加入 Python 路径，确保能找到 src 包
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.entity_extraction.trainer import prepare_data, train

# ---------- 配置 ----------
LABELSTUDIO_FILE = "知识点.json"          # LabelStudio 导出的标注数据
TRAIN_DIR = "./data/processed/course"      # 训练数据保存目录
SAVE_DIR = "./finetuned/checkpoint"        # 微调模型保存目录
NUM_EPOCHS = 20                            # 训练轮数
BATCH_SIZE = 16                            # 批大小
MAX_SEQ_LEN = 512                          # 最大序列长度
VALID_STEPS = 5                            # 每 N 步验证并保存一次模型
DEVICE = "cpu"                             # cpu 或 gpu
# -------------------------

if __name__ == "__main__":
    # 第1步：准备数据
    prepare_data(LABELSTUDIO_FILE, TRAIN_DIR)

    # 第2步：训练
    train(
        train_path=f"{TRAIN_DIR}/train.txt",
        dev_path=f"{TRAIN_DIR}/dev.txt",
        save_dir=SAVE_DIR,
        num_epochs=NUM_EPOCHS,
        batch_size=BATCH_SIZE,
        max_seq_len=MAX_SEQ_LEN,
        valid_steps=VALID_STEPS,
        device=DEVICE
    )
