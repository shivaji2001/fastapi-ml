from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
from fastapi import HTTPException,Path,Query
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
app=FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description="ID of the patient",example="P001")]
    name:Annotated[str,Field(...,description="Name of the patient")]
    city:Annotated[str,Field(...,description="City of the patient")]
    age:Annotated[int,Field(...,gt=0,lt=120,description="Age of the patient")]
    gender:Annotated[Literal['male','female','others'],Field(...,description="Gender of the patient")]
    height:Annotated[float,Field(...,gt=0,description="Height of patient in meters")]
    weight:Annotated[float,Field(...,gt=0,description="Weight of patient in kgs")]
    @computed_field
    @property
    def bmi(self)->float:
        return round( self.weight/(self.height**2) ,2)
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return "underweight"
        elif self.bmi<30:
            return "normal"
        else:
            return "Obese"

class UpdatePatient(BaseModel):
    name:Annotated[Optional[str],Field(description="Name of the patient")]=None
    city:Annotated[Optional[str],Field(description="City of the patient")]=None
    age:Annotated[Optional[int],Field(gt=0,lt=120,description="Age of the patient")]=None
    gender:Annotated[Optional[Literal['male','female','others']],Field(description="Gender of the patient")]=None
    height:Annotated[Optional[float],Field(gt=0,description="Height of patient in meters")]=None
    weight:Annotated[Optional[float],Field(gt=0,description="Weight of patient in kgs")]=None

def getDummyData():
    with open("data.json","r") as f:
        return json.load(f)
def savePatientsData(patients):
    with open('data.json','w') as f:
        json.dump(patients,f)


@app.get("/")
def startMsg():
    return "Patient Management backend is running"


@app.post("/create")
def create_patient(patient:Patient):
    patients=getDummyData()
    if patient.id in patients:
        raise HTTPException(status_code=400,detail="This patient id already exists")
    patients[patient.id]=patient.model_dump(exclude=['id'])
    savePatientsData(patients)
    return JSONResponse(status_code=201,content={'msg':"Data inserted successfully"})

@app.put("/update/{id}")
def update_patient(id:str,patient:UpdatePatient):
    patients_data=getDummyData()
    if id not in patients_data:
        raise HTTPException(status_code=400,detail="Patient with this id not found")
    patient_data=patients_data[id]
    updated_data=patient.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        patient_data[key]=value
    patient_data['id']=id
    new_patient_obj=Patient(**patient_data)
    new_patient_dict_data=new_patient_obj.model_dump(exclude=['id'])
    patients_data[id]=new_patient_dict_data
    savePatientsData(patients_data)
    return JSONResponse(status_code=200,content={'MSG':f"Data updated successfully for the patient with id:{id}"})
    
@app.delete("/delete/{id}")
def delete_patient(id:str):
    patients_data=getDummyData()
    if id not in patients_data:
        raise HTTPException(status_code=400,detail="Patient with this id is not present")
    del patients_data[id]
    savePatientsData(patients_data)
    return JSONResponse(status_code=200,content={"Msg":f"Successfully deleted the patient with id:- {id}"})




@app.get("/about")
def aboutMsg():
    return "This is shivanshu's backend"

@app.get("/patients")
def loadData():
    return getDummyData()

@app.get("/patient/{patient_id}")
def get_patient(patient_id:str=Path(...,description="to get the patient detail using its id",examples="P001")):
    data=getDummyData()
    if patient_id not in data:
        raise HTTPException(404,detail="Patient with this id is not present")
    
    return data[patient_id]

@app.get("/sort")
def getsortedpatient(sort_by:str=Query(...,description="pass values like age, weight",examples="age") ,order_by:str=Query(...,description="asc or desc")):
    allowed_sortby=["age","weight"]
    if sort_by not in allowed_sortby:
        raise HTTPException(400,detail="This sort_by value is not applicable")
    allowed_orderby=["asc","desc"]
    if order_by not in allowed_orderby:
        raise HTTPException(400,detail="You can only sort by asc or desc")
    should_reverse=True if order_by=="desc" else False
    data=getDummyData()
    sorted_data=sorted(data.items(),key=lambda x:x[1][sort_by],reverse=should_reverse)
    return sorted_data
