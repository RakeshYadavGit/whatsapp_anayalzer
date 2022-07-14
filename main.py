from preprocessor import date_time, getDatapoint
def get_List(uploaded_file):
    data = []
    with open(uploaded_file, encoding="utf-8") as fp:
        fp.readline()
        messageBuffer = []
        date, time, author = None, None, None
        while True:
            line = fp.readline()
            if not line:
                break
            line = line.strip()
            if date_time(line):
                if len(messageBuffer) > 0:
                    data.append([date, time, author, ' '.join(messageBuffer)])
                messageBuffer.clear()
                date, time, author, message = getDatapoint(line)
                messageBuffer.append(message)
            else:
                messageBuffer.append(line)
    return date

