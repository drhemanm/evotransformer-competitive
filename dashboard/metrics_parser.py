"""
Metrics parser for EvoTransformer
Parses data from RESULTS_COMPETITIVE.md and other project files
"""

import re
import os
from typing import Dict, List, Optional
from datetime import datetime

class MetricsParser:
    """Parse metrics from project files"""

    def __init__(self, project_root: str = None):
        if project_root is None:
            # Assume script is in dashboard/ subdirectory
            self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        else:
            self.project_root = project_root

        self.results_file = os.path.join(self.project_root, 'RESULTS_COMPETITIVE.md')
        self.readme_file = os.path.join(self.project_root, 'README.md')

    def parse_results_file(self) -> Dict:
        """Parse RESULTS_COMPETITIVE.md file"""
        if not os.path.exists(self.results_file):
            return self._get_default_metrics()

        with open(self.results_file, 'r') as f:
            content = f.read()

        metrics = {
            'accuracies': self._extract_accuracies(content),
            'training_epochs': self._extract_training_epochs(content),
            'model_comparisons': self._extract_model_comparisons(content),
            'improvements': self._extract_improvements(content)
        }

        return metrics

    def _extract_accuracies(self, content: str) -> Dict[str, float]:
        """Extract accuracy values from content"""
        accuracies = {}

        # Pattern for validation accuracy
        val_acc_pattern = r'Validation Accuracy:\s*([\d.]+)%'
        match = re.search(val_acc_pattern, content)
        if match:
            accuracies['validation'] = float(match.group(1))

        # Pattern for competitive accuracy
        comp_pattern = r'Competitive EvoTransformer:\s*([\d.]+)%'
        match = re.search(comp_pattern, content)
        if match:
            accuracies['competitive'] = float(match.group(1))

        # Pattern for baseline
        baseline_pattern = r'Original.*?:\s*([\d.]+)%'
        match = re.search(baseline_pattern, content)
        if match:
            accuracies['baseline'] = float(match.group(1))

        return accuracies

    def _extract_training_epochs(self, content: str) -> List[Dict]:
        """Extract training epoch data"""
        epochs = []

        # Pattern for epoch data: Epoch X: XX.XX%
        epoch_pattern = r'Epoch\s+(\d+):\s+([\d.]+)%'
        matches = re.findall(epoch_pattern, content)

        for match in matches:
            epoch_num = int(match[0])
            accuracy = float(match[1])
            epochs.append({
                'epoch': epoch_num,
                'accuracy': accuracy,
                'is_best': False  # Would need more context to determine
            })

        return epochs

    def _extract_model_comparisons(self, content: str) -> List[Dict]:
        """Extract model comparison data"""
        comparisons = []

        # Pattern for model rows in tables
        # | Model | Accuracy | Parameters |
        table_pattern = r'\|\s*([^|]+)\s*\|\s*([\d.]+)%?\s*\|\s*([\d.]+)M?'
        matches = re.findall(table_pattern, content)

        for match in matches:
            model_name = match[0].strip()
            accuracy = float(match[1])
            params = float(match[2])

            # Skip table headers
            if 'Model' in model_name or 'Acc' in model_name:
                continue

            comparisons.append({
                'model': model_name,
                'accuracy': accuracy,
                'parameters': params,
                'efficiency': accuracy / params if params > 0 else 0
            })

        return comparisons

    def _extract_improvements(self, content: str) -> Dict[str, float]:
        """Extract improvement percentages"""
        improvements = {}

        # Pattern for improvement values
        imp_pattern = r'\+\s*([\d.]+)%'
        matches = re.findall(imp_pattern, content)

        if matches:
            improvements['total'] = float(matches[0])

        return improvements

    def _get_default_metrics(self) -> Dict:
        """Return default metrics if files don't exist"""
        return {
            'accuracies': {
                'validation': 70.35,
                'competitive': 70.35,
                'baseline': 63.06
            },
            'training_epochs': [],
            'model_comparisons': [],
            'improvements': {'total': 7.29}
        }

    def parse_model_file(self) -> Dict:
        """Parse model_competitive.py for architecture details"""
        model_file = os.path.join(self.project_root, 'model_competitive.py')

        if not os.path.exists(model_file):
            return self._get_default_architecture()

        with open(model_file, 'r') as f:
            content = f.read()

        architecture = {
            'num_layers': self._extract_value(content, r'num_layers[\'"]?\s*[:=]\s*(\d+)'),
            'num_heads': self._extract_value(content, r'num_heads[\'"]?\s*[:=]\s*(\d+)'),
            'ffn_dim': self._extract_value(content, r'ffn_dim[\'"]?\s*[:=]\s*(\d+)'),
            'd_model': self._extract_value(content, r'd_model[\'"]?\s*[:=]\s*(\d+)'),
            'dropout': self._extract_value(content, r'dropout[\'"]?\s*[:=]\s*([\d.]+)', float),
            'unfreeze_layers': self._extract_value(content, r'unfreeze_layers[\'"]?\s*[:=]\s*(\d+)'),
        }

        return architecture

    def _extract_value(self, content: str, pattern: str, type_func=int):
        """Extract a single value using regex pattern"""
        match = re.search(pattern, content)
        if match:
            try:
                return type_func(match.group(1))
            except (ValueError, IndexError):
                pass
        return None

    def _get_default_architecture(self) -> Dict:
        """Return default architecture if file doesn't exist"""
        return {
            'num_layers': 2,
            'num_heads': 12,
            'ffn_dim': 2048,
            'd_model': 768,
            'dropout': 0.1,
            'unfreeze_layers': 4
        }

    def get_all_metrics(self) -> Dict:
        """Get all parsed metrics"""
        results = self.parse_results_file()
        architecture = self.parse_model_file()

        return {
            'results': results,
            'architecture': architecture,
            'parsed_at': datetime.now().isoformat()
        }

if __name__ == '__main__':
    # Test the parser
    parser = MetricsParser()
    metrics = parser.get_all_metrics()

    import json
    print(json.dumps(metrics, indent=2))
