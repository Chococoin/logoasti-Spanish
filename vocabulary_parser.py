import requests
import shutil
import os
import re

token_definitions = { "pronoun":"noun",
                      "noun":"noun",
                      "plural noun":"noun",
                      "masculine noun": "noun",
                      "femenine noun": "noun",
                      "geographical name": "noun",
                      "verb":"bi",
                      "intransitive verb":"bi",
                      "auxiliary verb": "bi",
                      "transitive verb":"du",
                      "impersonal verb": "du",
                      "reflessive verb": "se"
                    }


traslated_list = { "noun":"", "du":"", "es":"", "bi":"", "se":"" }

def spanish_traslations(lsta):
    global traslated_list
    print(lex, traslated_list)
    input("-> Enter to continue")
    os.system('clear')
    logoasti_Spanish.write('"spanish":\n')
    for token, traslation in lsta.items():
        if traslation:
            # TODO: Parse and clean list of words (traslations)
            logoasti_Spanish.write('"{}":"{}",\n'.format(token, traslation))
    logoasti_Spanish.write("#\n")
    lsta = ""
    traslated_list = { "noun":"", "du":"", "es":"", "bi":"", "se":"" }
    

def traslate_to_memory(to_traslate):
    to_json = open("./"+lex.strip('"') + "/" +(lex.strip('"') + ".json"), 'w')
    to_txt  = open("./"+lex.strip('"') + "/" +(lex.strip('"') + ".txt"), 'w')
    print("Logoasti Lexema: ", lex)
    print("Token: '{}' English words: {}".format(token, to_traslate))
    for words in to_traslate:
        wrd = words.strip().strip('"')
        wrd = wrd.lstrip(" ")
        print("Next word: [{}] to translate as [{}]".format(wrd, token))
        if re.search(" ", wrd):
            manual_entry_mode(wrd)
        elif re.search(":", wrd):
            wrd = wrd.split(":")[0]
            standard_process(wrd, to_json, to_txt)
        else:
            standard_process(wrd, to_json, to_txt)

    print("END OF FUNCTION", traslated_list)
    os.system('clear')
    to_json.close()
    to_txt.close()

def manual_entry_mode(wd):
    global traslated_list
    traslated_list[token] += input("(*) Manual Entry Mode: [{}]\n(*)-> ".format(wd))
    os.system('clear')
    print(traslated_list[token])


def standard_process(wrd, t_json, t_txt):
    query = "https://www.dictionaryapi.com/api/v3/references/spanish/json/{}?key={}".format(wrd ,secret)
    res = requests.get(query)
    res_content = res.json()
    print(res.url)
    if res.status_code == 200 and res_content[0] != str:
        t_json.write(res.text)
        for json in res_content:
            try:
                to_Spanish = json['meta']['src'] == 'spanish'
                from_English = json['meta']['lang'] == 'en'
                same_definition = token_definitions[json['fl']] == token
                match_word = re.search('^{}'.format(wrd), json['meta']['id'])
                # breakpoint()
                if  match_word and same_definition and from_English and to_Spanish:
                    print("Gramatical Token: {} / Functional Label: {}".format(token, json['fl']))
                    print("Proposed traduction: {}".format(json['shortdef']))
                    action = input("[0 + ENTER](add) | [. + ENTER](Manual Mode)| [ENTER](pass)\n->: ")
                    if action == '0':
                        t_txt.write(json['meta']['id']+ ": as (" + token + ")\n")
                        for definition in json['shortdef']:
                            t_txt.write("\t" + definition + "\n")
                            traslated_list[token] += definition.strip("\n") + ", "
                        os.system('clear')
                    if action == ".":
                        manual_entry_mode(wrd) 
            except TypeError:
                manual_entry_mode(wrd)                          
            except KeyError:
                # print("Exception: No 'fl' in json format.")
                pass
            except:
                print("Fatal Error")
                pass

    
logasti_English = open("vocabulary.txt", "r")
logoasti_Spanish = open("vocabulary2.txt", "a")

secret = open(".secret").readline()

source_new_line = True
to_traslate = None
token = None
count_line_in_source = 0

while(source_new_line):
    count_line_in_source += 1
    source_new_line = logasti_English.readline()
    lexeme = re.search('^\"lexeme\"', source_new_line)
    hasho  = re.search('^#', source_new_line)
    es     = re.search('^\"es\"', source_new_line)
    noun   = re.search('^\"noun\"', source_new_line)
    du     = re.search('^\"du\"', source_new_line)
    bi     = re.search('^\"bi\"', source_new_line)
    se     = re.search('^\"se\"', source_new_line)
    level  = re.search('^\"level\"', source_new_line)
    
    if level:
        continue
    if lexeme:
        lex = source_new_line.split(":")[1].rstrip(',\n')
        logoasti_Spanish.write('"lexeme":' + lex +',\n'+ '"english":\n')
        path = "./"+lex.strip('"')
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        continue
    if noun:
        to_traslate = source_new_line.split(":")[1].rstrip(',\n')
        logoasti_Spanish.write('"noun":' + to_traslate +',\n')
        to_traslate = to_traslate.split(",")
        token = "noun"
        traslate_to_memory(to_traslate)
        continue
    if du:
        to_traslate = source_new_line.split(":")[1].rstrip(',\n')
        logoasti_Spanish.write('"du":' + to_traslate +',\n')
        to_traslate = to_traslate.split(",")
        token = "du"
        traslate_to_memory(to_traslate)
        continue
    if es:
        to_traslate = source_new_line.split(":")[1].rstrip(',\n')
        logoasti_Spanish.write('"es":' + to_traslate +',\n')
        to_traslate = to_traslate.split(",")
        token = "es"
        traslate_to_memory(to_traslate)
        continue
    if bi:
        to_traslate = source_new_line.split(":")[1].rstrip(',\n')
        logoasti_Spanish.write('"bi":' + to_traslate +',\n')
        to_traslate = to_traslate.split(",")
        token = "bi"
        traslate_to_memory(to_traslate)
        continue
    if se:
        to_traslate = source_new_line.split(":")[1].rstrip(',\n')
        logoasti_Spanish.write('"se":' + to_traslate +',\n')
        to_traslate = to_traslate.split(",")
        token = "se"
        traslate_to_memory(to_traslate)
        continue
    if hasho:
        spanish_traslations(traslated_list)
        continue
    else:
        pass

logasti_English.close()
logoasti_Spanish.close()
