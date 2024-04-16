import openai
from dotenv import load_dotenv
import time
import logging

# from datetime import datetime


load_dotenv()

client = openai.OpenAI()
model = "gpt-3.5-turbo-16k"


# Uncomment the code to create your assistant and thread before running code below

# == Create our Assistant ==

# perosnal_trainer_assistant = client.beta.assistants.create(
#     name="Personal Trainer",
#     instructions="""You are the best perosnal trainer and nutritionalist.
#     You have trained A list movie starts""",
#     model=model,
# )
# personal_assistant_id = perosnal_trainer_assistant.id
# print(personal_assistant_id)


# ======== Thread =========


# thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "How do I get started working out to lose"
#             " fat and gain lean muscle?",
#         }
#     ]
# )


# ======== HardCode our ids =======
assitant_id = "asst_jlEhP5rOL3oKODfAzZT90z7M"
thread_id = "thread_49LZVyz77Onrs6bt6i66CoTP"


# # ======== Create a message =======

# message = "How many steps a day is realistic for weight loss?"
user_message = input("Enter your message: ")
message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=user_message,
)


# # == Run our Assistatnt ========

run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assitant_id,
    instructions="Please address the user as Your Majesty",
)


def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """
    Waits for a run to complete and prints the elapsed time.
    :param client: The OpenAI client instance.
    :param thread_id: The ID of the thread containing the run.
    :param run_id: The ID of the run to wait for.
    :param sleep_interval: The number of seconds to wait between checking steps

    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id,
            )
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )

                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(
                    thread_id=thread_id,
                )
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"Error while waiting for run completion: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)


# # === Run ===
wait_for_run_completion(
    client=client,
    thread_id=thread_id,
    run_id=run.id,
)


# === Steps --Logs ===

run_step = client.beta.threads.runs.steps.list(
    thread_id=thread_id,
    run_id=run.id,
)
print(f"Run Steps: {run_step.data[0]}")
