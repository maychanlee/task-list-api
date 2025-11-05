from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from ..db import db
from datetime import datetime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(
            title = task_data["title"],
            description = task_data["description"],
            completed_at = task_data.get("completed_at")
        )
        return new_task
    
    def to_dict(self):
        task_dict = {}
        task_dict["id"] = self.id
        task_dict["title"] = self.title
        task_dict["description"] = self.description
        task_dict["is_complete"] = bool(self.completed_at)

        return task_dict
