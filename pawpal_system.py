from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class Task:
	description: str
	time: str
	frequency: str
	is_completed: bool = False

	def mark_complete(self) -> None:
		"""Mark this task as completed."""
		self.is_completed = True

	def mark_incomplete(self) -> None:
		"""Mark this task as not completed."""
		self.is_completed = False

	def update_time(self, new_time: str) -> None:
		"""Update the scheduled time for this task."""
		self.time = new_time


@dataclass
class Pet:
	pet_id: str
	name: str
	species: str
	age: int
	tasks: List[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		"""Add a task to this pet's task list."""
		self.tasks.append(task)

	def remove_task(self, description: str) -> bool:
		"""Remove the first task matching the description."""
		for i, task in enumerate(self.tasks):
			if task.description == description:
				del self.tasks[i]
				return True
		return False

	def get_tasks(self) -> List[Task]:
		"""Return a shallow copy of this pet's tasks."""
		return list(self.tasks)


@dataclass
class Owner:
	owner_id: str
	name: str
	email: str
	timezone: str
	pets: List[Pet] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to this owner's pet list."""
		self.pets.append(pet)

	def remove_pet(self, pet_id: str) -> bool:
		"""Remove a pet by id and return whether removal succeeded."""
		for i, pet in enumerate(self.pets):
			if pet.pet_id == pet_id:
				del self.pets[i]
				return True
		return False

	def get_pet(self, pet_id: str) -> Pet | None:
		"""Return a pet by id, or None if not found."""
		for pet in self.pets:
			if pet.pet_id == pet_id:
				return pet
		return None

	def get_all_tasks(self) -> List[Task]:
		"""Collect tasks from all pets owned by this owner."""
		all_tasks: List[Task] = []
		for pet in self.pets:
			all_tasks.extend(pet.get_tasks())
		return all_tasks


class Scheduler:
	def get_all_tasks(self, owner: Owner) -> List[Task]:
		"""Return all tasks across every pet for the owner."""
		return owner.get_all_tasks()

	def get_pending_tasks(self, owner: Owner) -> List[Task]:
		"""Return all incomplete tasks across the owner's pets."""
		return [task for task in owner.get_all_tasks() if not task.is_completed]

	def get_tasks_by_frequency(self, owner: Owner, frequency: str) -> List[Task]:
		"""Return tasks filtered by a normalized frequency value."""
		normalized = frequency.strip().lower()
		return [
			task
			for task in owner.get_all_tasks()
			if task.frequency.strip().lower() == normalized
		]

	def get_tasks_for_time(self, owner: Owner, time: str) -> List[Task]:
		"""Return tasks scheduled exactly at the provided time string."""
		return [task for task in owner.get_all_tasks() if task.time == time]

	def organize_tasks(self, owner: Owner, include_completed: bool = False) -> List[Task]:
		"""Sort tasks by time, optionally excluding completed tasks."""
		tasks = owner.get_all_tasks()
		if not include_completed:
			tasks = [task for task in tasks if not task.is_completed]
		return sorted(tasks, key=self._task_sort_key)

	def mark_task_complete(self, owner: Owner, pet_id: str, description: str) -> bool:
		"""Mark a pet task complete by pet id and task description."""
		pet = owner.get_pet(pet_id)
		if pet is None:
			return False

		for task in pet.tasks:
			if task.description == description:
				task.mark_complete()
				return True
		return False

	@staticmethod
	def _task_sort_key(task: Task) -> tuple[int, str]:
		"""Provide a stable sort key that prefers valid HH:MM times."""
		try:
			parsed_time = datetime.strptime(task.time, "%H:%M")
			return (0, parsed_time.strftime("%H:%M"))
		except ValueError:
			# Keep invalid time formats at the end but preserve deterministic ordering.
			return (1, task.time)


# Backward-compatible aliases for earlier naming in this project.
CareTask = Task
SchedulerEngine = Scheduler
