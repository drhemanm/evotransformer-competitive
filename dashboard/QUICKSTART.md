# EvoTransformer Dashboard - Quick Start Guide

## Installation (One-Time Setup)

### Option 1: Automated Script (Recommended)

**Linux/Mac:**
```bash
cd dashboard
./start_dashboard.sh
```

**Windows:**
```cmd
cd dashboard
start_dashboard.bat
```

### Option 2: Manual Setup

1. **Create virtual environment:**
```bash
python3 -m venv venv
```

2. **Activate virtual environment:**

Linux/Mac:
```bash
source venv/bin/activate
```

Windows:
```cmd
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the dashboard:**
```bash
python app.py
```

## Access the Dashboard

Open your browser and navigate to:
```
http://localhost:5000
```

## What You'll See

### 1. Performance Overview Cards
- Current accuracy: 70.35%
- Training time: 7.5 hours
- Model size: 40.6M parameters
- Statistical confidence: 95% CI

### 2. Interactive Charts
- **Training Progress**: Line chart showing accuracy and loss per epoch
- **Model Comparison**: Bubble chart comparing different model variants
- **Feature Impact**: Bar chart showing contribution of each enhancement

### 3. Technical Details
- **Architecture**: RoBERTa-base configuration and evolved layers
- **Resources**: GPU specs, memory, training hyperparameters

### 4. Product Roadmap
- Planned enhancements with expected accuracy gains
- Path to achieving 79% SOTA performance

## API Usage

### Get All Metrics
```bash
curl http://localhost:5000/api/all-metrics
```

### Get Overview Only
```bash
curl http://localhost:5000/api/overview
```

### Get Training Progress
```bash
curl http://localhost:5000/api/training-progress
```

### Get Model Comparison
```bash
curl http://localhost:5000/api/competitive-comparison
```

### Health Check
```bash
curl http://localhost:5000/health
```

## Using with Customer Presentations

### Full Screen Mode
Press `F11` in your browser for full-screen presentation mode.

### Key Talking Points

1. **Performance Achievement**
   - "We've achieved 70.35% accuracy on PIQA, a 7.29% improvement over baseline"
   - "With enhanced techniques, we reach 78.32%, within 1% of industry SOTA"

2. **Efficiency**
   - "Our model uses only 40.6M parameters vs 355M for RoBERTa-Large"
   - "That's 89% of SOTA performance with just 11% of the parameters"

3. **Training Resources**
   - "Trained on a single Tesla T4 GPU in just 7.5 hours"
   - "Production-ready and cost-effective for deployment"

4. **Innovation**
   - "Evolutionary architecture search automatically optimizes model structure"
   - "Combines pretrained RoBERTa with learned transformer blocks"

5. **Roadmap**
   - "Clear path to 79% accuracy with planned enhancements"
   - "Multi-task learning and ensemble methods in development"

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `app.py`:
```python
socketio.run(app, host='0.0.0.0', port=5001, debug=True)
```

### Python Version Issues
Ensure you have Python 3.8 or higher:
```bash
python3 --version
```

### Missing Dependencies
If you see import errors, reinstall dependencies:
```bash
pip install --force-reinstall -r requirements.txt
```

### Browser Compatibility
Use a modern browser:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Stopping the Dashboard

Press `Ctrl+C` in the terminal where the dashboard is running.

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore API endpoints for integration
- Customize metrics data in `app.py`
- Modify styling in `static/css/styles.css`

## Support

For issues or questions, refer to:
- Main README: [README.md](README.md)
- Project documentation: [../README.md](../README.md)
- Flask documentation: https://flask.palletsprojects.com/

---

**Ready to impress your customers!** 🚀
