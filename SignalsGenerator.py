import re
import pandas as pd

read_path = 'Files/var_declarations'
with open(read_path, 'r', encoding='utf-8') as file:
    var_declarations_string = file.read()  # Чтение файла с объявлениями переменных
declarations = var_declarations_string.split('\n')  # Разделение файла по строкам в массив declarations
sr = declarations[0].split(sep=' ')[1]  # Выделение названия sr-ки для добавления в название целевых файлов

def signals_matches(equipment_type: str, signal_type: str) -> tuple:
    result = ''

    if equipment_type == 'valve':
        for declaration in declarations:
            object_name_list = re.search(r'\d{1,2}[a-z][a-z][a-z][a-z]?\d{1,3}(_\d)?', declaration)     # Поиск названия клапана с помощью регулярки
            object_name: str = ''
            var_name: str = ''
            signal_desc: str = ''
            if object_name_list:
                object_name = object_name_list[0]
                splitted_declaration = declaration.split(sep=':')
                var_name = re.sub(r'\s', '', splitted_declaration[0])
                splitted_var_name = var_name.split(sep='_')
                signal_desc = splitted_var_name[len(splitted_var_name) - 1]

            if signal_type == 'di':
                if object_name != '':
                    if signal_desc == 'OPENED':
                        valve_opened_signal = 'V_' + object_name + '_opened' + '\t' + sr + '.' + var_name + '\n'
                        result += valve_opened_signal

                    if signal_desc == 'CLOSED':
                        valve_closed_signal = 'V_' + object_name + '_closed' + '\t' + sr + '.' + var_name + '\n'
                        result += valve_closed_signal

                    if signal_desc == 'Internal':
                        valve_fault_signal = 'V_' + object_name + '_fault' + '\t' + sr + '.' + var_name + '\n'
                        result += valve_fault_signal
            elif signal_type == 'do':
                if object_name != '':
                    if signal_desc == 'OPEN':
                        valve_opened_signal = 'V_' + object_name + '_open' + '\t' + sr + '.' + var_name + '\n'
                        result += valve_opened_signal

                    if signal_desc == 'CLOSE':
                        valve_closed_signal = 'V_' + object_name + '_close' + '\t' + sr + '.' + var_name + '\n'
                        result += valve_closed_signal
    elif equipment_type == 'mtr':
        for declaration in declarations:
            object_name_list = re.search(r'N[A-Z]?\d{1,2}(_\d)?', declaration)
            object_name: str = ''
            var_name: str = ''
            signal_desc: str = ''
            if object_name_list:
                object_name = object_name_list[0]
                splitted_declaration = declaration.split(sep=':')
                var_name = re.sub(r'\s', '', splitted_declaration[0])
                splitted_var_name = var_name.split(sep='_')
                signal_desc = splitted_var_name[len(splitted_var_name) - 1]

            if signal_type == 'di':
                if object_name != '':
                    if signal_desc == 'WORK':
                        pump_work_signal = object_name + '_pump_work' + '\t' + sr + '.' + var_name + '\n'
                        result += pump_work_signal

                    if signal_desc == 'FAULT':
                        pump_fault_signal = object_name + '_pump_fault' + '\t' + sr + '.' + var_name + '\n'
                        result += pump_fault_signal

                    if signal_desc == 'WAITING':
                        pump_waiting_signal = object_name + '_pump_waiting' + '\t' + sr + '.' + var_name + '\n'
                        result += pump_waiting_signal
            elif signal_type == 'do':
                if object_name != '':
                    if signal_desc == 'OFF':
                        pump_setStart_signal = object_name + '_pump_setStart' + '\t' + sr + '.' + var_name + '\n'
                        result += pump_setStart_signal
    elif equipment_type == 'ai':
        for declaration in declarations:
            object_name_list = re.search(r'[L|P|T|Q|F]T_\d{1,2}[L|P|T|Q|F]\d{1,2}', declaration)
            object_name: str = ''
            var_name: str = ''
            signal_desc: str = ''
            if object_name_list:
                object_name = object_name_list[0]
                splitted_object_name = object_name.split(sep='_')
                sensor_position = splitted_object_name[1]
                ymin_var: str = ''
                ymax_var: str = ''
                ah_var: str = ''
                al_var: str = ''
                for row in declarations:
                    sensor_name_list = re.search(sensor_position, row)
                    if sensor_name_list:
                        splitted_row = row.split(sep=':')
                        sensor_var_name = re.sub(r'\s', '', splitted_row[0])
                        splitted_sensor_var_name = sensor_var_name.split(sep='_')
                        config_var = splitted_sensor_var_name[len(splitted_sensor_var_name) - 2] + '_' + splitted_sensor_var_name[len(splitted_sensor_var_name) - 1]
                        if config_var == 'Lo_limit':
                            ymin_var = sensor_var_name
                        elif config_var == 'Hi_limit':
                            ymax_var = sensor_var_name
                        elif config_var == 'SET_MAX':
                            ah_var = sensor_var_name
                        elif config_var == 'SET_MIN':
                            al_var = sensor_var_name
                splitted_declaration = declaration.split(sep=':')
                var_name = re.sub(r'\s', '', splitted_declaration[0])
                splitted_var_name = var_name.split(sep='_')
                signal_desc = splitted_var_name[len(splitted_var_name) - 1]
                ai_signal = object_name + '\t' + sr + '.' + var_name + '\t' + sr + '.' + ymin_var + '\t' + sr + '.' + ymax_var + '\t' + sr + '.' + ah_var + '\t' + sr + '.' + al_var + '\n'
                print(ai_signal)
                result += ai_signal
    return (result, sr)

def write_str_to_file(data: str, path: str) -> None:
    with open(path, "w+", encoding="UTF-8") as f:
        for i in data:
            f.write(i)

def write_signal_to_excel(data: str, write_path: str, equipment_type: str, signal_type: str):
    if signal_type == 'di':
        ids: list = []
        systems: list = []
        equipments: list = []
        names: list = []
        fbs: list = []
        comments: list = []
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
                if equipment_type == 'valve':
                    if len(splitted_id) == 4:
                        equipment = splitted_id[1] + '/' + splitted_id[2]
                    else:
                        equipment = splitted_id[1]
                elif equipment_type == 'mtr':
                    equipment = splitted_id[0] + '/' + splitted_id[1]
                equipments.append(equipment)
                name: str = ''
                if equipment_type == 'valve':
                    if len(splitted_id) == 4:
                        name = splitted_id[1] + '/' + splitted_id[2] + ' ' + splitted_id[3]
                    else:
                        name = splitted_id[1] + ' ' + splitted_id[2]
                elif equipment_type == 'mtr':
                    name = splitted_id[0] + '/' + splitted_id[1] + ' ' + splitted_id[2] + ' ' + splitted_id[3]
                names.append(name)
                comment = splitted_row[1]
                comments.append(comment)

        df = pd.DataFrame(
            {'id': ids, 'system': systems, 'equipment': equipments, 'name': names, 'place': '', 'product': '',
             'module': '', 'channel': '', 'crate': '', 'check': '', 'cat': '', 'property': '', 'fb': fbs,
             'inversion': '', 'ton': '', 'tof': '', 'comment': comments, 'modbus': '', 'node': ''})
        df.to_excel(write_path)
    elif signal_type == 'do':
        ids: list = []
        systems: list = []
        equipments: list = []
        names: list = []
        fbs: list = []
        comments: list = []
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
                if equipment_type == 'valve':
                    if len(splitted_id) == 4:
                        equipment = splitted_id[1] + '/' + splitted_id[2]
                    else:
                        equipment = splitted_id[1]
                elif equipment_type == 'mtr':
                    equipment = splitted_id[0] + '/' + splitted_id[1]
                equipments.append(equipment)
                name: str = ''
                if equipment_type == 'valve':
                    if len(splitted_id) == 4:
                        name = splitted_id[1] + '/' + splitted_id[2] + ' ' + splitted_id[3]
                    else:
                        name = splitted_id[1] + ' ' + splitted_id[2]
                elif equipment_type == 'mtr':
                    name = splitted_id[0] + '/' + splitted_id[1] + ' ' + splitted_id[2] + ' ' + splitted_id[3]
                names.append(name)
                comment = splitted_row[1]
                comments.append(comment)

        df = pd.DataFrame(
            {'id': ids, 'equipment': equipments, 'system': systems, 'name': names, 'place': '', 'product': '',
             'module': '', 'channel': '', 'crate': '', 'check': '', 'inversion': '', 'property': '', 'fb': fbs,
             'comment': comments, 'modbus': '', 'node': ''})
        df.to_excel(write_path)
    elif signal_type == 'ai':
        ids: list = []
        systems: list = []
        equipments: list = []
        names: list = []
        fbs: list = []
        comments: list = []
        rows = data.split(sep='\n')
        ymins: list = []
        ymaxs: list = []
        ahs: list = []
        als: list = []

        for row in rows:
            splitted_row = row.split(sep='\t')
            if splitted_row[0]:
                id = splitted_row[0]
                ids.append(id)
                systems.append('RSU_12')
                fbs.append('FB_AI')
                splitted_id = id.split(sep='_')
                equipment: str = splitted_id[0] + '-' + splitted_id[1]
                equipments.append(equipment)
                name: str = splitted_id[0] + '-' + splitted_id[1]
                names.append(name)
                comment = splitted_row[1]
                comments.append(comment)
                ymin: str = splitted_row[2]
                if ymin != '':
                    ymins.append(ymin)
                else:
                    ymins.append('none')
                ymax: str = splitted_row[3]
                if ymax != '':
                    ymaxs.append(ymax)
                else:
                    ymaxs.append('none')
                ah: str = splitted_row[4]
                if ah != '':
                    ahs.append(ah)
                else:
                    ahs.append('none')
                al: str = splitted_row[5]
                if al != '':
                    als.append(al)
                else:
                    als.append('none')



        df = pd.DataFrame(
            {'id': ids, 'system': systems, 'equipment': equipments, 'name': names, 'unit': '', 'place': '', 'product': '',
             'module': '', 'channel': '', 'crate': '', 'check': '', 'fb': fbs, 'property': '', 'comment': comments,
             'modbus': '', 'adr': '', 'sign': '', 'YMIN': ymins, 'YMAX': ymaxs, 'AH': ahs, 'WH': '', 'WL': '', 'AL': als, '2': '', 'node': '', 'filter': ''})
        df.to_excel(write_path)

signals_valve_di = signals_matches( 'valve', 'di')
write_signal_to_excel(signals_valve_di[0], 'Files/valve_di_' + signals_valve_di[1] + '.xlsx', 'valve', 'di')

signals_valve_do = signals_matches('valve', 'do')
write_signal_to_excel(signals_valve_do[0], 'Files/valve_do_' + signals_valve_do[1] + '.xlsx', 'valve', 'do')

signals_mtr_di = signals_matches('mtr', 'di')
write_signal_to_excel(signals_mtr_di[0], 'Files/mtr_di_' + signals_mtr_di[1] + '.xlsx', 'mtr', 'di')

signals_mtr_do = signals_matches('mtr', 'do')
write_signal_to_excel(signals_mtr_do[0], 'Files/mtr_do_' + signals_mtr_do[1] + '.xlsx', 'mtr', 'do')

signals_ai = signals_matches('ai', 'ai')
write_signal_to_excel(signals_ai[0], 'Files/ai_' + signals_ai[1] + '.xlsx', 'ai', 'ai')