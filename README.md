# FuncNotify ⏰ 
> **Get notified when your functions run**

![Build](https://img.shields.io/github/workflow/status/kevinfjiang/FuncNotify/CI?label=CI) ![Deploy](https://img.shields.io/github/workflow/status/kevinfjiang/FuncNotify/CD?label=CD)
 ![LCommit](https://img.shields.io/github/last-commit/kevinfjiang/FuncNotify) ![release](https://img.shields.io/github/v/release/kevinfjiang/FuncNotify?include_prereleases) ![License](https://img.shields.io/github/license/kevinfjiang/FuncNotify.svg)
![wheel](https://img.shields.io/pypi/wheel/FuncNotify)
### **Premise:**

Sometimes, functions take a long time. I wanted to create something that automatically notifies you when they're completed without risking exposing your phone number.

#### Installation use `pip` or equivalent
```$ pip install FuncNotify```

#### Quick Guide
```python
# Add more as projects grow!
from FuncNotify import time_func, time_text, time_slack


@time_func(NotifyMethod="Text", use_env=True, env_path".env", update_env=True, cellphone="8001234567")
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
    """Send to multiple sources either through specifiying multiple dictionaries of kwargs
    or multiple .env paths, or both in pairs!"""
    do_something()

if __name__ == "__main__":
    """You don't even need to use the timer as a decorator, use it as a normal function
    This is how we do testing 😊 """
    time_func(function=wait_func5)(*func5_args, **func5_kwargs)
```

#### [Contributing:](Contributing.md)  
Click above for instructions on how to contribute

#### Supported Notify Methods
|               Platform                |
| :-----------------------------------: |
|            Console Print              |
|            [Email Twilio](https://docs.sendgrid.com/for-developers/sending-email/v3-python-code-example)           |
|            [Email Yagmail](https://github.com/kootenpv/yagmai)|
|        [Text](https://www.twilio.com/docs/sms/send-messages)                          |
|        [Slack](https://api.slack.com/messaging/sending)                                |
|        [Microsoft Teams](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)            |

### **TODO:**
##### Personal stuff to organize and show what's currently accocmplished in the project
<details>
<summary>Project TODOs</summary>
<br>

**Admin stuff/documentation**
- [ ]  Complete ReadMe
- [x]  Remove my environment variables
- [X]  Document environment variables
- [X]  Write some tests

**Code stuff**
- [x] Add support for texts
- [x] Add support for slack
- [x] Add Default notify
- [x] Add ENV variable support
- [x] Use user email to search for slackID
- [x] Add generic decorator support
- [X] Add arguments to decorator support so you can specify keyword arguments like "(email={email}, token={token})"
- [X] Add .env support
- [X] Write Tests
- [X] Add logger support
- [X] Dropped support for 2.7, too annoying to mantain as metaclass was different
- [X] Made super easy to add to (automated imports, define the decorator at the same time).
- [X] Separate tests
- [X] GitHub action auto deployment
- [X] Multi person texting enabled
- [X] Add email
- [ ] Add whatsapp
- [ ] Add wechat
- [ ] Add Microsoft teams
</br>
</details>

##### Create .env in current working directory and fill out information that you wanna use

<details>
<summary>.env</summary>
<a href="https://raw.githubusercontent.com/kevinfjiang/FuncNotify/master/template.env">Strongly encourage copying this template</a>

</details>