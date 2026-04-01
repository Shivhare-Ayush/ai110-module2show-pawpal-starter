import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+, a smart pet care scheduler.

Use this app to add pets and tasks, mark recurring tasks complete,
review conflict warnings, and inspect a sorted/filtered schedule.
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

with st.expander("What this app demonstrates", expanded=True):
    st.markdown(
        """
This UI is connected to scheduler methods that provide:
- Time-based sorting for task lists.
- Task filtering by pet and completion status.
- Recurring task rollover for daily/weekly tasks when marked complete.
- Lightweight conflict warnings for same-time tasks.
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
            sorted_pet_tasks = scheduler.sort_by_time(pet.tasks)
            st.table(
                [
                    {
                        "due_date": task.due_date.isoformat(),
                        "description": task.description,
                        "time": task.time,
                        "frequency": task.frequency,
                        "completed": task.is_completed,
                    }
                    for task in sorted_pet_tasks
                ]
            )
        else:
            st.caption("No tasks yet.")
else:
    st.info("No tasks yet. Add tasks above.")

st.divider()

st.subheader("Complete a Task")
st.caption("Mark a pending task complete. Daily/weekly tasks auto-create the next occurrence.")

if owner.pets and any(pet.tasks for pet in owner.pets):
    pending_options: dict[str, tuple[str, str]] = {}
    for pet in owner.pets:
        for task in pet.tasks:
            if not task.is_completed:
                label = (
                    f"{pet.name} | {task.due_date.isoformat()} {task.time} | "
                    f"{task.description} ({task.frequency})"
                )
                pending_options[label] = (pet.pet_id, task.description)

    if pending_options:
        selected_pending_label = st.selectbox(
            "Pending tasks",
            list(pending_options.keys()),
        )
        if st.button("Mark selected task complete"):
            selected_pet_id, selected_description = pending_options[selected_pending_label]
            was_marked = scheduler.mark_task_complete(
                owner,
                pet_id=selected_pet_id,
                description=selected_description,
            )
            if was_marked:
                st.success("Task marked complete. Recurring tasks were rolled forward if needed.")
            else:
                st.warning("Task could not be marked complete.")
    else:
        st.info("No pending tasks available.")
else:
    st.info("Add pets and tasks first.")

st.divider()

st.subheader("Conflict Warnings")
st.caption("Warnings are shown when multiple tasks share the same exact HH:MM time.")

conflict_warnings = scheduler.detect_time_conflicts(owner)
if conflict_warnings:
    for warning in conflict_warnings:
        st.warning(warning)
else:
    st.success("No same-time task conflicts found.")

st.divider()

st.subheader("Smart Schedule View")
st.caption("Use filters below to view a sorted schedule for a pet, status, or both.")

pet_filter_options = ["All Pets"] + [pet.name for pet in owner.pets]
selected_pet_filter = st.selectbox("Filter by pet", pet_filter_options)
status_filter = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

selected_pet_name = None if selected_pet_filter == "All Pets" else selected_pet_filter
selected_status = None
if status_filter == "Pending":
    selected_status = False
elif status_filter == "Completed":
    selected_status = True

filtered_schedule = scheduler.filter_tasks(
    owner,
    is_completed=selected_status,
    pet_name=selected_pet_name,
)

if not filtered_schedule:
    st.warning("No tasks match the selected filters.")
else:
    st.table(
        [
            {
                "due_date": task.due_date.isoformat(),
                "time": task.time,
                "description": task.description,
                "frequency": task.frequency,
                "status": "Done" if task.is_completed else "Pending",
            }
            for task in filtered_schedule
        ]
    )
