from dataclasses import dataclass, field
from typing import Any, Dict, List


class Owner:
	def __init__(
		self,
		owner_id: str,
		name: str,
		email: str,
		timezone: str,
		preferences: Dict[str, Any] | None = None,
	) -> None:
		self.owner_id = owner_id
		self.name = name
		self.email = email
		self.timezone = timezone
		self.preferences = preferences or {}
		self.pets: List[Pet] = []

	def add_pet(self, pet: "Pet") -> None:
		raise NotImplementedError

	def update_preferences(self, preferences: Dict[str, Any]) -> None:
		raise NotImplementedError

	def view_daily_tasks(self, date: str) -> List["CareTask"]:
		raise NotImplementedError


@dataclass
class Pet:
	pet_id: str
	owner_id: str
	name: str
	species: str
	age: int
	care_preferences: Dict[str, Any] = field(default_factory=dict)

	def update_profile(self, data: Dict[str, Any]) -> None:
		raise NotImplementedError

	def get_care_needs(self) -> Dict[str, Any]:
		raise NotImplementedError


@dataclass
class CareTask:
	task_id: str
	pet_id: str
	task_type: str
	duration_minutes: int
	priority: int
	scheduled_time: str
	status: str = "pending"

	def set_priority(self, level: int) -> None:
		raise NotImplementedError

	def reschedule(self, new_time: str) -> None:
		raise NotImplementedError

	def mark_complete(self) -> None:
		raise NotImplementedError


class Schedule:
	def __init__(self, date: str) -> None:
		self.date = date
		self.tasks: List[CareTask] = []
		self.reasoning: List[str] = []

	def add_task(self, task: CareTask) -> None:
		raise NotImplementedError

	def get_ordered_tasks(self) -> List[CareTask]:
		raise NotImplementedError


class SchedulerEngine:
	def __init__(self, constraints: Dict[str, Any] | None = None) -> None:
		self.constraints = constraints or {}

	def generate_daily_plan(
		self,
		owner: Owner,
		pets: List[Pet],
		tasks: List[CareTask],
	) -> Schedule:
		raise NotImplementedError

	def score_task(self, task: CareTask, constraints: Dict[str, Any]) -> int:
		raise NotImplementedError

	def explain_plan(self, schedule: Schedule) -> List[str]:
		raise NotImplementedError
