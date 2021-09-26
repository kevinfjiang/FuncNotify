# FuncNotify
### **Premise:**
Sometimes, functions take a long time. I wanted to create something that automatically notifies you when they're completed or of any errors, training ML. The advantage over other decorator nontifiers is that there's an added option to hide your api tokens and emails so they aren't accidentally pushed to a public repo. 

#### Installation
```$ pip install FuncNotify```

#### Use
```python
@time_func(dot_env=True, NotifyMethod="Text", cellphone="8001234567")
def wait_func():
    do_something()

@time_text
def wait_func2():
    do_something()
```
Both accomplish the same objective of notifying the user after ```wait_func()``` completes, one does so with the phone number saved as a env variable in ```.env``` so it never accidentally gets exposed.

#### Conribution:
Pleaes follow the instructions in ```TemplateMethod_.py``` and add to ```template.env``` and create a new branch. Also, test your credentials in a `.env` file and share them with me eventually!! I promise all I need them for is testing. If anybody knows a better method than my current secrets method, contact me at kevin.j@columbia.edu Thank you!
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