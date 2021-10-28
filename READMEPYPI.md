# FuncNotify
> **Get notified when your code finishes/crashes with one line of code**

![Build](https://img.shields.io/github/workflow/status/kevinfjiang/FuncNotify/CI) ![Deploy](https://img.shields.io/github/workflow/status/kevinfjiang/FuncNotify/CD)
![LCommit](https://img.shields.io/github/last-commit/kevinfjiang/FuncNotify) ![release](https://img.shields.io/github/v/release/kevinfjiang/FuncNotify?include_prereleases)
![License](https://img.shields.io/github/license/kevinfjiang/FuncNotify.svg)
### **Premise:**
Sometimes, functions take a long time. I wanted to create something that automatically notifies you when they're completed or of any errors, training ML. The advantage over other decorator nontifiers is that there's an added option to hide your api tokens and emails so they aren't accidentally pushed to a public repo. All this with just one line of code. 

#### This is a super lean ReadMe, check out the github linked [here](https://github.com/kevinfjiang/FuncNotify)

#### Installation
```$ pip install FuncNotify```
#### Use case
```python
# Add more as projects grow!
from FuncNotify import time_func, time_text, time_slack


@time_func(NotifyMethod="Text", use_env=True, env_path".env", 
           update_env=True, cellphone="8001234567")
def wait_func():
    """This function will use the text method and pull env varaibles from
    `.env`, it will update the already determined env variables too!"""
    do_something()


@time_Text()
def wait_func2():
    """All parameters are optional and each method has a personal decorator, 
    even the function call is optional see below"""
    do_something()

@time_Text
def wait_func3():
    """Auto pull from `.env` is enabled by default with Method specific 
    time decorators"""
    do_something()

@time_func(multi_target=[{...}, {...}], multi_env=["1.env", "2.env"])
def wait_func4():
    """Send to multiple sources either through specifiying multiple 
    dictionaries of kwargs or multiple .env paths, or both in pairs!"""
    do_something()

if __name__ == "__main__":
    """You don't even need to use the timer as a decorator, 
    use it as a normal function This is how we do testing 😊 """
    time_func(function=wait_func5)(*func5_args, **func5_kwargs)
```

All accomplish the same objective of notifying the user after ```wait_func()``` completes, one does so with the phone number saved as a env variable in ```.env``` so it never accidentally gets exposed.

#### CLI arguments
```
$ FuncNotify [command here] --kwargs NotifyMethod=Email multi_env=1.env multi_env=2.env 
```
```
$ FuncNotify go run main.go --kwargs NotifyMethod=Text cellphone=8001234567 
```
Anything after `--kwargs` with an equal sign will automatically be parsesd as a key word argument for FuncNotify. The remainder without `=` will be executed. This allows you to time any script.
`multi_target` not yet supported

#### Basic/Quick Demo
```$ pip install FuncNotify```
```FuncNotify sleep 5 --kwargs NotifyMethod=Print```

To expand, create a `.env` file and a twilio account according to these [instructions](https://www.twilio.com/docs/sms/quickstart/python) (it's free!). Instead of hard coding variables or exporting them to your env, jusst put them in the twilio alerts section of your `.env`, skp installing twilio as it's already installed. Then try:

```FuncNotify sleep 5 --kwargs NotifyMethod=Text```

### Supported Notify Methods
|               Platform                |
| :-----------------------------------: |
|            Console Print              |
|            [Email Twilio](https://docs.sendgrid.com/for-developers/sending-email/v3-python-code-example)           |
|            [Email Yagmail](https://github.com/kootenpv/yagmail)           |
|        [Text](https://www.twilio.com/docs/sms/send-messages)                          |
|        [Slack](https://api.slack.com/messaging/sending)                                |
|        [Microsoft Teams](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)            |

###### Create .env in current working directory and fill out information that you wanna use

[template.env](https://raw.githubusercontent.com/kevinfjiang/FuncNotify/master/template.env)