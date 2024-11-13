import requests
import json
import pandas as pd
from datetime import datetime
from pathlib import Path


class AttendanceSheet:

    subjects = {
        "CN": 117584,
        "JAVA": 117583,
        "KM": 117582,
        "NUMERICAL": 117585,
        "MINOR_PROJECT": 117586
    }
    
    def __init__(self, student_name, student_id):
        self.StudentName = student_name
        self.StudentId = student_id


    def getSubData(self, subject_id):
        
        file_path = Path('{}.json'.format(subject_id))

        if file_path.is_file():
            print("{} JSON file exists.".format(subject_id))
            return

        url = "https://portal.vmedulife.com/api/learner/subject_api.php"

        payload = f'getLearnerAssignedSubjectSessionList=true&acayr=10&sid=2464&groupid=37112&subjectid={subject_id}&batchid=0'
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        data = response.json()

        with open(f'{subject_id}.json', 'w') as json_file: 
            json.dump(data, json_file, indent=4)

        print("JSON data has been saved to {}.json".format(subject_id))

    
    def get_all_subjects_data(self):
        # Fetch all subjects data from api
        for subject_name, subject_id in self.subjects.items():
            self.getSubData(subject_id)
    

    def generate_excel_sheet(self):
        for subject_name, subject_id in self.subjects.items():
            # Load subject json file
            with open(f'{subject_id}.json', 'r') as file:
                data = json.load(file)

            # Process subject data and generate excel sheet
            exceldata = [ ]

            i = 1
            for session in data['sorted_session_ids']:
                session_date = data['data'][session]['proposed_date']
                session_id = data['data'][session]['sessionId']
                attendance_status = data['data'][session]['attendanceStatus']
                faculty_name = data['data'][session]['faculty_name']
                absent_list = data['data'][session]["absent_students"].split(',')

                status = "Not Marked"
                
                if attendance_status == "Present":
                    if self.StudentId in absent_list:
                        status = "Absent"
                    else:
                        status = "Present"


                exceldata.append({ "S.No.": int(i), "SessionId": int(session_id), "Session Date": session_date, "Attendance Status": status, "Faculty Name": faculty_name})

                i = i+1


            df = pd.DataFrame(exceldata)
            df["Session Date"] = pd.to_datetime(df["Session Date"]).dt.date
            # Write the DataFrame to an Excel file
            df.to_excel("attendacnceSheet-[{}]-{}.xlsx".format(self.StudentName, subject_name), index=False)




if __name__ == "__main__":
    # Simply get your cookie and replace it
    kartikay = "370519"

    kartikaydata = AttendanceSheet("Kartikay","370519")
    kartikaydata.get_all_subjects_data()
    kartikaydata.generate_excel_sheet()









