from pawpal_system import Pet, Task


def test_task_completion_updates_status() -> None:
    task = Task(description="Morning walk", time="07:30", frequency="daily")

    task.mark_complete()

    assert task.is_completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet(pet_id="pet-1", name="Mochi", species="dog", age=4)
    initial_count = len(pet.tasks)

    pet.add_task(Task(description="Feed breakfast", time="08:00", frequency="daily"))

    assert len(pet.tasks) == initial_count + 1
