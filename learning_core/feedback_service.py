import json
import os
import uuid
from datetime import datetime

FEEDBACK_FILE = "learning_core/feedback_db.json"

class FeedbackService:
    def __init__(self):
        self._ensure_db()

    def _ensure_db(self):
        if not os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, "w") as f:
                json.dump({"extraction": [], "optimization": []}, f)

    def log_feedback(self, task_type, input_snapshot, model_output, user_rating=0, user_corrections=None):
        """
        task_type: 'extraction' or 'optimization'
        input_snapshot: dict containing context (CV text, JD text etc)
        model_output: the raw output from the LLM
        user_rating: 1 (positive), -1 (negative), 0 (neutral)
        user_corrections: dict of corrected fields if available
        """
        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "input": input_snapshot,
            "output": model_output,
            "rating": user_rating,
            "corrections": user_corrections
        }
        
        with open(FEEDBACK_FILE, "r+") as f:
            data = json.load(f)
            data.setdefault(task_type, []).append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)

    def get_golden_examples(self, task_type, limit=3):
        """
        Retrieves high-rated examples to serve as few-shot context.
        """
        with open(FEEDBACK_FILE, "r") as f:
            data = json.load(f)
            
        # Filter for positive feedback
        good_examples = [e for e in data.get(task_type, []) if e['rating'] > 0]
        
        # specific logic depending on task could go here (e.g. semantic search)
        # For MVP, just return recent ones
        return good_examples[-limit:]
