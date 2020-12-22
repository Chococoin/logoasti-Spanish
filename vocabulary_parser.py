import requests
import shutil
import os
import re

traslated_list = { "noun":"", "du":"", "es":"", "bi":"", "se":"" }
no_pause = True

def spanish_traslations(lsta):
    global traslated_list
    logoasti_Spanish.write('"spanish":\n')
    for token, traslation in lsta.items():
        if traslation:
            # TODO: Parse and clean list of words (traslations)
            logoasti_Spanish.write('"{}":"{}",\n'.format(token, traslation))
    logoasti_Spanish.write("#\n")


def traslate_to_memory(to_traslate):
    to_json = open("./apidata/"+lex.strip('"') + "/" +(lex.strip('"') + ".json"), 'w')
    to_txt  = open("./apidata/"+lex.strip('"') + "/" +(lex.strip('"') + ".txt"), 'w')
    for words in to_traslate:
        wrd = words.strip().strip('"')
        wrd = wrd.lstrip(" ")
        if re.search(" ", wrd):
            manual_entry_mode(wrd)
        elif re.search(":", wrd):
            wrd = wrd.split(":")[0]
            standard_process(wrd, to_json, to_txt, to_traslate)
        else:
            standard_process(wrd, to_json, to_txt, to_traslate)
    os.system('clear')
    print("Traslated Result < {} >: ".format(token), traslated_list)
    to_json.close()
    to_txt.close()

def manual_entry_mode(wd):
    global traslated_list
    print("Lexeme:[ {} ]".format(lex))
    intext = input("(*) Manual Entry Mode: [{}] as [{}]\n(*)-> ".format(wd, token))
    if intext == "PAUSE":
        pause()
    if intext == "BRK":
        return "break"  
    else:
        traslated_list[token] += intext
    os.system('clear')

def standard_process(wrd, t_json, t_txt, to_trasl):
    query = "https://www.dictionaryapi.com/api/v3/references/spanish/json/{}?key={}".format(wrd ,secret)
    res = requests.get(query)
    res_content = res.json()
    if res.status_code == 200 and res_content[0] != str:
        print(res.url)
        print("Traslated Result < {} >: ".format(token), traslated_list)
        t_json.write(res.text)
        for json in res_content:
            try:
                to_Spanish = json['meta']['src'] == 'spanish'
                from_English = json['meta']['lang'] == 'en'
                match_word = re.search('^{}'.format(wrd), json['meta']['id'])
                if  match_word and from_English and to_Spanish:
                    print("Logoasti Lexema: ", lex)
                    print("English words: {}".format(to_trasl))
                    print("Next word: [{}] to translate as [{}]".format(wrd, token))
                    print("Gramatical Token: {} / Functional Label: {}".format(token, json['fl']))
                    print("Proposed traduction: {}".format(json['shortdef']))
                    action = input("[0 + ENTER](add) | [. + ENTER](Manual Mode)| [ENTER](pass)\n->: ")
                    if action == '0':
                        t_txt.write(json['meta']['id']+ ": as (" + token + ")\n")
                        for definition in json['shortdef']:
                            t_txt.write("\t" + definition + "\n")
                            traslated_list[token] += definition.strip("\n") + ", "
                        os.system('clear')
                        pass
                    if action == ".":
                        manual_entry_mode(wrd)
                        os.system('clear')
                        pass
                    if  len(action) >= 3 and action != "PAUSE":
                        traslated_list[token] += action + ", "
                        os.system('clear')
                        print(traslated_list[token])
                        pass
                    if action == "PAUSE":
                        pause()
                    else:
                        pass
                        os.system('clear')
                else:
                    print("Logoasti Lexema: ", lex)
                    print("English words: {}".format(to_trasl))
                    print("Next word: [{}] to translate as [{}]".format(wrd, token))
                    print("Gramatical Token: {} / Functional Label: {}".format(token, json['fl']))
                    print("Proposed traduction: {}".format(json['shortdef']))
                    manual_entry_mode(wrd)
            except TypeError:
                print("From except Type error")
                manual_entry_mode(wrd)
                pass                        
            except KeyError:
                print("Exception: No 'fl' in json format.")
                manual_entry_mode(wrd)                         
                pass
            except:
                print("Fatal Error")
                pass
    else:
        print("Logoasti Lexema: ", lex)
        print("English words: {}".format(to_trasl))
        print("Next word: [{}] to translate as [{}]".format(wrd, token))
        print("Gramatical Token: {} / Functional Label: {}".format(token, json['fl']))
        print("Proposed traduction: {}".format(json['shortdef']))

def pause():
    global no_pause
    paused_line = open('last_line.txt', 'w')
    paused_line.write(str(last_lex_line))
    paused_line.close()
    no_pause = False
    exit()

    
logasti_English = open("vocabulary.txt", "r")
logoasti_Spanish = open("vocabulary2.txt", "a")

secret = open(".secret").readline().rstrip(" ")
try:
    last_line = int(open("last_line.txt").readline().rstrip(" "))
except ValueError:
    last_line = 1

source_incoming_new_line = True
to_traslate = None
token = None
count_line_in_source = 0
notes = False
last_lex_line = 0

while(source_incoming_new_line and no_pause):
    count_line_in_source += 1
    source_incoming_new_line = logasti_English.readline()
    if count_line_in_source >= last_line:
        lexeme    = re.search('^\"lexeme\"', source_incoming_new_line)
        hasho     = re.search('^#', source_incoming_new_line)
        es        = re.search('^\"es\"', source_incoming_new_line)
        noun      = re.search('^\"noun\"', source_incoming_new_line)
        du        = re.search('^\"du\"', source_incoming_new_line)
        bi        = re.search('^\"bi\"', source_incoming_new_line)
        se        = re.search('^\"se\"', source_incoming_new_line)
        level     = re.search('^\"level\"', source_incoming_new_line)
        note      = re.search('^\"notes\"', source_incoming_new_line)
        special   = re.search('^\"special\"', source_incoming_new_line)
        
        if level:
            continue
        if lexeme:
            lex = source_incoming_new_line.split(":")[1].rstrip(',\n')
            logoasti_Spanish.write('"lexeme":' + lex + ',\n' + '"english":\n')
            path = "./" + lex.strip('"')
            if os.path.exists(path):
                shutil.rmtree(path)
            os.mkdir(path)
            last_lex_line = count_line_in_source
            continue
        if note:
            notes = source_incoming_new_line.split(":")
            continue
        if special:
            try:
                logoasti_Spanish.write('"notes:' + notes[1] + ": " + notes[2].strip() +'\n')
            except:
                logoasti_Spanish.write('"notes:' + notes[0] + '\n')
            logoasti_Spanish.write('"special:' + source_incoming_new_line.split(":")[1].rstrip(',\n') +'\n')
            path = "./z_specials/" + lex.strip('"')
            if os.path.exists(path):
                shutil.rmtree(path)
            os.mkdir(path)
            to_note = open(path + "/" + ".txt", 'w+')
            try:
                to_note.write(notes[1] + notes[2])
            except:
                to_note.write(notes[0])
            to_note.close()
            if os.path.exists(lex.strip('"')):
                shutil.rmtree(lex.strip('"'))
            continue
        if noun:
            to_traslate = source_incoming_new_line.split(":")[1].rstrip(',\n')
            logoasti_Spanish.write('"noun":' + to_traslate +',\n')
            to_traslate = to_traslate.split(",")
            token = "noun"
            traslate_to_memory(to_traslate)
            continue
        if du:
            to_traslate = source_incoming_new_line.split(":")[1].rstrip(',\n')
            logoasti_Spanish.write('"du":' + to_traslate + ',\n')
            to_traslate = to_traslate.split(",")
            token = "du"
            traslate_to_memory(to_traslate)
            continue
        if es:
            to_traslate = source_incoming_new_line.split(":")[1].rstrip(',\n')
            logoasti_Spanish.write('"es":' + to_traslate + ',\n')
            to_traslate = to_traslate.split(",")
            token = "es"
            traslate_to_memory(to_traslate)
            continue
        if bi:
            to_traslate = source_incoming_new_line.split(":")[1].rstrip(',\n')
            logoasti_Spanish.write('"bi":' + to_traslate + ',\n')
            to_traslate = to_traslate.split(",")
            token = "bi"
            traslate_to_memory(to_traslate)
            continue
        if se:
            to_traslate = source_incoming_new_line.split(":")[1].rstrip(',\n')
            logoasti_Spanish.write('"se":' + to_traslate + ',\n')
            to_traslate = to_traslate.split(",")
            token = "se"
            traslate_to_memory(to_traslate)
            continue
        if hasho:
            if notes:
                if traslated_list['noun'] != '':
                    logoasti_Spanish.write('"spanish":' + '\n' + '\"noun":\"' + traslated_list['noun'] + '",\n')
                    notes = False
                    special = False
                    traslated_list['noun'] = ''
                logoasti_Spanish.write("#\n")
                traslated_list = { "noun":"", "du":"", "es":"", "bi":"", "se":"" }
            else:
                spanish_traslations(traslated_list)
                traslated_list = { "noun":"", "du":"", "es":"", "bi":"", "se":"" }
                continue
        else:
            pass

logasti_English.close()
logoasti_Spanish.close()
pause()
