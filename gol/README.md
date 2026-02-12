# Conway's Game of Life

Run the app:

```bash
cd gol
pip install -r requirements.txt
streamlit run app.py
```

Run tests:

```bash
cd gol
pytest tests/ -v
pytest tests/ --cov=app --cov-report=term-missing
```
