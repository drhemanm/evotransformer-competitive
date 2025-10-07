"""
Competitive EvoTransformer Architecture
RoBERTa-base + evolved layers + unfreezing
"""

import torch
import torch.nn as nn

class CompetitiveGenome:
    """Enhanced genome with unfreezing and contrastive learning"""
    def __init__(self, num_layers=2, num_heads=12, ffn_dim=2048,
                 memory_enabled=False, dropout=0.1, weight_decay=0.01,
                 unfreeze_layers=4, use_contrastive=True):
        self.d_model = 768
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.ffn_dim = ffn_dim
        self.memory_enabled = memory_enabled
        self.dropout = dropout
        self.weight_decay = weight_decay
        self.unfreeze_layers = unfreeze_layers
        self.use_contrastive = use_contrastive
    
    def to_dict(self):
        return {
            'num_layers': self.num_layers,
            'd_model': self.d_model,
            'num_heads': self.num_heads,
            'ffn_dim': self.ffn_dim,
            'memory_enabled': self.memory_enabled,
            'dropout': self.dropout,
            'weight_decay': self.weight_decay,
            'unfreeze_layers': self.unfreeze_layers,
            'use_contrastive': self.use_contrastive
        }
    
    def __repr__(self):
        return (f"CompGenome(L={self.num_layers}, h={self.num_heads}, "
                f"ffn={self.ffn_dim}, unfreeze={self.unfreeze_layers})")

class TransformerBlock(nn.Module):
    def __init__(self, d_model, num_heads, ffn_dim, dropout=0.1):
        super().__init__()
        self.attention = nn.MultiheadAttention(
            embed_dim=d_model, num_heads=num_heads,
            dropout=dropout, batch_first=True
        )
        self.ffn = nn.Sequential(
            nn.Linear(d_model, ffn_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(ffn_dim, d_model),
            nn.Dropout(dropout)
        )
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
    
    def forward(self, x, mask=None):
        attn_out, _ = self.attention(x, x, x, key_padding_mask=mask)
        x = self.norm1(x + attn_out)
        ffn_out = self.ffn(x)
        x = self.norm2(x + ffn_out)
        return x

class CompetitiveEvoTransformer(nn.Module):
    """RoBERTa with strategic unfreezing + evolved task layers"""
    def __init__(self, genome, pretrained_roberta):
        super().__init__()
        self.genome = genome
        
        # RoBERTa with partial unfreezing
        self.roberta = pretrained_roberta
        
        # Freeze all first
        for param in self.roberta.parameters():
            param.requires_grad = False
        
        # Unfreeze top N layers
        if genome.unfreeze_layers > 0:
            for layer in self.roberta.encoder.layer[-genome.unfreeze_layers:]:
                for param in layer.parameters():
                    param.requires_grad = True
        
        # Memory token (optional)
        if genome.memory_enabled:
            self.memory_token = nn.Parameter(torch.randn(1, 1, genome.d_model))
        
        # Evolved layers
        self.evolved_layers = nn.ModuleList([
            TransformerBlock(genome.d_model, genome.num_heads,
                           genome.ffn_dim, dropout=genome.dropout)
            for _ in range(genome.num_layers)
        ])
        
        # Classification head
        self.classifier = nn.Sequential(
            nn.Dropout(genome.dropout),
            nn.Linear(genome.d_model, genome.d_model // 2),
            nn.GELU(),
            nn.Dropout(genome.dropout),
            nn.Linear(genome.d_model // 2, 1)
        )
        
        # Contrastive head
        if genome.use_contrastive:
            self.contrastive_head = nn.Sequential(
                nn.Linear(genome.d_model, genome.d_model),
                nn.GELU(),
                nn.Linear(genome.d_model, genome.d_model // 2)
            )
    
    def forward(self, input_ids, attention_mask, return_embedding=False):
        # RoBERTa embeddings
        roberta_output = self.roberta(input_ids=input_ids, attention_mask=attention_mask)
        x = roberta_output.last_hidden_state
        
        # Memory token
        if self.genome.memory_enabled:
            batch_size = x.size(0)
            memory = self.memory_token.expand(batch_size, -1, -1)
            x = torch.cat([memory, x], dim=1)
            memory_mask = torch.ones(batch_size, 1, device=attention_mask.device,
                                    dtype=attention_mask.dtype)
            attention_mask = torch.cat([memory_mask, attention_mask], dim=1)
        
        mask = (attention_mask == 0)
        
        # Evolved layers
        for layer in self.evolved_layers:
            x = layer(x, mask)
        
        # Pool
        mask_expanded = (~mask).unsqueeze(-1).float()
        summed = (x * mask_expanded).sum(dim=1)
        counts = mask_expanded.sum(dim=1)
        pooled = summed / counts.clamp(min=1e-9)
        
        # Contrastive embedding
        if return_embedding and self.genome.use_contrastive:
            embedding = self.contrastive_head(pooled)
            return embedding
        
        # Classification
        logits = self.classifier(pooled).squeeze(-1)
        return logits
