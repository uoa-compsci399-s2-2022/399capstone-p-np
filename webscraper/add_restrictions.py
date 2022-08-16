import json
import sqlite3
import re

for name in names:
    for course in data[name]:
        for req in course[3]:
            if req.split(" ")[0] == "Restriction:":
                restrictions = []
                clean_req =  " ".join(req.split(" ")[1:])
                clean_req=re.sub(",","",clean_req)

                mainSubject = course[0]
                mainID = course[1]
                currentSubject = "This is Problematic"
                currentID = "this is also problematic"

                word_num = 0        
                for x in clean_req.split(" ")[1:]:
                    if x not in coursenames and x not in courseids and x not in ["and", "or"]:
                        break
                    else:
                        print(clean_req)
                        for restriction in clean_req.split(" ")[1:]:
                            if restriction in coursenames:
                                currentSubject = restriction
                            else:
                                currentID = restriction
                                restrictions.append((mainSubject, mainID, currentSubject, currentID))




