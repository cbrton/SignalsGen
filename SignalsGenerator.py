import re
import csv
import pandas as pd

def signals_matches_valve_di(path: str) -> tuple:
    result = ''
    with open(path, 'r', encoding='utf-8') as file:
        var_declarations_string = file.read()
    declarations = var_declarations_string.split('\n')
    sr = declarations[0].split(sep=' ')[1]

    for declaration in declarations:
        object_name_list = re.search(r'\d{1,2}[a-z][a-z][a-z][a-z]?\d{1,3}(_\d)?', declaration)
        object_name:str = ''
        var_name:str = ''
        signal_type:str = ''
        if object_name_list:
            object_name = object_name_list[0]
            splitted_declaration = declaration.split(sep=':')
            var_name = re.sub(r'\s', '', splitted_declaration[0])
            splitted_var_name = var_name.split(sep='_')
            signal_type = splitted_var_name[len(splitted_var_name) - 1]

        if object_name != '':
            if signal_type == 'OPENED':
                valve_opened_signal = 'V_' + object_name + '_opened' + '\t' + sr + '.' + var_name + '\n'
                result += valve_opened_signal

            if signal_type == 'CLOSED':
                valve_closed_signal = 'V_' + object_name + '_closed' + '\t' + sr + '.' + var_name + '\n'
                result += valve_closed_signal

            if signal_type == 'Internal':
                valve_fault_signal = 'V_' + object_name + '_fault' + '\t' + sr + '.' + var_name + '\n'
                result += valve_fault_signal
    return (result, sr)

def signals_matches_valve_do(path: str) -> tuple:
    result = ''
    with open(path, 'r', encoding='utf-8') as file:
        var_declarations_string = file.read()
    declarations = var_declarations_string.split('\n')
    sr = declarations[0].split(sep=' ')[1]

    for declaration in declarations:
        object_name_list = re.search(r'\d{1,2}[a-z][a-z][a-z][a-z]?\d{1,3}(_\d)?', declaration)
        object_name:str = ''
        var_name:str = ''
        signal_type:str = ''
        if object_name_list:
            object_name = object_name_list[0]
            splitted_declaration = declaration.split(sep=':')
            var_name = re.sub(r'\s', '', splitted_declaration[0])
            splitted_var_name = var_name.split(sep='_')
            signal_type = splitted_var_name[len(splitted_var_name) - 1]

        if object_name != '':
            if signal_type == 'OPEN':
                valve_opened_signal = 'V_' + object_name + '_open' + '\t' + sr + '.' + var_name + '\n'
                result += valve_opened_signal

            if signal_type == 'CLOSE':
                valve_closed_signal = 'V_' + object_name + '_close' + '\t' + sr + '.' + var_name + '\n'
                result += valve_closed_signal
    return (result, sr)

def signals_matches_mtr_di(path: str) -> tuple:
    result = ''
    with open(path, 'r', encoding='utf-8') as file:
        var_declarations_string = file.read()
    declarations = var_declarations_string.split('\n')
    sr = declarations[0].split(sep=' ')[1]

    for declaration in declarations:
        object_name_list = re.search(r'N[A-Z]?\d{1,2}(_\d)?', declaration)
        object_name:str = ''
        var_name:str = ''
        signal_type:str = ''
        if object_name_list:
            object_name = object_name_list[0]
            splitted_declaration = declaration.split(sep=':')
            var_name = re.sub(r'\s', '', splitted_declaration[0])
            splitted_var_name = var_name.split(sep='_')
            signal_type = splitted_var_name[len(splitted_var_name) - 1]

        if object_name != '':
            if signal_type == 'WORK':
                pump_work_signal = object_name + '_pump_work' + '\t' + sr + '.' + var_name + '\n'
                result += pump_work_signal

            if signal_type == 'FAULT':
                pump_fault_signal = object_name + '_pump_fault' + '\t' + sr + '.' + var_name + '\n'
                result += pump_fault_signal

            if signal_type == 'WAITING':
                pump_waiting_signal = object_name + '_pump_waiting' + '\t' + sr + '.' + var_name + '\n'
                result += pump_waiting_signal
    return (result, sr)

def signals_matches_mtr_do(path: str) -> tuple:
    result = ''
    with open(path, 'r', encoding='utf-8') as file:
        var_declarations_string = file.read()
    declarations = var_declarations_string.split('\n')
    sr = declarations[0].split(sep=' ')[1]

    for declaration in declarations:
        object_name_list = re.search(r'N[A-Z]?\d{1,2}(_\d)?', declaration)
        object_name:str = ''
        var_name:str = ''
        signal_type:str = ''
        if object_name_list:
            object_name = object_name_list[0]
            splitted_declaration = declaration.split(sep=':')
            var_name = re.sub(r'\s', '', splitted_declaration[0])
            splitted_var_name = var_name.split(sep='_')
            signal_type = splitted_var_name[len(splitted_var_name) - 1]

        if object_name != '':
            if signal_type == 'OFF':
                pump_setStart_signal = object_name + '_pump_setStart' + '\t' + sr + '.' + var_name + '\n'
                result += pump_setStart_signal
    return (result, sr)

def write_str_to_file(data: str, path: str) -> None:
    with open(path, "w+", encoding="UTF-8") as f:
        for i in data:
            f.write(i)

def write_str_to_csv(data: str, path: str):
    with open(path, "w+", encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'system', 'equipment', 'name', 'place', 'product', 'module', 'channel', 'crate', 'check', 'cat', 'property', 'fb', 'inversion', 'ton', 'tof', 'comment', 'modbus', 'node'])
        rows = data.split(sep='\n')
        for row in rows:
            splitted_row = row.split(sep='\t')
            if splitted_row[0]:
                print(splitted_row)
                id = splitted_row[0]
                splitted_id = id.split(sep='_')
                equipment:str = ''
                equipment = splitted_id[1] + '/' + splitted_id[2]
                name:str = ''
                name = splitted_id[1] + '/' + splitted_id[2] + ' ' + splitted_id[3]
                comment = splitted_row[1]
                writer.writerow(
                   [id, 'RSU_12', equipment, name, '', '', '', '', '', '', '',
                     '', '', '', '', '', comment, '', ''])

def write_di_to_excel(data: str, path: str, type: str):
    ids:list = []
    systems:list = []
    equipments:list = []
    names: list = []
    fbs: list = []
    comments:list = []
    rows = data.split(sep='\n')

    for row in rows:
        splitted_row = row.split(sep='\t')
        if splitted_row[0]:
            id = splitted_row[0]
            ids.append(id)
            systems.append('RSU_12')
            fbs.append('FB_DI')
            splitted_id = id.split(sep='_')
            equipment: str = ''
            if type == 'valve':
                if len(splitted_id) == 4:
                    equipment = splitted_id[1] + '/' + splitted_id[2]
                else:
                    equipment = splitted_id[1]
            elif type == 'mtr':
                equipment = splitted_id[0] + '/' +splitted_id[1]
            equipments.append(equipment)
            name: str = ''
            if type == 'valve':
                if len(splitted_id) == 4:
                    name = splitted_id[1] + '/' + splitted_id[2] + ' ' + splitted_id[3]
                else:
                    name = splitted_id[1] + ' ' + splitted_id[2]
            elif type == 'mtr':
                name = splitted_id[0] + '/' + splitted_id[1] + ' ' + splitted_id[2] + ' ' + splitted_id[3]
            names.append(name)
            comment = splitted_row[1]
            comments.append(comment)

    df = pd.DataFrame({'id' : ids, 'system' : systems, 'equipment' : equipments, 'name' : names, 'place' : '', 'product' : '', 'module' : '', 'channel' : '', 'crate' : '', 'check' : '', 'cat' : '', 'property' : '', 'fb' : fbs, 'inversion' : '', 'ton' : '', 'tof' : '', 'comment' : comments, 'modbus' : '', 'node' : ''})
    df.to_excel(path)

def write_do_to_excel(data: str, path: str, type: str):
    ids:list = []
    systems:list = []
    equipments:list = []
    names: list = []
    fbs: list = []
    comments:list = []
    rows = data.split(sep='\n')

    for row in rows:
        splitted_row = row.split(sep='\t')
        if splitted_row[0]:
            id = splitted_row[0]
            ids.append(id)
            systems.append('RSU_12')
            fbs.append('FB_DO')
            splitted_id = id.split(sep='_')
            equipment: str = ''
            if type == 'valve':
                if len(splitted_id) == 4:
                    equipment = splitted_id[1] + '/' + splitted_id[2]
                else:
                    equipment = splitted_id[1]
            elif type == 'mtr':
                equipment = splitted_id[0] + '/' + splitted_id[1]
            equipments.append(equipment)
            name: str = ''
            if type == 'valve':
                if len(splitted_id) == 4:
                    name = splitted_id[1] + '/' + splitted_id[2] + ' ' + splitted_id[3]
                else:
                    name = splitted_id[1] + ' ' + splitted_id[2]
            elif type == 'mtr':
                name = splitted_id[0] + '/' + splitted_id[1] + ' ' + splitted_id[2] + ' ' + splitted_id[3]
            names.append(name)
            comment = splitted_row[1]
            comments.append(comment)

    df = pd.DataFrame({'id' : ids, 'equipment' : equipments, 'system' : systems, 'name' : names, 'place' : '', 'product' : '', 'module' : '', 'channel' : '', 'crate' : '', 'check' : '', 'inversion' : '', 'property' : '', 'fb' : fbs, 'comment' : comments, 'modbus' : '', 'node' : ''})
    df.to_excel(path)

signals_valve_di = signals_matches_valve_di('Files/var_declarations')
#write_str_to_file(signals_valve_di[0], 'Files/valve_di_' + signals_valve_di[1])
write_di_to_excel(signals_valve_di[0], 'Files/valve_di_' + signals_valve_di[1] + '.xlsx', 'valve')

signals_valve_do = signals_matches_valve_do('Files/var_declarations')
#write_str_to_file(signals_valve_do[0], 'Files/valve_do_' + signals_valve_do[1])
write_do_to_excel(signals_valve_do[0], 'Files/valve_do_' + signals_valve_do[1] + '.xlsx', 'valve')

signals_mtr_di = signals_matches_mtr_di('Files/var_declarations')
#write_str_to_file(signals_mtr_di[0], 'Files/mtr_di_' + signals_mtr_di[1])
write_di_to_excel(signals_mtr_di[0], 'Files/mtr_di_' + signals_mtr_di[1] + '.xlsx', 'mtr')

signals_mtr_do = signals_matches_mtr_do('Files/var_declarations')
#write_str_to_file(signals_mtr_do[0], 'Files/mtr_do_' + signals_mtr_do[1])
write_do_to_excel(signals_mtr_do[0], 'Files/mtr_do_' + signals_mtr_do[1] + '.xlsx', 'mtr')