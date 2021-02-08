# -*- coding: utf-8 -*-
"""
Virginia Hebert
Mon Oct 19 22:06:48 2020
Python 1, DAT119
"""

# create a program to create and track a User's todo list

import os

def make_todo_list():
    """create a todo list"""
    exists = os.path.isfile("todo_app_todo.txt")
    if exists == True: # pull from file, if file is present
        saved_tasks = open("todo_app_todo.txt", "r")
        task_list = saved_tasks.readlines()
        saved_tasks.close()
    elif exists == False: # otherwise, create blank list
        task_list = []
    return task_list
    
def make_completed_list():
    """create completed item list"""
    exists = os.path.isfile("todo_app_done.txt")
    if exists == True: # pull from file, if file is present
        done_tasks = open("todo_app_done.txt", "r")
        done_list = done_tasks.readlines()
        done_tasks.close()
    elif exists == False: # otherwise, create blank list    
        done_list = []
    return done_list

def write_todo_list(task_list):
    """create file of not completed tasks"""
    export_todo_list = open("todo_app_todo.txt", 'w') 
    list_of_tasks_todo = task_list 
    for task in list_of_tasks_todo:
        export_todo_list.write(task)
    export_todo_list.close()   
    return export_todo_list

def write_done_list(finished_list):
    """create file of completed tasks"""
    export_done_list = open("todo_app_done.txt", 'w') 
    list_of_tasks_done = finished_list 
    for task in list_of_tasks_done:
        export_done_list.write(task)
    export_done_list.close()  
    return export_done_list

def append_todo_list(needing_todo_list,thing_todo):
    exported_todo_list = open("todo_app_todo.txt", 'a') 
    exported_todo_list.write(thing_todo) # add new item to todo list file
    exported_todo_list.close()
    needing_todo_list.append(thing_todo) # add new item to the in-program to do list
    return needing_todo_list

def get_input():
    """put together the list of options for the User to choose from and give error notice if they don't make a choice"""
    print() # aesthetic line
    print("your OPTIONS are: ")
    print("1 PRINT the TODO list")
    print("2 PRINT the COMPLETED items list")
    print("3 ADD a task to the todo list")
    print("4 CHECK an item as COMPLETED on the todo list")
    print("5 EXIT the program")
    user_input = input("Please enter the number that corresponds to what you would like to do: ")
    while user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4" and user_input != "5":
        print() # aesthetic line
        print("You didn't make a valid choice, try again.") # flag if they didn't enter in a proper choice
        user_input = input("Please enter the number that corresponds to what you would like to do: ")
    return user_input

def options():
    """define what happens when the User chooses each of the options and confirm they want to exit"""
    choice = get_input()
    while choice == "1" or choice == "2" or choice == "3" or choice == "4" or choice == "5":
        if choice == "1": # print todo list
            print() # aesthetic line
            print("Your TODO LIST is: ")
            todo_list = make_todo_list() # read from saved todo list file 
            if not todo_list:
                print("you have no tasks") # flag if no tasks are present
            else:
                for tasks in todo_list:
                    tasks_index = todo_list.index(tasks)
                    print(tasks_index +1, tasks.rstrip("\n"))
            choice = get_input()
        elif choice == "2": # print completed task list
            print() # aesthetic line
            print("You have CHECKED OFF: ")
            completed_list = make_completed_list() # read from saved completed list file 
            if not completed_list:
                print("you have not checked off any tasks") # flag if no completed tasks present
            else:
                for checked in completed_list:
                    checked_index = completed_list.index(checked)
                    print(checked_index + 1, checked.rstrip("\n"))
            choice = get_input()
        elif choice == "3": # add item to todo list
            add_item = input("What would you like to ADD? ")
            todo_list = make_todo_list() # read from saved todo list file 
            append_todo_list(todo_list, add_item + '\n')
            choice = get_input()
        elif choice == "4": # check item off todo list
            print() # aesthetic line
            todo_list = make_todo_list() # read from saved todo list file           
            completed_list = make_completed_list() # read from saved completed list file
            for tasks in todo_list: # print todo list to choose item
                tasks_index = todo_list.index(tasks)
                print(tasks_index +1, tasks.rstrip("\n"))
            check_item = input("Please select the number for which item you would like to CHECK OFF? ")
            if len(check_item) == 0 or ((int(check_item)) - 1) > tasks_index: # flag if proper value not entered
                print() # aesthetic line
                print("Please enter a valid number.")
                choice = get_input()
            else:
                done_item = todo_list[(int(check_item) - 1)]
                completed_list.append(done_item) # add completed item to done list
                todo_list.remove(done_item) # remove completed item from todo list
                write_todo_list(todo_list) # create todo list file
                write_done_list(completed_list) # create completed list file
                choice = get_input()
        elif choice == "5": # confirm exit and send them back into tracker if they change mind, otherwise quit program
            confirm_exit = input("Are you sure you want to exit - YES or NO? ")
            while confirm_exit.lower() != "no" and confirm_exit.lower() != "yes":
                print() # aesthetic line
                print("You didn't put in a yes or no, try again.")
                confirm_exit = input("Are you sure you want to exit - YES or NO? ")
            else:
                if confirm_exit.lower() == "no":    
                    choice = get_input() # head back into program
                elif confirm_exit.lower() == "yes":
                    print() # aesthetic line
                    return print("Thanks for using the TASK TRACKER. Come back around soon!")
        else: 
            print() # aesthetic line
            print("You didn't enter a valid option, try again.")
            choice = get_input()
                
        
def main():
    """pull it all together with the program introduction"""
#    todo_list = make_todo_list()
#    completed_list = make_completed_list()
    print() # aesthetic line
    print("Greetings!  I'd like to help you put together a todo list and keep TRACK of TASKS you've completed.")
    print() # aesthetic line    
    print("Please choose from the options below to create your list and check off items.")
    options()
    
 
if __name__ == "__main__":
    main()     
    
#make_todo_list()