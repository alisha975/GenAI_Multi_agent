##tool
##@tool of data generation
from langchain_core.tools import tool
import pandas as pd
Images_folder='./plots'
@tool
def data_generation(user_id:int):

    """ 
        take user_id as input and return student_json in dict
    """
    physical_apperance=pd.read_csv(".\physical_apperance.csv")
    extra_circular_activity=pd.read_csv(".\Extra_circular_activities.csv")
    inovation_and_project=pd.read_csv(".\Innovation_and_projects.csv")
    academic_acheivements=pd.read_csv(".\Axademic_acheivements.csv",index_col=False)

    ##combined data
    merged_data=physical_apperance.merge(extra_circular_activity,on="id").merge(inovation_and_project,on="id").merge(academic_acheivements,on="id")
    student_data=merged_data[merged_data["id"]==user_id]
    student_json=student_data.to_dict(orient="records")

    return student_json


import matplotlib.pyplot as plt

##@tool for generating graph
@tool
def generate_graph(student_data:dict):

    """
        take input data in dict as input and return images of graph and description
    """

    name=student_data["first_name"]+" "+student_data["last_name"]
    Email=student_data["email"]
    Gender=student_data['gender']
    Height=student_data["Height"]
    Color=student_data["Color"]
    CGPA=student_data['cgpa']
    Positions=student_data['position']

# 
    keys=['cricket','dance','music','painting','swimming','Projects','Research_paper','App_development','Scholarship','Award'] #predefined keys
    activities_data={key:student_data[key] for key in keys} #new dictionary
    activities_detail_label=[]# new activities_detail_label
    for key,value in activities_data.items():
        activities_detail_label.append(f"{value}")

    categories=list(activities_data.keys()) #categories


###values
    values=[]
    for key,value in activities_data.items():
        if "No" in value:
            values.append("No")
        elif "no" in value:
            values.append("No")
        elif "Only" in value:
            values.append("Good")
        else:
            values.append("Yes")
# values=['Yes','Yes','Yes','Yes','Yes','Yes','Yes','Yes','No','No']

    colors=['green' if value=='Yes' else 'blue' if value=='Good' else 'red' for value in values]

    info={
        "Name":name,
        "Email":Email,
        "Gender":Gender,
        "Height":Height,
        "Color":Color,
        "Position":Positions,
        "CGPA":CGPA
        
    }
    

    fig,ax=plt.subplots(figsize=(8,6))
    bars=plt.barh(categories,[1] *len(categories),color=colors)

    for bar,label in zip(bars,activities_detail_label):
        plt.text(bar.get_width()+0.05,bar.get_y()+bar.get_height()/2, label, ha='left',va='center',fontsize=8,fontweight='bold')
    plt.xlabel('Status')
    plt.ylabel('Activity')
    plt.title(f'Activities and Achievements of {name}')
    # plt.show()

    #convert plot to image

    filename=f"Activities and Achievements of {name}.png"
    path_plot=f"{Images_folder}/{filename}"
    fig.savefig(path_plot,dpi=fig.dpi)
    # img_buf= BytesIO()
    # plt.savefig(img_buf,format='png')
    # plt.close(fig)

    # img_str=base64.b64decode(img_buf.getvalue()).decode('iso8859-1')
    return{
        "info":info,
        "image_location":path_plot
    }


    



