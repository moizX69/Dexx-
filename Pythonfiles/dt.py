from datetime import datetime

# datetime object containing current date and time

def getdate():
    now = datetime.now()



    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string.split()[0]



