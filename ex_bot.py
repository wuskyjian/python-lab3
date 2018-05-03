from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def new_task(bot, update, args):
    """
    Add a new element to the given list
    """

    # args is a list: when you insert words separated by a space,
    # it considers the space as a separator and creates a list of all the inserted words

    # to re-create the string, you can simply join the words inserting a space among them
    task_to_add = ' '.join(args)

    if task_to_add and task_to_add.strip() and (not task_to_add.isspace()):
        # actually add the item to the list
        tasks_list.append(task_to_add)
        message = "The new task was successfully added to the list!"

    else:
        message = "You did not specify any task!"
    # send the generated message to the user
    bot.sendMessage(chat_id=update.message.chat_id, text=message)
    saveListToFile()


def remove_task(bot, update, args):
    """
    Remove an element from the given list
    """

    # args is a list: when you insert words separated by a space,
    # it considers the space as a separator and creates a list of all the inserted words

    # to re-create the string, you can simply join the words inserting a space among them

    task_to_remove = ' '.join(args)

    if task_to_remove and task_to_remove.strip() and (not task_to_remove.isspace()):
        # check if the task is actually present in the list
        if task_to_remove in tasks_list:
            tasks_list.remove(task_to_remove)
            message = "The task was successfully deleted!"
        else:
            message = "The task you specified is not in the list!"
    else:
        message = "You did not specify any task!"
    # send the generated message to the user
    bot.sendMessage(chat_id=update.message.chat_id, text=message)
    # save the list into the file
    saveListToFile()


def remove_multiple_tasks(bot, update, args):
    """
    Remove all the elements that contain a provided string
    """

    # create a list to store tasks we will remove at the end
    remove_list = []
    removed_elements = []
    # args is a list: when you insert words separated by a space,
    # it considers the space as a separator and creates a list of all the inserted words
    # to re-create the string, you can simply join the words inserting a space among them
    substring = ' '.join(args)

    if substring and substring.strip() and (not substring.isspace()):
        # substring is not None AND substring is not empty or blank AND substring is not only made by spaces

        # mark tasks that contains the specified substring
        for single_task in tasks_list:
            # if the substring is contained in the task we save it in the remove_list
            if substring in single_task:
                remove_list.append(single_task)
        if len(remove_list) > 0:
            for task_to_remove in remove_list:
                if task_to_remove in tasks_list:
                    tasks_list.remove(task_to_remove)
                    removed_elements.append(task_to_remove)
            message = "The elements " + ' , '.join(removed_elements)+" were successfully removed!"
        else:
            message = "I did not find any task to delete!"
    else:
        message = "You did not specify any string!"
    # send the generated message to the user
    bot.sendMessage(chat_id=update.message.chat_id, text=message)
    # save the list into the file
    saveListToFile()


def print_sorted_list(bot, update):
    """
    Print the elements of the list, sorted in alphabetic order
    """

    # check if the list is empty
    if len(tasks_list) == 0:
        message = "Nothing to do, here!"
    else:
        # we don't want to modify the real list of elements: we want only to print it after sorting
        # there are 2 possibilities:
        # a) using the sort method
        #  temp_tasks_list = tasks_list[:]
        #  temp_tasks_list.sort()
        #  message = temp_tasks_list
        # b) using the sorted method (the sorted method returns a new list)
        message = sorted(tasks_list)
    bot.sendMessage(chat_id=update.message.chat_id, text=message)


# define one command handler. Command handlers usually take the two arguments:
# bot and update.

def start(bot, update):
    update.message.reply_text('Hello! This is AmITaskListBot. You can use one of the following commands:')
    update.message.reply_text('/newTask <task to add>')
    update.message.reply_text('/removeTask <task to remove>')
    update.message.reply_text('/removeAllTasks <substring used to remove all the tasks that contain it>')
    update.message.reply_text('/showTasks')


def echo(bot, update):
    # get the message from the user
    text_to_send = "I'm sorry, I can't do that"
    bot.sendMessage(chat_id=update.message.chat_id, text=text_to_send)


def saveListToFile():

    """
    Here we save the changed list into the task_list.txt file
    """

    filename = "task_list.txt"

    try:
        # open file in write mode
        txt = open(filename, "w")

        # write each task as a new line in the file
        for single_task in tasks_list:
            txt.write(single_task + "\n")

        # close the file
        txt.close()
    except IOError:
        print("Problems in saving todo list to file")


if __name__ == '__main__':

    # main program

    # initialize the task list
    tasks_list = []
    # get the list from the "task_list.txt" file
    filename = "task_list.txt"
    try:
        # open the file
        txt = open(filename)

        # read the file: load each row in an element of the list without "/n"
        tasks_list = txt.read().splitlines()

        # close the file
        txt.close()

    except IOError:
        # File not found! We work with an empty list
        print("File not found!")
        exit()

    updater = Updater(token='486289139:AAH6O9v7HiBY-zkHHcGap_3BySYstoYBBHc')

    # add an handler to start the bot replying with the list of available commands
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))

    # on non-command textual messages - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # add an handler to insert a new task in the list
    newTask_handler = CommandHandler('newTask', new_task, pass_args=True)
    dispatcher.add_handler(newTask_handler)

    # add an handler to remove the first occurrence of a specific task from the list
    removeTask_handler = CommandHandler('removeTask', remove_task, pass_args=True)
    dispatcher.add_handler(removeTask_handler)

    # add an handler to remove from the list all the existing tasks that contain a provided string
    removeAllTasks_handler = CommandHandler('removeAllTasks', remove_multiple_tasks, pass_args=True)
    dispatcher.add_handler(removeAllTasks_handler)

    # add an handler to show the list tasks
    showTasks_handler = CommandHandler('showTasks', print_sorted_list)
    dispatcher.add_handler(showTasks_handler)

    # run the bot
    updater.start_polling()

    # run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
