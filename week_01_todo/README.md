# 第一周：Python 基础与命令行待办程序

本周需要掌握：用列表和字典表示任务，使用函数拆分功能，通过循环和条件分支组织菜单，处理输入错误，并解释数据怎样在函数之间传递。

本文按当前 `main.py` 整理。文件中的 JSON 保存、加载和路径处理是第二周增加的扩展，放在后半部分单独说明；标为“建议”的内容是复习示例，不表示代码已经修改。

## 1. 文件与运行方式

| 文件 | 用途 |
|---|---|
| main.py | 添加、查看、完成、删除任务，以及菜单入口 |
| tasks.json | 当前 main.py 实际读取、保存的任务数据 |
| todos.json | 当前目录中的另一个 JSON 文件，main.py 当前没有引用它 |
| .gitignore | 告诉 Git 哪些文件不应纳入版本管理 |
| .venv/ | 本地 Python 虚拟环境，通常不提交到 Git |

在本目录终端运行：

```powershell
python main.py
```

本程序使用 `json`、`pathlib` 标准库，不需要额外安装第三方包。运行时可能更新 `tasks.json`；练习异常情况前使用副本，不要用损坏数据覆盖原文件。

## 2. 列表、字典与布尔值

```python
tasks = [
    {"id": 1, "title": "学习列表", "done": False},
    {"id": 2, "title": "完成函数练习", "done": True},
]
```

- `tasks` 是列表，存放多个任务。
- 每个任务是字典，通过键读取字段。
- `id` 是任务编号，`title` 是标题，`done` 是完成状态。
- `True`、`False` 是布尔值，不要写成字符串 `"True"`、`"False"`。
- Python 下标从 0 开始，因此 `tasks[0]` 是第一项任务。

```python
tasks[0]             # 第一个任务字典
tasks[0]["title"]    # 第一个任务的标题
tasks[0]["done"]     # False
len(tasks)           # 任务数量：2
```

任务编号不等于列表下标。删除一项后，后面元素的下标会改变，原任务编号可以保持不变。

## 3. 遍历与条件判断

```python
for task in tasks:
    print(task["id"], task["title"])
    if task["done"]:
        print("已完成")
    else:
        print("未完成")
```

`for` 每次从列表取出一个任务字典，交给变量 `task`。`tasks` 是整个列表，`task` 是其中一个元素，不要混淆。

```python
if not tasks:
    print("当前没有任务")
```

空列表在条件判断中为假。当前代码中的 `if tasks == []:` 也正确；`if not tasks:` 更简洁。当前 `if task["done"] == True:` 可简写为 `if task["done"]:`，但不要在尚未理解时只机械替换。

### 格式化输出

```python
print(f'编号：{task["id"]}，标题：{task["title"]}，', end="")
print("未完成")
```

- `f"..."` 是格式化字符串，将花括号中的表达式结果放进文字。
- `end=""` 表示本次打印结束时不自动换行；下一次打印会接在同一行。
- 不指定 `end` 时，默认在末尾换行。

## 4. 函数、形参与实参

```python
def show_tasks(tasks):
    for task in tasks:
        print(task["title"])

my_tasks = [{"id": 1, "title": "复习函数", "done": False}]
show_tasks(my_tasks)
```

| 名称 | 本例含义 |
|---|---|
| def | 定义函数 |
| show_tasks | 函数名称 |
| 定义处的 tasks | 形参，接收调用时传入的对象 |
| 调用处的 my_tasks | 实参，实际传入的任务列表 |
| show_tasks(my_tasks) | 调用函数，执行函数体 |

形参和实参可以同名，也可以不同名。定义函数不会自动执行它，必须调用。函数应使用自己的形参，不要形参写成 `task`、函数体却意外读取外部的 `tasks`。

### return 与 print

```python
def add_task(tasks, title, task_id):
    title = title.strip()
    if title == "":
        return False
    tasks.append({"id": task_id, "title": title, "done": False})
    return True

ok = add_task(my_tasks, "学习字典", 2)
print(ok)
```

- `return` 把结果交给调用者，并立即结束本次函数执行。
- `print` 只向终端显示内容，不等于将该内容作为返回值。
- 函数没有执行带值的 `return` 时，默认返回 `None`。
- 本例 `ok` 接收成功或失败；`my_tasks` 存放任务，两者不是同一种数据。

## 5. 字符串 strip 与列表 append

```python
title = "  学习 Python  "
title = title.strip()
```

`strip()` 去掉字符串两端的空白，不删除中间的正常空格。字符串不可变，`strip()` 返回新字符串；只写 `title.strip()` 而不接住结果，原变量的内容不会改变。

```python
tasks.append({"id": 3, "title": "学习文件", "done": False})
```

`append()` 直接修改原列表，并返回 `None`。因此不要写成：

```python
# 错误示例：tasks 会被赋值为 None
tasks = tasks.append({"id": 3, "title": "学习文件", "done": False})
```

需要分清每个方法是“返回新结果”还是“修改原对象”。

## 6. 查找、None 与对象共享

```python
def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None
```

`return None` 在循环外面：必须检查完整个列表，才能确认没找到。如果放进第一次不匹配的分支，函数可能在第一项就提前结束。

```python
task = find_task(tasks, 2)
if task is None:
    print("任务不存在")
else:
    task["done"] = True
```

- 找到时返回的是列表中那个字典，不会自动复制成新字典。
- 因此修改 `task["done"]`，列表中的任务状态也会变化。
- 函数接收列表时也不会自动复制列表；在函数中 append/remove，调用者能看到变化。
- 若在函数里仅写 `tasks = []`，只是让该局部名称指向新列表，不等于清空调用者的原列表。
- `None` 表示没有找到结果，判断它通常使用 `is None`。

## 7. 完成与删除任务

当前 `complete_task()`、`delete_task()` 都按 id 遍历查找，找到返回 `True`，遍历结束未找到返回 `False`。

```python
task["done"] = True   # 修改字典中的字段
tasks.remove(task)    # 从列表删除该任务
```

当前删除函数在 `remove()` 后立即 `return`，不会继续遍历，因此当前用法可以工作。不要照搬成“边遍历边删除多项”的写法，那样可能漏过元素。以后可以复用 `find_task()`，减少重复查找代码，但并非本周必须重构。

## 8. 菜单、输入与循环控制

```python
while True:
    choice = input("请输入选项：").strip()
    if choice == "0":
        break
    elif choice == "2":
        show_tasks(tasks)
    else:
        print("请继续操作")
```

- `while True` 持续运行菜单，直到 `break` 结束该循环。
- `input()` 返回字符串，输入数字 2 后得到的是 `"2"`，所以菜单与字符串比较。
- `if / elif / else` 选择一条匹配分支。
- 缩进决定哪些语句属于函数、循环和分支。

```python
try:
    task_id = int(input("请输入任务编号："))
except ValueError:
    print("任务编号必须是整数")
    # 菜单循环中这里使用 continue
```

`int("2")` 转为整数 2；`int("abc")` 抛出 `ValueError`。菜单里的 `continue` 结束当前这一轮，回到下一轮显示菜单，不会退出整个程序。

| 语句 | 作用 |
|---|---|
| return | 结束当前函数，可把结果返回调用者 |
| break | 结束所在的最近一层循环 |
| continue | 跳过本轮剩余语句，进入下一轮循环 |

## 9. 编号 next_id

```python
next_id = max((task["id"] for task in tasks), default=0) + 1
```

括号中的生成器逐个提供已有任务 id，`max` 取最大值。列表为空时使用 `default=0`，于是新编号为 1。添加成功后 `next_id += 1`；添加空标题失败时不增加。

不要简单使用 `len(tasks) + 1`：删除某项后，任务数量减少，可能与仍存在的较大编号冲突。当前“最大已有编号加一”保证不与当前已有任务冲突，但删除最大编号后重启，可能再次使用那个历史编号。这不等于历史编号永不复用；需要这种保证时，要单独保存编号计数器。

## 10. main 与导入

```python
if __name__ == "__main__":
    main()
```

直接运行 `main.py` 时执行菜单；其他文件 `import main` 时不会自动启动菜单。函数定义仍然会加载，可以供调用者使用。本周不必把全部逻辑都写在文件最外层。

### 虚拟环境、Git 与文件保存

```powershell
python -m venv .venv
```

虚拟环境让项目使用独立的 Python 依赖。PyCharm 选择的解释器应与安装依赖的环境一致；本周只用标准库，暂时不必安装第三方包。`.venv` 是环境，不是业务代码，也不是 Git 仓库。

Git 用于保存代码修改的历史，与 JSON 保存任务数据是两件事。常用命令的含义：

| 命令 | 作用 |
|---|---|
| `git init` | 在当前目录初始化仓库，已有仓库不需要重复建立 |
| `git status` | 查看修改、新文件和暂存状态 |
| `git add main.py README.md .gitignore` | 将指定文件的当前修改放入暂存区 |
| `git commit -m "说明本次改动"` | 将暂存内容保存为一次本地提交 |
| `git log --oneline` | 查看简短提交历史 |

先检查状态，再暂存需要保存的文件。`.gitignore` 中可写 `.venv/`、`__pycache__/`，用于忽略尚未跟踪的环境和缓存；它不会自动让已跟踪文件退出 Git。`commit` 是本地保存历史，不等于已经上传到远程仓库。

## 11. 第二周扩展：保存与加载

当前 `main.py` 已经通过 `save_tasks()` 将列表保存到 `tasks.json`，启动时通过 `load_tasks()` 恢复任务。因此“关闭后任务一定消失”只适用于第一周最初的内存版本，不适用于当前实现。

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "tasks.json"
```

`Path` 首字母大写；`resolve()` 是方法，需要括号；`parent` 是属性，不加括号。详细文件、JSON 与异常知识见第二周 README。

当前加载函数在文件不存在时返回空列表；JSON 解析失败时主函数打印错误并退出。合法 JSON 不一定有正确的任务结构，当前尚未检查所有字段和字段类型，属于后续可完善项。

当前保存失败会打印“保存失败”，但有些分支仍打印添加、完成或删除成功。应理解：内存中的操作可能成功，磁盘保存却失败，两个状态要分清。本文记录这一学习要点，没有修改代码。

## 12. 本周应该能独立回答的问题

- [ ] 能解释 tasks、task、task_id 的区别，以及 tasks[0]["title"]。
- [ ] 能独立遍历列表，根据布尔值显示完成状态。
- [ ] 能解释形参、实参、函数调用、return 与 print。
- [ ] 知道 strip 返回新字符串，append/remove 修改原列表。
- [ ] 能说明 find_task 的 return None 为什么放在循环外。
- [ ] 能解释返回字典后修改 done，为什么列表中的状态也变化。
- [ ] 能处理非整数编号、不存在的编号和空标题。
- [ ] 能区分 return、break、continue。
- [ ] 能解释 next_id 为什么不直接用 len(tasks)+1。
- [ ] 能说明直接运行与 import 时，主入口的行为区别。
- [ ] 能区分虚拟环境、Git 代码提交与 JSON 任务数据保存。
- [ ] 能区分内存修改成功与文件保存成功。

复习时先自己写出添加和查找函数，再用三项任务练习完成、删除和再次查找。验收重点是能解释与修改需求，不是背下完整代码。
