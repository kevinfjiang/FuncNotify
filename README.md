# **FuncNotify ⏰**
> **Get notified when your code finishes/crashes with one line of code**

![Build](https://img.shields.io/github/workflow/status/kevinfjiang/FuncNotify/CI?label=CI) ![Deploy](https://img.shields.io/github/workflow/status/kevinfjiang/FuncNotify/CD?label=CD) [![DOC](https://github.com/kevinfjiang/FuncNotify/actions/workflows/docs.yml/badge.svg)](https://kevinfjiang.github.io/FuncNotify/) ![LCommit](https://img.shields.io/github/last-commit/kevinfjiang/FuncNotify) ![release](https://img.shields.io/github/v/release/kevinfjiang/FuncNotify?include_prereleases) ![License](https://img.shields.io/github/license/kevinfjiang/FuncNotify.svg)
![wheel](https://img.shields.io/pypi/wheel/FuncNotify)

**[Documentation](https://kevinfjiang.github.io/FuncNotify/#header-submodules) | [GitHub](https://github.com/kevinfjiang/FuncNotify) | [PyPI](https://pypi.org/project/FuncNotify/)**

### **Installation:**
```$ pip install FuncNotify```

### **Guide:**
```python
"""Add more as projects grow!"""
from FuncNotify import time_func, time_text, time_slack


@time_func(NotifyMethod="Text", use_env=True, env_path".env", update_env=True, phone="8001234567")
def wait_func():
    """This function will use the text method and pull env varaibles from
    `.env`, it will update the already determined env variables too!"""
    do_something()


@time_Text()
def wait_func2():
    """All parameters are optional and each method has a personal decorator, even the 
    function call is optional see below"""
    do_something()

@time_Text
def wait_func3():
    """Auto pull from `.env` is enabled by default with Method specific time decorators"""
    do_something()

@time_func(multi_target=[{...}, {...}], multi_env=["1.env", "2.env"])
def wait_func4():
    """Send to multiple sources either through specifying multiple dictionaries of kwargs
    or multiple .env paths, or both in pairs!"""
    do_something()

custom_message("HELLO WORLD", NotifyMethod="Text", multi_target=[{...}, {...}], multi_env=["1.env", "2.env"])
"""Custom messaging is here, pass the same arguments in as time_func and you 
can mass send messages in many methods"""

if __name__ == "__main__":
    """You don't even need to use the timer as a decorator, use it as a normal function
    This is how we do testing 😊 """
    time_func(function=wait_func5)(*func5_args, **func5_kwargs)
```
#### **CLI arguments:**
```$ FuncNotify [command here] --kwargs NotifyMethod=Text phone=8001234567 ```

```$ FuncNotify go run main.go --kwargs NotifyMethod=Email multi_env=1.env multi_env=2.env ```

```$ FuncNotify sleep 5 --kwargs NotifyMethod=Text multi_target="[{'NotifyMethod': 'Print', 'verbose': True}, {'phone': '8001234567'}]"```

Anything after `--kwargs` with an equal sign will automatically be parsesd as a key word argument for FuncNotify. The remainder without `=` will be executed. Wrap lists, dicts, and tuples in `"` so they get read properly. This allows you to time any script.

### **Demo:**
```$ pip install FuncNotify```

```$ FuncNotify sleep 5 --kwargs NotifyMethod=Print```

To expand, create a `.env` file and a twilio account according to these [instructions](https://www.twilio.com/docs/sms/quickstart/python) (it's free!). Instead of hard coding variables or exporting them to your env, just put them in the twilio alerts section of your `.env`, skip installing twilio as it's already installed. Then try:

```$ FuncNotify sleep 5 --kwargs NotifyMethod=Text```

### **[Contributing:](.github/Contributing.md)**
Click above for instructions on how to contribute

### Supported Methods:
|               Platform                |
| :-----------------------------------: |
|            Console Print              |
|            [Email Twilio](https://docs.sendgrid.com/for-developers/sending-email/v3-python-code-example)           |
|            [Email Yagmail](https://github.com/kootenpv/yagmai)|
|        [Text](https://www.twilio.com/docs/sms/send-messages)                          |
|        [Slack](https://api.slack.com/messaging/sending)                                |
|        [Microsoft Teams](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)            |


### Create following .env in CWD
<details>
<summary></summary>
<a href="https://raw.githubusercontent.com/kevinfjiang/FuncNotify/master/template.env">&emsp; .env</a>
</details>