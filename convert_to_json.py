import json
import os
import codecs

def parse_file(filename, output_filename):
    file_content = []
    print filename
    with codecs.open(filename, encoding='iso-8859-2') as file:
        file_content = file.readlines()
    questions = []
    last_question = None
    inside_question = False
    correct_answer = None
    for line in file_content:
        try:
            line = line.rstrip()   
            if line == "":
                continue
            elif line[0] == "#":
                if last_question is not None:
                    last_question["correct_answer"] = last_question["answers"].index(correct_answer)
                    questions.append(last_question)
                    
                last_question = {
                    "content": line[3:],
                    "answers": [],
                }
                inside_question = True
            elif line[0] == "^":
                correct_answer = line[2:]
                inside_question = False
            elif line[0] == "A" or line[0] == "B" or line[0] == "C" or line[0] == "D":
                last_question["answers"].append(line[2:])
            elif inside_question:
                last_question["content"] += "\n" + line
            elif line.strip() != "":
                raise Exception("Can't parse line in file {0}: {1}".format(filename, line))
        except:
            print line
            print last_question
            raise
    
    if last_question is not None:
        last_question["correct_answer"] = last_question["answers"].index(correct_answer)
        questions.append(last_question)

    with codecs.open(output_filename, 'w', encoding='utf8') as output_file:
        output_file.write(json.dumps(questions, indent=4, ensure_ascii=False, encoding='utf8'))

if __name__ == "__main__":
    directory = 'categories'
    files = os.listdir(directory)
    for file in files:
        if not file.startswith('.'):
            parse_file(os.path.join(directory, file), os.path.join('json', file + ".json"))
    
