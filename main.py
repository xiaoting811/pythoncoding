

# 自行添加任务
tasks = [
    # {"id": 1, "title": "学习python字典","done": False},
    # {"id": 2, "title": "完成函数练习", "done": True}
]

# 显示所有任务
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

# 添加任务 成功返回True 内容为空返回False
def add_task(tasks,title,task_id):
    title = title.strip()
    if title == "" :
        return  False
    # 创建任务字典
    tasks.append({"id":task_id,"title":title,"done":False})
    return True

#  查找  找到任务时返回任务字典 找不到时返回None
def find_task(tasks,task_id):
    for task in tasks :
        if task["id"] == task_id:
            return task
    return None

# 完成任务 标记完成 找到任务返回True 否则返回False
def complete_task(tasks,task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return True
    return False

# 删除任务  找到任务返回True否则返回False
def delete_task(tasks,task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return True
    return False

def main():
    tasks = []
    next_id = 1
    print("当前没有任务")
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
                print("添加成功！")
            else:
                print("添加失败，请重新输入。")

        elif choice == "2":
            show_tasks(tasks)

        elif choice == "3":
            # 输入任务编号，调用 complete_task
            task_id = int(input("请输入任务的编号"))
            if complete_task(tasks, task_id):
                print("标记成功！")
            else:
                print("任务编号不存在，请重新输入。")

        elif choice == "4":
            # 输入任务编号，调用 delete_task
            task_id = int(input("请输入任务的编号"))
            if delete_task(tasks, task_id):
                print("删除成功！")
            else:
                print("任务编号不存在，请重新输入。")
        elif choice == "0":
            print("再见！")
            break
        else:
            print("无效选项，请重新输入。")


if __name__ == "__main__":
    main()