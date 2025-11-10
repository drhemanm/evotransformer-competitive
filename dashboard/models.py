"""
Data models for EvoTransformer Dashboard
"""

from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
from datetime import datetime
import json

@dataclass
class OverviewMetrics:
    """Overview performance metrics"""
    current_accuracy: float
    baseline_accuracy: float
    improvement: float
    confidence_interval: List[float]
    standard_error: float
    validation_samples: int
    correct_predictions: int
    p_value: str
    status: str
    last_updated: str

    def to_dict(self):
        return asdict(self)

@dataclass
class TrainingEpoch:
    """Training epoch data"""
    epoch: int
    accuracy: float
    loss: float
    is_best: bool

    def to_dict(self):
        return asdict(self)

@dataclass
class ModelComparison:
    """Competitive model comparison"""
    model: str
    accuracy: float
    parameters: float  # in millions
    status: str
    efficiency: float  # accuracy per million parameters

    def to_dict(self):
        return asdict(self)

@dataclass
class FeatureImpact:
    """Feature impact analysis"""
    feature: str
    impact: float
    description: str

    def to_dict(self):
        return asdict(self)

@dataclass
class ResourceMetrics:
    """Resource utilization metrics"""
    gpu: str
    vram: str
    training_time: str
    batch_size: int
    learning_rate_roberta: float
    learning_rate_evolved: float
    framework: str
    model_size_mb: float

    def to_dict(self):
        return asdict(self)

@dataclass
class ArchitectureConfig:
    """Model architecture configuration"""
    name: str
    base_model: str
    num_evolved_layers: int
    num_attention_heads: int
    hidden_dim: int
    ffn_dim: int
    dropout: float
    unfreeze_layers: int
    use_contrastive: bool
    total_parameters: int

    def to_dict(self):
        return asdict(self)

@dataclass
class RoadmapItem:
    """Roadmap enhancement item"""
    enhancement: str
    expected_gain: float
    status: str
    note: str

    def to_dict(self):
        return asdict(self)

class DashboardData:
    """Main dashboard data container"""

    def __init__(self):
        self.overview: Optional[OverviewMetrics] = None
        self.training_progress: List[TrainingEpoch] = []
        self.competitive_comparison: List[ModelComparison] = []
        self.feature_impact: List[FeatureImpact] = []
        self.resources: Optional[ResourceMetrics] = None
        self.architecture: Optional[ArchitectureConfig] = None
        self.roadmap: List[RoadmapItem] = []

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'overview': self.overview.to_dict() if self.overview else {},
            'training_progress': [ep.to_dict() for ep in self.training_progress],
            'competitive_comparison': [mc.to_dict() for mc in self.competitive_comparison],
            'feature_impact': [fi.to_dict() for fi in self.feature_impact],
            'resources': self.resources.to_dict() if self.resources else {},
            'architecture': self.architecture.to_dict() if self.architecture else {},
            'roadmap': [ri.to_dict() for ri in self.roadmap]
        }

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: Dict) -> 'DashboardData':
        """Create DashboardData from dictionary"""
        dashboard = cls()

        if 'overview' in data and data['overview']:
            dashboard.overview = OverviewMetrics(**data['overview'])

        if 'training_progress' in data:
            dashboard.training_progress = [
                TrainingEpoch(**ep) for ep in data['training_progress']
            ]

        if 'competitive_comparison' in data:
            dashboard.competitive_comparison = [
                ModelComparison(**mc) for mc in data['competitive_comparison']
            ]

        if 'feature_impact' in data:
            dashboard.feature_impact = [
                FeatureImpact(**fi) for fi in data['feature_impact']
            ]

        if 'resources' in data and data['resources']:
            dashboard.resources = ResourceMetrics(**data['resources'])

        if 'architecture' in data and data['architecture']:
            dashboard.architecture = ArchitectureConfig(**data['architecture'])

        if 'roadmap' in data:
            dashboard.roadmap = [
                RoadmapItem(**ri) for ri in data['roadmap']
            ]

        return dashboard
