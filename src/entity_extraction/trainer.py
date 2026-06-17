"""UIE 模型训练：数据准备 + 训练"""

import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def prepare_data(labelstudio_file: str, output_dir: str = "./data/processed/course"):
    """将 LabelStudio 标注数据转为训练集和验证集

    Args:
        labelstudio_file: LabelStudio 导出的 JSON 文件
        output_dir: 训练数据保存目录
    """
    print("[1/2] 转换 LabelStudio → doccano 格式...")
    r = subprocess.run(
        [sys.executable, "uie_pytorch/labelstudio2doccano.py",
         "--labelstudio_file", labelstudio_file],
        capture_output=True, text=True, cwd=BASE_DIR
    )
    if r.returncode != 0:
        print(f"转换失败: {r.stderr}")
        return

    print("[2/2] 切分训练集/验证集...")
    r = subprocess.run(
        [sys.executable, "uie_pytorch/doccano.py",
         "--doccano_file", "./doccano_ext.jsonl",
         "--task_type", "ext",
         "--save_dir", output_dir,
         "--splits", "0.8", "0.2", "0"],
        capture_output=True, text=True, cwd=BASE_DIR
    )
    if r.returncode != 0:
        print(f"切分失败: {r.stderr}")
        return

    print(r.stdout)
    print(f"[OK] 训练数据保存在 {output_dir}")


def train(train_path: str = "./data/processed/course/train.txt",
          dev_path: str = "./data/processed/course/dev.txt",
          save_dir: str = "./finetuned/checkpoint",
          model_path: str = "./uie_pytorch/uie_base_pytorch",
          num_epochs: int = 100,
          batch_size: int = 16,
          max_seq_len: int = 512,
          valid_steps: int = 100,
          device: str = "cpu"):
    """微调 UIE 模型

    Args:
        train_path: 训练集路径
        dev_path: 验证集路径
        save_dir: 模型保存路径
        model_path: 预训练模型路径
        num_epochs: 训练轮数
        batch_size: 批大小
        max_seq_len: 最大序列长度
        valid_steps: 每 N 步验证并保存一次
        device: cpu 或 gpu
    """
    print(f"开始训练（{num_epochs} 轮, batch_size={batch_size}, device={device}）...")
    cmd = [
        sys.executable, "uie_pytorch/finetune.py",
        "--train_path", train_path,
        "--dev_path", dev_path,
        "--save_dir", save_dir,
        "--learning_rate", "1e-5",
        "--batch_size", str(batch_size),
        "--max_seq_len", str(max_seq_len),
        "--num_epochs", str(num_epochs),
        "--model", model_path,
        "--logging_steps", "10",
        "--valid_steps", str(valid_steps),
        "--device", device
    ]
    r = subprocess.run(cmd, cwd=BASE_DIR)
    if r.returncode == 0:
        print(f"[OK] 模型训练完成，保存在 {save_dir}")
    else:
        print("[FAIL] 模型训练失败")
