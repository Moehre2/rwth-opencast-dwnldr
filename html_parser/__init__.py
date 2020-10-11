# (c) 2020 Moehre2

from html.parser import HTMLParser

parsed_values = []
parsing_level = 0
parsing_buffer = ""

class CustomHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global parsing_level
        global parsing_buffer
        if parsing_level == 0 and tag == "p":
            parsing_level = 1
        elif parsing_level == 1 and tag == "video":
            parsing_level = 2
        elif parsing_level == 1 and tag == "a":
            parsing_buffer = attrs[0][1]
            parsing_level = 6
        elif parsing_level == 2 and tag == "source":
            parsing_level = 3

    def handle_data(self, data):
        global parsed_values
        global parsing_level
        global parsing_buffer
        if parsing_level == 1:
            parsing_buffer = data[:-2]
        elif parsing_level == 3:
            parsed_values.append({"name": parsing_buffer, "guid": data})
            parsing_level = 4
            parsing_buffer = ""
        elif parsing_level == 6:
            parsed_values.append({"name": data, "guid": parsing_buffer})
            parsing_level = 7
            parsing_buffer = ""

    def handle_endtag(self, tag):
        global parsing_level
        if parsing_level == 4 and tag == "video":
            parsing_level = 5
        elif parsing_level == 7 and tag == "a":
            parsing_level = 8
        if tag == "p":
            parsing_level = 0

def check_file_ending(inputfile):
    return inputfile.endswith(('.html', '.htm'))

def parse_file(htmlfilepath):
    global parsed_values
    parse_successful = True
    try:
        htmlfile = open(htmlfilepath, "r")
        parser = CustomHTMLParser()
        parser.feed(htmlfile.read())
        htmlfile.close()
    except:
        parse_successful = False
    return parse_successful

def url2guid():
    global parsed_values
    for obj in parsed_values:
        obj["guid"] = obj["guid"][-36:]

def get_parsed_values():
    global parsed_values
    return parsed_values
