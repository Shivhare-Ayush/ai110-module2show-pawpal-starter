import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
owner_email = st.text_input("Owner email", value="jordan@example.com")
owner_timezone = st.text_input("Owner timezone", value="America/Los_Angeles")

# Keep core objects in session_state so they persist across reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        owner_id="owner-1",
        name=owner_name,
        email=owner_email,
        timezone=owner_timezone,
    )

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

if "next_pet_id" not in st.session_state:
    st.session_state.next_pet_id = 1

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler

# Keep owner profile in sync with inputs.
owner.name = owner_name
owner.email = owner_email
owner.timezone = owner_timezone

st.markdown("### Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    pet_species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_age = st.number_input("Age", min_value=0, max_value=40, value=2)
    add_pet_submitted = st.form_submit_button("Add pet")

    if add_pet_submitted:
        pet_id = f"pet-{st.session_state.next_pet_id}"
        new_pet = Pet(
            pet_id=pet_id,
            name=pet_name,
            species=pet_species,
            age=int(pet_age),
        )
        owner.add_pet(new_pet)
        st.session_state.next_pet_id += 1
        st.success(f"Added pet: {pet_name}")

st.markdown("### Current Pets")
if owner.pets:
    st.table(
        [
            {
                "pet_id": pet.pet_id,
                "name": pet.name,
                "species": pet.species,
                "age": pet.age,
                "task_count": len(pet.tasks),
            }
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Add a Task")
if owner.pets:
    pet_lookup = {f"{pet.name} ({pet.pet_id})": pet.pet_id for pet in owner.pets}
    with st.form("add_task_form", clear_on_submit=True):
        selected_pet_label = st.selectbox("Select pet", list(pet_lookup.keys()))
        task_description = st.text_input("Task description", value="Morning walk")
        task_time = st.text_input("Time (HH:MM)", value="07:30")
        task_frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])
        add_task_submitted = st.form_submit_button("Add task")

        if add_task_submitted:
            selected_pet_id = pet_lookup[selected_pet_label]
            pet = owner.get_pet(selected_pet_id)
            if pet is None:
                st.error("Could not find pet for task assignment.")
            else:
                pet.add_task(
                    Task(
                        description=task_description,
                        time=task_time,
                        frequency=task_frequency,
                    )
                )
                st.success(f"Added task to {pet.name}: {task_description}")
else:
    st.info("Add a pet first to start assigning tasks.")

st.markdown("### Tasks by Pet")
if owner.pets and any(pet.tasks for pet in owner.pets):
    for pet in owner.pets:
        st.write(f"**{pet.name}**")
        if pet.tasks:
            st.table(
                [
                    {
                        "description": task.description,
                        "time": task.time,
                        "frequency": task.frequency,
                        "completed": task.is_completed,
                    }
                    for task in pet.tasks
                ]
            )
        else:
            st.caption("No tasks yet.")
else:
    st.info("No tasks yet. Add tasks above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button calls your Scheduler to organize tasks by time.")

if st.button("Generate schedule"):
    schedule = scheduler.organize_tasks(owner)
    if not schedule:
        st.warning("No pending tasks found. Add tasks first.")
    else:
        st.markdown("### Today's Schedule")
        st.table(
            [
                {
                    "time": task.time,
                    "description": task.description,
                    "frequency": task.frequency,
                    "status": "Done" if task.is_completed else "Pending",
                }
                for task in schedule
            ]
        )
