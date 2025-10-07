# EvoTransformer Competitive: 70.35% on PIQA

Competitive implementation of EvoTransformer achieving **70.35% validation accuracy** on PIQA through evolutionary architecture search with RoBERTa-base.

## 🎯 Results

| Configuration | Val Acc | Improvement |
|---------------|---------|-------------|
| **Competitive (RoBERTa + Enhancements)** | **70.35%** | **+7.29%** |
| Original (Frozen BERT) | 63.06% | Baseline |
| Static Baseline | 53.43% | -9.63% |

## 🚀 Key Enhancements

✅ **RoBERTa-base** instead of BERT (better pretraining)
✅ **Partial unfreezing** (top 4 encoder layers)
✅ **4x data augmentation** (16K → 64K examples)
✅ **Contrastive learning** (improved representations)
✅ **Early stopping + LR scheduling** (better convergence)

## 📊 Training Progress

First genome results (40M trainable parameters):

- Epoch 1: 66.32%
- Epoch 3: 68.39%
- Epoch 5: **70.35%** ← Peak
- Epoch 8: Early stopping triggered

## 🏗️ Architecture

- **Base:** RoBERTa-base (125M params, top 4 layers unfrozen)
- **Evolved layers:** 2 transformer blocks
- **FFN dimension:** 2048
- **Attention heads:** 12
- **Trainable parameters:** 40.6M

## 🔬 Methodology

1. Start with pretrained RoBERTa-base
2. Unfreeze top 4 encoder layers for task adaptation
3. Add evolved transformer layers (2 blocks)
4. Train with contrastive + classification loss
5. Use 4x augmented data (swapping, paraphrasing)
6. Early stopping with patience=4

## 📦 Installation
```bash
pip install torch transformers tensorflow-datasets





@article{mohabeer2025evotransformer,
  title={EvoTransformer: Competitive Neural Architecture Through Evolution},
  author={Mohabeer, Heman},
  journal={Journal of Machine Learning Research},
  year={2025},
  note={Achieved 70.35\% on PIQA with 40.6M parameters}
}



4. Scroll down and click **"Commit changes"**
5. Add commit message: `Update README with competitive results`
6. Click **"Commit changes"**

---

## 📁 File 2: `train_competitive.py`

1. Click **"Add file"** → **"Create new file"**
2. Name: `train_competitive.py`
3. Paste this code:
```python
"""
Competitive EvoTransformer Training Script
Achieves 70.35% on PIQA validation set
"""

import tensorflow_datasets as tfds
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torch.optim as optim
from transformers import RobertaTokenizer, RobertaModel
import random
import numpy as np
from tqdm import tqdm
import copy

from model_competitive import CompetitiveGenome, CompetitiveEvoTransformer
from data_utils_competitive import preprocess_piqa_data_augmented

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

set_seed(42)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load data
print("Loading PIQA dataset...")
ds_train = tfds.load('piqa', split='train', as_supervised=False)
ds_val = tfds.load('piqa', split='validation', as_supervised=False)

train_data = list(tfds.as_numpy(ds_train))
val_data = list(tfds.as_numpy(ds_val))

# Load tokenizer and model
tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
pretrained_roberta = RobertaModel.from_pretrained("roberta-base")

# Preprocess with augmentation
train_processed = preprocess_piqa_data_augmented(train_data, tokenizer, augment=True)
val_processed = preprocess_piqa_data_augmented(val_data, tokenizer, augment=False)

print(f"Train: {len(train_processed)}, Val: {len(val_processed)}")

# Best competitive genome
genome = CompetitiveGenome(
    num_layers=2,
    num_heads=12,
    ffn_dim=2048,
    memory_enabled=False,
    dropout=0.1,
    weight_decay=0.01,
    unfreeze_layers=4,
    use_contrastive=True
)

# Create model
model = CompetitiveEvoTransformer(genome, pretrained_roberta).to(device)
print(f"Trainable params: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")

# Train
from training_competitive import train_competitive_genome

val_acc, train_acc, _, _ = train_competitive_genome(
    model, train_processed, val_processed, genome,
    max_epochs=20, batch_size=32
)

print(f"\nFinal Results:")
print(f"Validation: {val_acc:.4f}")
print(f"Training: {train_acc:.4f}")
