import json
from pathlib import Path

# 自行添加任务
tasks = [
    # {"id": 1, "title": "学习python字典","done": False},
    # {"id": 2, "title": "完成函数练习", "done": True}
]

# 1.显示所有任务
def show_tasks(tasks):
    if tasks == [] :
        print("当前没有任务")
    else :
        # 用for循环打印任务编号和内容 再根据done打印已完成或者未完成
        for task in tasks:
            print(f'任务的编号为{task["id"]},任务的内容为{task["title"]},', end="")
            if task["done"] == True:
                print("已完成")
            else:
                print("未完成")

# 2.添加任务 成功返回True 内容为空返回False
def add_task(tasks,title,task_id):
    title = title.strip()
    if title == "" :
        return  False
    # 创建任务字典
    tasks.append({"id":task_id,"title":title,"done":False})
    return True

#  3.查找  找到任务时返回任务字典 找不到时返回None
def find_task(tasks,task_id):
    for task in tasks :
        if task["id"] == task_id:
            return task
    return None

# 4.完成任务 标记完成 找到任务返回True 否则返回False
def complete_task(tasks,task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return True
    return False

# 5.删除任务  找到任务返回True否则返回False
def delete_task(tasks,task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return True
    return False

# 6. 将任务列表保存到指定JSON文件
def save_tasks(tasks,file_path):
    with open(file_path,"w",encoding="utf-8") as file:
        json.dump(tasks,file,ensure_ascii=False,indent=2)

# 7. 加载任务 文件不存在时返回新列表
def load_tasks(file_path):
    try:
        with open(file_path,"r",encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# 7.主函数
def main():
    # 设置一个tasks存放的路径
    BASE_DIR = Path(__file__).resolve().parent
    file_path = BASE_DIR / "tasks.json"
    try :
        tasks = load_tasks(file_path)
    except json.JSONDecodeError:
        print(f"任务文件格式错误，请检查文件，程序已停止")
        return
    # 获取下一个任务的编号
    next_id = max((task["id"] for task in tasks), default=0) + 1
    while True:
        print("\n===== 我的待办事项 =====")
        print("1. 添加任务")
        print("2. 查看任务")
        print("3. 标记任务完成")
        print("4. 删除任务")
        print("0. 退出")

        choice = input("请输入选项：").strip()

        if choice == "1":
            # 输入标题，调用 add_task
            title = input("请输入任务标题：").strip()
            if add_task(tasks, title, next_id):
                # 添加成功后，next_id 加 1
                next_id += 1
                # 保存到json里面
                try:
                    save_tasks(tasks, file_path)
                except OSError:
                    print("保存失败")
                print("添加成功！")
            else:
                print("添加失败，请重新输入。")

        elif choice == "2":
            show_tasks(tasks)

        elif choice == "3":
            # 输入任务编号，调用 complete_task
            try:
                task_id = int(input("请输入任务的编号"))
            except ValueError:
                print("任务编号必须是整数，请重新输入。")
                continue
            if complete_task(tasks, task_id):
                print("标记成功！")
                # 保存
                try:
                    save_tasks(tasks, file_path)
                except OSError:
                    print("保存失败")
            else:
                print("任务编号不存在，请重新输入。")

        elif choice == "4":
            # 输入任务编号，调用 delete_task
            try:
                task_id = int(input("请输入任务的编号"))
            except ValueError:
                print("任务编号必须是整数，请重新输入。")
                continue
            if delete_task(tasks, task_id):
                print("删除成功！")
                # 保存到json里面
                try:
                    save_tasks(tasks, file_path)
                except OSError:
                    print("保存失败")
            else:
                print("任务编号不存在，请重新输入。")
        elif choice == "0":
            print("再见！")
            break
        else:
            print("无效选项，请重新输入。")


if __name__ == "__main__":
    main()