# FuncNotify
> **Get notified when your functions run**
### **Premise:**
Sometimes, functions take a long time. I wanted to create something that automatically notifies you when they're completed without risking exposing your phone nubmer.

#### Installation use `pip` or equivalent
```$ pip install FuncNotify```

#### Use
```python
# Add more as projects grow!
from FuncNotify import time_func, time_text, time_slack


@time_func(NotifyMethod="Text", use_env=True, env_path".env", update_env=True, cellphone="8001234567")
def wait_func():
    """This function will use the text method and pull env varaibles from
    `.env`, it will update the already determined env variables too!"""
    do_something()


@time_text()
def wait_func2():
    """All parameters are optional and each method has a personal decorator, even the 
    function call is optional see below"""
    do_something()

@time_text
def wait_func3():
    """Auto pull from `.env` is enabled by default with Method specific time decorators"""
    do_something()

if __name__ == "__main__":
    """You don't even need to use the timer as a decorator, use it as a normal function
    This is how we do testing :) """
    time_func(function=wait_func4)(func4_args, func4_kwargs)
```

#### Conribution:
Please follow the instructions in ```TemplateMethod_.py``` and add to ```template.env``` and create a new branch. Also, test your credentials in a `.env` file and share them with me eventually!! I promise all I need them for is testing. If anybody knows a better method than my current secrets method, contact me at kevin.j@columbia.edu Thank you!

#### Supported Notify Methods
|               Platform                |
| :-----------------------------------: |
|            Console Print              |
|            Email                      |
|        [Slack](https://slack.com/)    |

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
- [ ] Separate tests
- [ ] GitHub action auto deploymentt
- [ ] Add Microsoft teams
- [ ] Add Some other 
</br>
</details>

##### Create .env in current working directory and fill out information that you wanna use

<details>
<summary>.env</summary>
<a href="https://raw.githubusercontent.com/kevinfjiang/FuncNotify/master/template.env">Strongly encourage copying this template</a>

</details>