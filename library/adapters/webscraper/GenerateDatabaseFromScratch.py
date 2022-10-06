import GenerateDatabaseTables
import InsertCoursesIntoDatabase
import InsertGenEdsToDatabase
import ScrapeMajorRequirementsJSON
import AddMajorRequirementsToDatabase


insert into schedule (scheduleID, majorID)  select scheduleID, majorID from  schedule inner join majorRequirements on scheduleID == "Open Schedule" or scheduleID == "Engineering, Medical and Health Sciences, Science (EMHSS) Schedule";
