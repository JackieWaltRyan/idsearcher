import sys
from base64 import b64encode
from json import loads, dump, dumps
from os import walk, makedirs
from os.path import exists, join, abspath, dirname, isfile
from sys import exit, argv

from bs4 import BeautifulSoup


SETTINGS = {"Format": {"TXT": True,
                       "JSON": True,
                       "XML": True},
            "Categories": {},
            "XML": {"Decore": "            <StoredItem ID=\"{{ ID }}\" Count=\"1000\"/>",
                    "Pony": "            <StoredItem ID=\"{{ ID }}\" PonyLevel=\"0\"/>",
                    "Pony_House": "            <StoredItem ID=\"{{ ID }}\"/>",
                    "PonyPet": "            <StoredItem ID=\"{{ ID }}\" Count=\"1000\"/>",
                    "PonyPart": "            <Item ID=\"{{ ID }}\"/>",
                    "ProfileAvatar": "            <ProfileAvatarItemIdOwned id=\"{{ ID }}\"/>\n            <ProfileAvatarItemStatus id=\"{{ ID }}\" status=\"use\"/>",
                    "ProfileAvatarFrame": "            <ProfileAvatarFrameItemIdOwned id=\"{{ ID }}\"/>\n            <ProfileAvatarFrameItemStatus id=\"{{ ID }}\" status=\"use\"/>",
                    "RoadBuildingPermit": "            <OwnedRBP ID=\"{{ ID }}\"/>",
                    "Theme": "            <OwnedTheme ID=\"{{ ID }}\"/>"}}


def create_file_settings(data=None):
    try:
        print("0: Создание файла IDsearcher.json.\n")
        
        with open(file="IDsearcher.json",
                  mode="w") as settings_json:
            dump(obj=(data or SETTINGS),
                 fp=settings_json,
                 indent=4)
        
        return (data or SETTINGS)
    except Exception:
        print("[ERROR] Во время создания файла настроек IDsearcher.json возникла ошибка. "
              "Возможно нет прав на создания файлов.\n")
        
        return (data or SETTINGS)


def create_file_out(cat, file, data):
    try:
        trigger = True
        
        if not exists(path="IDsearcher"):
            print(f"3: Создание папки IDsearcher.\n")
            
            try:
                makedirs(name="IDsearcher")
            except Exception:
                print(f"[ERROR] Во время создания папки IDsearcher возникла ошибка. "
                      f"Возможно нет прав на создания папок.\n")
                
                trigger = False
        
        print(f"        Создание файла IDsearcher/{cat}.{file}.")
        
        if (file == "json"):
            with open(file=f"IDsearcher/{cat}.{file}",
                      mode="w") as output_file:
                dump(obj=data,
                     fp=output_file,
                     indent=4)
        else:
            with open(file=f"IDsearcher/{cat}.{file}",
                      mode="w",
                      encoding="UTF-8") as output_file:
                output_file.write(data)
        
        return trigger
    except Exception:
        print(f"[ERROR] Во время создания файла IDsearcher/{cat}.{file} возникла ошибка. "
              f"Возможно нет прав на создания файлов.\n")
        
        return False


def load_file_settings(cats):
    try:
        for cat in cats:
            SETTINGS["Categories"].update({cat: True})
        
        if exists(path="IDsearcher.json"):
            print("2: Обработка файла IDsearcher.json.\n")
            
            with open(file="IDsearcher.json",
                      mode="r",
                      encoding="UTF-8") as settings_json:
                try:
                    data = loads(s=settings_json.read())
                    
                    if (len(data) < len(SETTINGS)):
                        print("[INFO] В файле настроек IDsearcher.json отсутствуют некоторые параметры. "
                              "Эти параметры будут добавлены в файл со стандартными значениями.\n")
                        
                        for item in SETTINGS:
                            if (item not in data):
                                data.update({item: SETTINGS[item]})
                        
                        data = create_file_settings(data=data)
                    
                    if (len(data["Format"]) < len(SETTINGS["Format"])):
                        print("[INFO] В файле настроек IDsearcher.json отсутствуют некоторые параметры. "
                              "Эти параметры будут добавлены в файл со стандартными значениями.\n")
                        
                        for item in SETTINGS["Format"]:
                            if (item not in data["Format"]):
                                data["Format"].update({item: SETTINGS["Format"][item]})
                        
                        data = create_file_settings(data=data)
                    
                    if (len(data["Categories"]) < len(SETTINGS["Categories"])):
                        print("[INFO] В файле настроек IDsearcher.json отсутствуют некоторые параметры. "
                              "Эти параметры будут добавлены в файл со стандартными значениями.\n")
                        
                        for item in SETTINGS["Categories"]:
                            if (item not in data["Categories"]):
                                data["Categories"].update({item: SETTINGS["Categories"][item]})
                        
                        data = create_file_settings(data=data)
                        
                    return data
                except Exception:
                    print("[INFO] Не удалось прочитать файл настроек IDsearcher.json. "
                          "Возможно данные в файле повреждены. "
                          "Будет создан новый файл со стандартными настройками.\n")
                    
                    return create_file_settings()
        else:
            print("[INFO] Файл настроек IDsearcher.json не обнаружен. "
                  "Будет создан новый файл со стандартными настройками.\n")
            
            return create_file_settings()
    except Exception:
        print("[ERROR] Во время обработки файла настроек IDsearcher.json возникла ошибка. "
              "Возможно данные в файле повреждены или нет прав на чтение файлов.\n")
        
        return SETTINGS


def parse_gameobjectdata(file, folder):
    try:
        trigger = True
        
        print(f"1: Обработка файла {folder}{file}.\n")
        
        with open(file=f"{folder}{file}",
                      mode="r",
                      encoding="UTF-8") as gameobjectdata_xml:
            soup = BeautifulSoup(markup=gameobjectdata_xml.read(),
                                     features="xml").find_all(name="GameObjects",
                                                              limit=1)[0]
            
            cats = [x["ID"] for x in soup.find_all(name="Category")]
            
            settings = load_file_settings(cats=cats)
            
            if (True not in settings["Format"].values()):
                print("[ERROR] В файле настроек IDsearcher.json в разделе \"Format\" не включен ни один параметр. "
                      "Для работы программы нужно включить хотя бы один.\n")
                    
                trigger = False
            
            if (True not in settings["Categories"].values()):
                print("[ERROR] В файле настроек IDsearcher.json в разделе \"Categories\" не включен ни один параметр. "
                      "Для работы программы нужно включить хотя бы один.\n")
                    
                trigger = False
                
            if trigger:
                for cat in settings["Categories"]:
                    if (settings["Categories"][cat] and (cat in SETTINGS["Categories"])):
                        print(f"    Поиск всех {cat}...")
                        
                        try:
                            data_raw, data_txt, data_json, data_xml = [], "", [], ""
                            i, items = 1, soup.find_all(name="Category",
                                                        attrs={"ID": cat},
                                                        limit=1)[0]
                            
                            for item in items:
                                print(f"\r        Обработано {i} из {len(items)}.", end="")
                                
                                if (len(item) > 1):
                                    res_id = ""
                                    
                                    try:
                                        res_id = item["ID"]
                                    except Exception:
                                        pass
                                    
                                    if res_id:
                                        data_raw.append(res_id)
                                
                                i += 1
                                
                            print("\n")

                            if (len(data_raw) > 0):
                                data_json = sorted(data_raw, key=str.lower)
                            
                                if settings["Format"]["TXT"]:
                                    for data_id in data_json:
                                        data_txt += f"{data_id}\n"
                                    
                                    trigger = create_file_out(cat=cat, file="txt", data=data_txt) if trigger else False
                            
                                if settings["Format"]["JSON"]:
                                    trigger = create_file_out(cat=cat, file="json", data=data_json) if trigger else False
                            
                                if settings["Format"]["XML"]:
                                    for data_id in data_json:
                                        if (cat in settings["XML"]):
                                            placeholder = settings["XML"][cat]
                                                
                                            data_xml += f"{placeholder}\n".replace("{{ ID }}", data_id)
                                        else:
                                            data_xml += f"{data_id}\n"
                                                
                                    trigger = create_file_out(cat=cat, file="xml", data=data_xml) if trigger else False
                            
                            print("")
                        except Exception:
                            print(f"[WARNING] Во время обработки категории {cat} возникла ошибка. "
                                  f"Возможно данные в файле повреждены или нет прав на чтение файлов. "
                                  f"Категория пропущена.\n")
                            
                            trigger = False
                
            return trigger
    except Exception:
        print(f"[ERROR] Во время обработки файла {folder}{file} возникла ошибка. "
              f"Возможно данные в файле повреждены или нет прав на чтение файлов.\n")
        
        return False


def load_files():
    try:
        files = [x for x in argv[1:] if (isfile(path=x) and x.endswith("gameobjectdata.xml"))]
        
        if (len(files) > 0):
            return parse_gameobjectdata(file=files[0], folder="")
        else:
            if exists(path="000_and_mlpextra_common/gameobjectdata.xml"):
                return parse_gameobjectdata(file="gameobjectdata.xml", folder="000_and_mlpextra_common/")
            else:
                print("[ERROR] Отсутствует папка 000_and_mlpextra_common или в ней нет файла gameobjectdata.xml. "
                      "Разархивируйте архив 000_and_mlpextra_common.ark используя программу ARKdumper.\n")
                
                return False
    except Exception:
        print("[ERROR] Во время обработки файлов возникла ошибка. "
              "Возможно данные в файлах повреждены или нет прав на чтение файлов.\n")
        
        return False


if __name__ == "__main__":
    try:
        if load_files():
            exit()
        else:
            raise Exception
    except Exception:
        input()
        exit()
