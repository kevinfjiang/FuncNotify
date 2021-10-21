# FuncNotify

![Build](https://img.shields.io/github/workflow/status/kevinfjiang/FuncNotify/CI) ![Deploy](https://img.shields.io/github/workflow/status/kevinfjiang/FuncNotify/CD)
![LCommit](https://img.shields.io/github/last-commit/kevinfjiang/FuncNotify) ![release](https://img.shields.io/github/v/release/kevinfjiang/FuncNotify?include_prereleases)
![License](https://img.shields.io/github/license/kevinfjiang/FuncNotify.svg)
### **Premise:**
Sometimes, functions take a long time. I wanted to create something that automatically notifies you when they're completed or of any errors, training ML. The advantage over other decorator nontifiers is that there's an added option to hide your api tokens and emails so they aren't accidentally pushed to a public repo. 

#### This is a super lean ReadMe, check out the github linked [here](https://github.com/kevinfjiang/FuncNotify)

#### Installation
```$ pip install FuncNotify```
#### Use case
```python
@time_func(dot_env=True, NotifyMethod="Text", cellphone="8001234567")
def wait_func():
    do_something()

@time_text
def wait_func2():
    do_something()
```


Both accomplish the same objective of notifying the user after ```wait_func()``` completes, one does so with the phone number saved as a env variable in ```.env``` so it never accidentally gets exposed.

### Supported Notify Methods
|               Platform                |
| :-----------------------------------: |
|            Console Print              |
|            Email                      |
|        [Slack](https://slack.com/)    |

###### Create .env in current working directory and fill out information that you wanna use

[template.env](https://raw.githubusercontent.com/kevinfjiang/FuncNotify/master/template.env)