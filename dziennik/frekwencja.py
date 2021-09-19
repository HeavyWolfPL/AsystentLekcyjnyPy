import asyncio, datetime, sys, random
import argparse

from vulcan import Keystore, Account, Vulcan
from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from tabulate import tabulate

MY_GROUP = 'Grupa 1'

grades = []
lessons = []
attendance = []

async def get_frekwencja():
    target_date = datetime.datetime.now()

    with open("key-config.json") as f:
        # load from a JSON string
        dziennikKeystore = Keystore.load(f.read())
    with open("acc-config.json") as f:
        # load from a JSON string
        dziennikAccount = Account.load(f.read())
    dziennikClient = Vulcan(dziennikKeystore, dziennikAccount)

    await dziennikClient.select_student()

    grades = await dziennikClient.data.get_grades(date_from=target_date)
    tmp = []

    # print(grades)
    # print(type(grades))

    async for grade in grades:
        tmp.append(grade)

    grades = tmp
    #print(grades)

    lessons = await dziennikClient.data.get_lessons(date_from=target_date)
    tmp = []
    async for lesson in lessons:
        tmp.append(lesson)
    print(lessons)

    lessons = tmp

    attendance = await dziennikClient.data.get_attendance(date_from=target_date)
    tmp = []
    async for att in attendance:
        tmp.append(att)

    attendance = tmp
    
    await dziennikClient.close()

    # For whole week
    if target_date == 'week':
        # Get week start date
        dt = datetime.datetime.now()
        start = dt - datetime.timedelta(days=dt.weekday())

        week_info = {}
        for d in range(5):
            target_date = start + datetime.timedelta(days=d)
            #loop = asyncio.get_event_loop()
            #loop.run_until_complete(await frekwencja())

            week_info[d] = {}
            for lesson in lessons:
                week_info[d][lesson.time.position] = {'lesson': lesson}

            for att in attendance:
                week_info[d][att.time.position]['attendance'] = att

        #  print(week_info)

        # table static
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Lp.", justify="right")
        table.add_column("Poniedziałek")
        table.add_column("Wtorek")
        table.add_column("Środa")
        table.add_column("Czwartek")
        table.add_column("Piątek")
        print("c")
        # Transform it from `day: data` to `1_hour: data` so it can be displayed
        for hour in range(1,9):
            row = [str(hour)]
            for day in range(5):
                cell = week_info[day].get(hour, None)
                # print(cell)
                if cell:
                    lesson = cell['lesson']

                    if lesson.subject:
                        name = lesson.subject.name
                        if len(name) > 16:
                            out = lesson.subject.code
                        else:
                            out = lesson.subject.name
                    elif lesson.event:
                        out = lesson.event
                    else:
                        out = 'NO_INFO'

                    att = cell.get('attendance', None)
                    if att:
                        if att.presence_type:
                            symbol = att.presence_type.symbol
                        else:
                            symbol = "b"
                    else:
                        symbol = "b"  # repetition is good for learning, right?

                    # Append group name, if MY_GROUP not specified
                    if lesson.group and not MY_GROUP:
                        out = out + ' (' + lesson.group.name + ')'
                        
                    out = symbol + ' ' + out
                else:
                    out = ''

                row.append(out)
            
            # print(row)
            table.add_row(*row)
            
        console.print(table)
        return table
    else:
        # For one day only
        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(await frekwencja())

        tabela = []
        headers = ["Lp.", "Od - Do", "Przedmiot", "Obecność"]
        all_info = {}

        for lesson in lessons:
            if lesson.visible:
                all_info[lesson.time.position] = [lesson]
        for att in attendance:
            if att.time.position in all_info.keys():
                all_info[att.time.position].append(att)

        godziny_nieobecne = []
        for key in sorted(all_info):
            try:
                symbol = all_info[key][1].presence_type.symbol
                if symbol == "▬":
                    godziny_nieobecne.append(str(all_info[key][1].time.position))
            except:
                symbol = "N/A"

            lesson = all_info[key][0]

            if lesson.subject:
                name = lesson.subject.name

                name = lesson.subject.name
                if len(name) > 16:
                    name = lesson.subject.code
                else:
                    name = lesson.subject.name
            elif lesson.event:
                name = lesson.event
            else:
                name = 'NO_INFO'

            if not MY_GROUP:
                if all_info[key][0].group:
                    name = name + ' (' + all_info[key][0].group.name + ')'
                
            tabela.append([str(all_info[key][0].time.position), all_info[key][0].time.displayed_time.split("-")[0] + " - " + all_info[key][0].time.displayed_time.split("-")[1], name, symbol])

        tabela = tabulate(tabela, headers, tablefmt="orgtbl", stralign="center")
        print(tabela)
        return tabela
