from pawpal_system import Owner, Pet, Scheduler, Task


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

    dog.add_task(Task(description="Mochi morning walk", time="07:30", frequency="daily"))
    cat.add_task(Task(description="Luna breakfast", time="08:00", frequency="daily"))
    dog.add_task(Task(description="Mochi evening walk", time="18:30", frequency="daily"))

    scheduler = Scheduler()
    todays_tasks = scheduler.organize_tasks(owner)

    print("Today's Schedule")
    print("-" * 24)
    for task in todays_tasks:
        status = "Done" if task.is_completed else "Pending"
        print(f"{task.time} | {task.description} | {task.frequency} | {status}")


if __name__ == "__main__":
    print_schedule()
