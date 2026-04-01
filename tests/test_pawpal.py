from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_updates_status() -> None:
    task = Task(description="Morning walk", time="07:30", frequency="daily")

    task.mark_complete()

    assert task.is_completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet(pet_id="pet-1", name="Mochi", species="dog", age=4)
    initial_count = len(pet.tasks)

    pet.add_task(Task(description="Feed breakfast", time="08:00", frequency="daily"))

    assert len(pet.tasks) == initial_count + 1


def test_mark_task_complete_creates_next_daily_task() -> None:
    owner = Owner(
        owner_id="owner-1",
        name="Jordan",
        email="jordan@example.com",
        timezone="America/Los_Angeles",
    )
    pet = Pet(pet_id="pet-1", name="Mochi", species="dog", age=4)
    owner.add_pet(pet)

    pet.add_task(
        Task(
            description="Morning walk",
            time="07:30",
            frequency="daily",
            due_date=date(2026, 3, 31),
        )
    )

    scheduler = Scheduler()
    was_marked = scheduler.mark_task_complete(owner, pet_id="pet-1", description="Morning walk")

    assert was_marked is True
    assert len(pet.tasks) == 2
    assert pet.tasks[0].is_completed is True
    assert pet.tasks[1].due_date.isoformat() == "2026-04-01"
    assert pet.tasks[1].is_completed is False


def test_detect_time_conflicts_returns_warning_message() -> None:
    owner = Owner(
        owner_id="owner-1",
        name="Jordan",
        email="jordan@example.com",
        timezone="America/Los_Angeles",
    )
    dog = Pet(pet_id="pet-1", name="Mochi", species="dog", age=4)
    cat = Pet(pet_id="pet-2", name="Luna", species="cat", age=2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task(description="Evening walk", time="18:30", frequency="daily"))
    cat.add_task(Task(description="Medication", time="18:30", frequency="weekly"))

    scheduler = Scheduler()
    warnings = scheduler.detect_time_conflicts(owner)

    assert len(warnings) == 1
    assert "18:30" in warnings[0]
    assert "Mochi: Evening walk" in warnings[0]
    assert "Luna: Medication" in warnings[0]
