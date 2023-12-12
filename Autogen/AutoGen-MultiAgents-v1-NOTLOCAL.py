import autogen
import datetime

log_filename = datetime.datetime.now().strftime("F:\\AutogenLogs\\%Y-%m-%d_%H-%M-%S.log")
autogen.ChatCompletion.start_logging()

config_list = [
    {
        "api_type": "open_ai",
        "api_base": "https://api.openai.com/v1/",
        "api_key": "YOUR-API-KEY"
    }
]

llm_config = {
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

Copywriter = autogen.AssistantAgent(
    name="Copywriter",
    system_message="You are an experienced copywriter that writes short, catchy, and emotional Facebook posts.",
    llm_config=llm_config,
)

Copycritic = autogen.AssistantAgent(
    name="Copycritic",
    system_message="Skeptic and cynical writing teacher, striving to have all posts perfect, full of emotions and persuasive.",
    llm_config=llm_config,
)

GrammarExpert = autogen.AssistantAgent(
    name="GrammarExpert",
    system_message="You are a rapper that can help create short and fast-paced stories.",
    llm_config=llm_config,
)

Brandy = autogen.AssistantAgent(
    name="Brandy",
    system_message="You are a branding expert that thinks long term and always focuses on the brand's voice.",
    llm_config=llm_config,
)

groupchat = autogen.GroupChat(agents=[user_proxy, Copywriter, Copycritic, GrammarExpert, Brandy], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

def send_message_with_logging(manager, message):
    autogen.ChatCompletion.log_message(f"Message sent: {message}")
    manager.last_message(message)

def stop_logging_and_save():
    logs = autogen.ChatCompletion.stop_logging()
    with open(log_filename, "w") as log_file:
        for entry in logs:
            log_file.write(f"{entry}\n")

user_proxy.initiate_chat(manager, message="create a Facebook post that emphasizes the importance of testing many variations of ads when running Facebook ads. Brandy, GrammarExpert, and Copycritic: you need to evaluate and give feedback to Copywriter until you feel like his post is perfect. I want you to feel like you're about to cry since the post is so emotionally strong")
send_message_with_logging(manager, "This is a test message to log.")
stop_logging_and_save()
