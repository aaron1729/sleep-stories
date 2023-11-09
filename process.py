file = open("stories/des-moines_2023-11-08_20-10-09.txt", "r").read()

# this is a list of strings. each one is a single full response from chat GPT.
chunks = file.split("=====")

def process_chunk(string):
    string = string.strip()
    list_old = string.split("\n\n")
    list_new = []
    for paragraph in list_old:
        paragraph_replaced = paragraph.replace("\"", "'")
        paragraph_with_quotes = "\"" + paragraph_replaced + "\""
        list_new.append(paragraph_with_quotes)
    return list_new

processed_chunks = []
for chunk in chunks:
    processed_chunk = process_chunk(chunk)
    processed_chunks.append(processed_chunk)

def chunk_to_listOf(string_list):
    output = "listOf("
    for paragraph in string_list:
        output += paragraph + ", "
    output = output[:-2] + ")"
    return output

kotlin_kode = "val story = listOf("
for chunk in processed_chunks:
    listOf = chunk_to_listOf(chunk)
    kotlin_kode += "\n" + listOf + ","
kotlin_kode = kotlin_kode[:-1] + "\n)"

# print(kotlin_kode)

newfile = open("des-moines_kotlin_kode.txt", "w")
newfile.write(kotlin_kode)
newfile.close()