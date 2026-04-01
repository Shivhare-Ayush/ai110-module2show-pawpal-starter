from pawpal_system import Owner, Pet, Scheduler, Task


def print_task_list(title: str, tasks: list[Task]) -> None:
    print(title)
    print("-" * len(title))
    for task in tasks:
        status = "Done" if task.is_completed else "Pending"
        print(
            f"{task.due_date.isoformat()} {task.time} | "
            f"{task.description} | {task.frequency} | {status}"
        )
    print()


def print_schedule() -> None:
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

    # Add tasks intentionally out of order and include one exact same-time conflict.
    dog.add_task(Task(description="Mochi evening walk", time="18:30", frequency="daily"))
    cat.add_task(Task(description="Luna meds", time="18:30", frequency="weekly"))
    dog.add_task(Task(description="Mochi morning walk", time="07:30", frequency="daily"))
    cat.add_task(Task(description="Luna breakfast", time="08:00", frequency="daily"))

    scheduler = Scheduler()

    # Marking complete automatically creates the next daily occurrence.
    scheduler.mark_task_complete(owner, pet_id="pet-2", description="Luna breakfast")

    all_tasks = owner.get_all_tasks()
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    pending_tasks = scheduler.filter_tasks(owner, is_completed=False)
    mochi_tasks = scheduler.filter_tasks(owner, pet_name="Mochi")
    done_luna_tasks = scheduler.filter_tasks(owner, is_completed=True, pet_name="Luna")
    conflict_warnings = scheduler.detect_time_conflicts(owner)

    print_task_list("All Tasks Sorted by Time", sorted_tasks)
    print_task_list("Pending Tasks", pending_tasks)
    print_task_list("Tasks for Mochi", mochi_tasks)
    print_task_list("Completed Tasks for Luna", done_luna_tasks)

    print("Conflict Warnings")
    print("-" * 17)
    if not conflict_warnings:
        print("No conflicts found.")
    else:
        for warning in conflict_warnings:
            print(warning)
    print()


if __name__ == "__main__":
    print_schedule()
