import streamlit as st

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go

import warnings
warnings.filterwarnings("ignore")


def app():
    @st.cache(allow_output_mutation=True)
    def load_data():
        data = pd.read_csv('crimes.csv')  
        c11 = pd.read_csv('india2011.csv')  
        lit= pd.read_csv('Literacy.csv')  
        
        data=data.iloc[:,1:]
        tc=c11.groupby("State name").sum().reset_index().sort_values("State name")
        c11p=c11[["District name","Population", "State name"]]
        c11p.columns=["DISTRICT","Population", "State"]
        
        lit.columns=['Unnamed: 0','DISTRICT', 'State', 'Literacy']
        lit.drop("Unnamed: 0", axis=1,inplace=True)
        
        lit["DISTRICT"]=lit["DISTRICT"].str.lstrip()
        lit.drop("State",axis=1,inplace=True)    
        
        for i in range (0, len(c11["State name"])):
            c11["State name"][i]=c11["State name"][i].title()
            c11["District name"][i]=c11["District name"][i].title()
            
        for i in range (0, len(data['Year'])):
            data['DISTRICT'][i]=data['DISTRICT'][i].title()
            data['STATE/UT'][i]=data['STATE/UT'][i].title()

        for i in range(0,len(data["Year"])):
            if data['DISTRICT'][i] in ["Total District(S)", "Zz Total", "Delhi Ut Total"]:
                data['DISTRICT'][i]="Total"

        for i in range(0,len(data["Year"])):
            if data['STATE/UT'][i] =="D&N Haveli":
                data['STATE/UT'][i]="D & N Haveli"   

        for i in range(0,len(data["Year"])):
            if data['STATE/UT'][i] =="Delhi Ut":
                data['STATE/UT'][i]="Delhi"         

        for i in range(0,len(data["Year"])):
            if data['STATE/UT'][i] =="A&N Islands":
                data['STATE/UT'][i]="A & N Islands"    
            
        #this is done because there are a lot of UTs divided by direction, ie., Delhi ans Sikkim both has North, South district.

        for i in range(0,len(data["Year"])):
            if data['DISTRICT'][i] in ["South", "North", "East", "West"]:
                data['DISTRICT'][i]= str(data["STATE/UT"][i]) + " "+  str(data['DISTRICT'][i])    

        sd=data[["STATE/UT", "DISTRICT"]].drop_duplicates()
        
        
        for i in range (0, len(data["DISTRICT"])):
            if data["DISTRICT"][i] == "Coochbehar":
                data["DISTRICT"][i]= "Koch Bihar"

            elif data["DISTRICT"][i] == "Malda":
                data["DISTRICT"][i]= "Maldah"

            elif data["DISTRICT"][i] in  ["24 Parganas North","North 24 Parganas"]:
                data["DISTRICT"][i]= "North Twenty Four Parganas"  

            elif data["DISTRICT"][i] in  ["24 Parganas South","South 24 Parganas"]:
                data["DISTRICT"][i]= "South Twenty Four Parganas"   
            elif data["DISTRICT"][i] == "Hooghly":
                data["DISTRICT"][i] = "Hugli"

            elif data["DISTRICT"][i] == "Hyderabad City":
                data["DISTRICT"][i] = "Hyderabad"

            elif data["DISTRICT"][i] == "Cyberabad":
                data["STATE/UT"][i] = "Andhra Pradesh"
            
            District_Total= data.groupby("DISTRICT").sum()

            #Lets add Population and Literacy to every individual District

            District_Total=pd.merge(District_Total,c11p, on = "DISTRICT", how="left")
            District_Total=pd.merge(District_Total,lit, on = "DISTRICT", how="left")
            # District_Total = pd.merge(District_Total,sd, on = "DISTRICT", how="left")
            District_Total20=District_Total.sort_values(by="Rape", ascending=False).reset_index().head(22)
            District_Total20.drop(0,axis=0,inplace=True)  
            
            
            # We will use join(inner join) to concate two tables

            state_total=data[data["DISTRICT"]=="Total"]
            label10=np.arange(1,11)
            label20=np.arange(0,20)

        return data, District_Total, state_total, c11p, lit


    data_re, District_Total_re , state_total_re,c11p, lit =load_data()
    data=data_re
    District_Total = District_Total_re
    state_total = state_total_re
    st.title("Crime against Women(2001-2014, India) Data Analysis and Visulization")


    st.text("""
    Disclaimer(please read it):
    
    This analysis and visualization is only for educational purposes, use of below
    graphs and analysis is strictly prohibited in any official or political work.
     
    Reason: Data is not well organised, dataset has various issues.In case of any
    query/issue, please connect through provided username in Footer! 
     
    Brief:Data is gathered from three different sources.

    Crimes against women data from Data.gov.in(CSV File)
    India 2011 Census Data from kaggle.com(CSV File)
    Literacy Data(based on Census 2011) from census2011.co.in/district.php(Data 
    was scraped and then stored into CSV file).
    
    As data is gathered from different sources there are some issues, I tried my best 
    to minimize them. For example, there were spelling differences with multiple 
    West Bengal districts and Cyberabad is notmentioned in Census data.Another important
    thing is to be noted that the Literacy and Population data isfrom the 2011 India
    Census and is used against all years between 2001 to 2014.
    
    Bonus Point: This notebook is made using Plotly library, you can zoom-in the graph,
    hover the point using the mouse to see detailed information in the cartesian
    planeand last 3D plot can be rotated 360 using mouse and hovering over the Scatter
    point will show you multiple information with that particular point

    """)

    label10=np.arange(1,11)
    label20=np.arange(0,20)
    ydata=data.groupby("Year").sum().reset_index()
    #Lets see the line graph for years between 2001 to 2014
    st.subheader('Line graph for years between 2001 to 2014 for all the Crimes against Women')

    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ydata.Year, y=ydata.Rape,
                                mode='lines+markers',
                                name='Rape',
                                hovertext="Rape", ))
    fig.add_trace(go.Scatter(x=ydata.Year, y=ydata["Dowry Deaths"],
                                mode='lines+markers',
                                name='Dowry Deaths'))
    fig.add_trace(go.Scatter(x=ydata.Year, y=ydata["Kidnapping and Abduction"],
                                mode='lines+markers',
                                name='Kidnapping and Abduction',
                                hovertext="Kidnapping and Abduction"))
    fig.add_trace(go.Scatter(x=ydata.Year, y=ydata["Importation of Girls"],
                                mode='lines+markers', 
                                name='Importation of Girls',
                                hovertext='Importation of Girls'))
    fig.add_trace(go.Scatter(x=ydata.Year, y=ydata["Cruelty by Husband or his Relatives"],
                                mode='lines+markers', 
                                name='Cruelty by Husband or his Relatives',
                                hovertext='Cruelty by Husband or his Relatives'))
    fig.add_trace(go.Scatter(x=ydata.Year, y=ydata["Insult to modesty of Women"],
                                mode='lines+markers',
                                name='Insult to modesty of Women',
                                hovertext='Insult to modesty of Women'))
    fig.add_trace(go.Scatter(x=ydata.Year, y=ydata["Assault on women with intent to outrage her modesty"],
                                mode='lines+markers',
                                name='Assault on women '
                                , hovertext="Assault on women with intent to outrage her modesty"))

    fig.update_layout(
                title="", 
                plot_bgcolor='rgba(0,0,0,0)', width= 900)
    st.plotly_chart(fig)


    st.write("We can see a sudden surge in Rape, Assault on women with intent to outrage her modesty and Kidnapping and Abduction after 2012. One of the main reasons for this could be Nirbhaya Delhi Case, after this, India got a moment of awareness and people started coming out against the crimes.")
    
    st.subheader("Total Crimes in each States(Dropdown for Bar Graph and Pie Chart) ")
    st.write("Hint: Here we have added all the crimes into one column for each state.")
    vis_type=st.selectbox("Select Bar Graph or Pie Chart?",["Bar Graph", "Pie Chart"])
    if vis_type=="Bar Graph":
        state_total_for_pie=state_total.groupby("STATE/UT").sum()
        state_total_for_pie["Total"]= state_total_for_pie["Rape"]+ state_total_for_pie["Kidnapping and Abduction"] + state_total_for_pie["Dowry Deaths"]+state_total_for_pie["Insult to modesty of Women"]+state_total_for_pie["Cruelty by Husband or his Relatives"]+state_total_for_pie["Importation of Girls"]
        state_total_for_pie=state_total_for_pie.sort_values(by="Total")
        fig=go.Figure(data=[go.Bar(x=state_total_for_pie.index,y=state_total_for_pie['Total'], marker={"color":np.arange(0, len(state_total_for_pie['Total']))})])
        fig.update_layout(autosize=True,plot_bgcolor='rgba(0,0,0,0)' )
        st.plotly_chart(fig)

    elif vis_type=="Pie Chart"  :
        state_total_for_pie=state_total.groupby("STATE/UT").sum()
        state_total_for_pie["Total"]= state_total_for_pie["Rape"]+ state_total_for_pie["Kidnapping and Abduction"] + state_total_for_pie["Dowry Deaths"]+state_total_for_pie["Insult to modesty of Women"]+state_total_for_pie["Cruelty by Husband or his Relatives"]+state_total_for_pie["Importation of Girls"]
        state_total_for_pie=state_total_for_pie.sort_values(by="Total")
        fig=go.Figure(data=[go.Pie(labels=state_total_for_pie.index,values=state_total_for_pie['Total'])])
        fig.update_traces(hoverinfo='label+percent', textinfo='label+percent', textfont_size=10, )
        fig.update_layout(autosize=True, )
        st.plotly_chart(fig)

    st.subheader("Top 20 districts with highest crimes(sum of all crimes) happened against Women")
    st.write("Hint: Hover-over the bars to see all informations.")
    District_Total["Total"]=District_Total["Rape"]+ District_Total["Kidnapping and Abduction"] + District_Total["Dowry Deaths"]+District_Total["Insult to modesty of Women"]+District_Total["Cruelty by Husband or his Relatives"]+District_Total["Importation of Girls"]
    srt=District_Total.sort_values(by="Total",ascending=False)
    srt=srt.head(23).reset_index()
    srt.drop([0,6,7],axis=0,inplace=True)
    # srt.drop(7,axis=0,inplace=True)
    fig=px.bar(srt, x="DISTRICT",y="Total" ,
           color='State', text='Total', 
           title="",)
    fig.update_traces( textposition='outside')
    fig.update_layout(plot_bgcolor='white', width= 900)
    st.plotly_chart(fig)

    st.subheader("Top 10 States for different Crimes(Dropdown)")
    variables=["Top 10 States/UT with Highest number of Rapes",
    "Top 10 States/UT with Highest number of Cruelty by Husband or his Relatives",
    "Top 10 states with Highest number of Dowry Deaths",
    "Top 10 states with Highest number of Kidnapping and Abduction"]
    x = st.selectbox("Chose from Dropdown", variables)
    
    if x=="Top 10 States/UT with Highest number of Rapes":
        state_total_r=state_total.groupby("STATE/UT").sum().sort_values(by="Rape", ascending=False).head(10).reset_index()
        fig=go.Figure(data=[go.Bar(x=state_total_r['STATE/UT'],y=state_total_r["Rape"], marker={'color':state_total_r['Rape']})])
        fig.update_layout(title="Total number of Rape vs State/UT",xaxis_title="Name of State/UT", yaxis_title="Number of Rapes",
                        plot_bgcolor='white' )
        fig.data[0].marker.line.width = 3
        fig.data[0].marker.line.color = "black"
        st.plotly_chart(fig)
    elif x=="Top 10 States/UT with Highest number of Cruelty by Husband or his Relatives":
        total_data_c=state_total.groupby("STATE/UT").sum().sort_values(by="Cruelty by Husband or his Relatives", ascending=False).head(10)
        fig=go.Figure(data=[go.Bar(x=total_data_c.index,y=total_data_c["Cruelty by Husband or his Relatives"] ,marker={'color':label10}	)])
        fig.update_layout(title="Cruelty by Husband or his Relatives vs State/UT",
                        xaxis_title="Name of State/UT", yaxis_title="Cruelty by Husband or his Relatives" ,
                        plot_bgcolor='white' )
        fig.data[0].marker.line.width = 3
        fig.data[0].marker.line.color = "black"
        st.plotly_chart(fig)
    elif x=="Top 10 states with Highest number of Dowry Deaths":
        state_total_d=state_total.groupby("STATE/UT").sum().sort_values(by="Dowry Deaths", ascending=False).head(10)      
        fig=go.Figure(data=[go.Bar(x=state_total_d.index,y=state_total_d["Dowry Deaths"], marker={'color':label10}	)])
        fig.update_layout(title="Dowry Deaths vs State/UT",xaxis_title="Name of State/UT", yaxis_title="Dowry Deaths" ,
                                            plot_bgcolor='white' )
        fig.data[0].marker.line.width = 3
        fig.data[0].marker.line.color = "black"
        st.plotly_chart(fig)        
    elif x=="Top 10 states with Highest number of Kidnapping and Abduction":
        total_data_k=state_total.groupby("STATE/UT").sum().sort_values(by="Kidnapping and Abduction", ascending=False).head(10)
        fig=go.Figure(data=[go.Bar(x=total_data_k.index,y=total_data_k["Kidnapping and Abduction"] ,marker={'color':label10}	)])
        fig.update_layout(title="Kidnapping and Abduction vs State/UT",xaxis_title="Name of State/UT", yaxis_title="Kidnapping and Abduction" ,
                                            plot_bgcolor='white' )
        fig.data[0].marker.line.width = 3
        fig.data[0].marker.line.color = "black"
        st.plotly_chart(fig)        

    st.write("Madhya Pradesh had the highest number of rapes between 2001 to 2014, lets see top 20 districts from Madhya Pradesh with highest Rapes.")
    MP_data=data[data['STATE/UT']=="Madhya Pradesh"]
    MP_data_District=MP_data.groupby("DISTRICT").sum().sort_values(by="Rape", ascending=False).head(20)
    MP_data_District=pd.merge(MP_data_District,lit,on="DISTRICT", how="inner") # Adding Literacy of Madhya Pradesh's Districts
    MP_data_District=pd.merge(MP_data_District,c11p,on="DISTRICT", how="inner") # Adding Population of Madhya Pradesh's  Districts    

    fig=go.Figure(data=[go.Scatter(x=MP_data_District.DISTRICT,y=MP_data_District.Rape,
                                
                                mode='markers',
                                marker=dict(size=(MP_data_District.Rape/25), color=label20 ))])
    fig.update_layout(title="Top 20 Districts with Highest number of Rapes in Madhya Pradesh",xaxis_title="Name of Districts", yaxis_title="Number of Rapes" ,
                    plot_bgcolor='white' )
    fig.data[0].marker.line.width = 3
    fig.data[0].marker.line.color = "black"
    st.plotly_chart(fig)    

    st.subheader("Now We gonna find Districts (with State, Population and Literacy) those have the highest number of rapes in Entire India")    
    st.write("Hint: Hover-over the bars to see State, Population, Literacy and other infos." )
    val=st.slider("Slide to see top N Districts",5,20,15)
    District_Total__= data.groupby("DISTRICT").sum().sort_values(by="Rape", ascending=False).reset_index().head(val+2)
    District_Total__.drop(0,axis=0,inplace=True)

    #Lets add Population and Literacy to every individual District

    District_Total__=pd.merge(District_Total__,c11p, on = "DISTRICT", how="left")
    District_Total__=pd.merge(District_Total__,lit, on = "DISTRICT", how="left")
    District_Total__.drop(2, inplace=True)
    District_Total__.drop("Year", axis=1, inplace=True)

    #---------#
    
    District_Total= data.groupby("DISTRICT").sum().sort_values(by="Rape", ascending=False).reset_index().head(22)
    District_Total.drop(0,axis=0,inplace=True)
    District_Total=pd.merge(District_Total,c11p, on = "DISTRICT", how="left")
    District_Total=pd.merge(District_Total,lit, on = "DISTRICT", how="left")
    District_Total.drop(2, inplace=True)
    District_Total.drop("Year", axis=1, inplace=True)  



    fig= px.bar(District_Total__,x="DISTRICT",y=District_Total__["Rape"],
                                color=District_Total__["Rape"],
                                hover_data=["State","Population","Literacy"], 
                )
    fig.update_layout(
                    xaxis_title="Name of Districts",
                    yaxis_title="Number of Rapes" ,
                    plot_bgcolor='white', height= 600, width=700
                    )
    fig.data[0].marker.line.width = 3
    fig.data[0].marker.line.color = "black"
    st.plotly_chart(fig)

    st.subheader("Line graph for India's top Rape Reported district to see if there any relation between Rape and Literacy.")
    st.write("Values are normalized using MinMax method, you can read about MinMax normalization on the Internet")
    temp_District_Total=District_Total
    District_TotalMM = pd.DataFrame(scaler.fit_transform(District_Total[["Literacy","Population","Rape"]]), columns=["Literacy","Population","Rape"])
    District_TotalMM.set_index(District_Total.index, inplace = True)

    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=temp_District_Total.DISTRICT, y=District_TotalMM.Rape,
                        mode='lines+markers',
                        name='Rape',
                        hovertext="Rape"))

    fig.add_trace(go.Scatter(x=temp_District_Total.DISTRICT, y=District_TotalMM.Literacy,
                        mode='lines+markers',
                        name='Literacy'))

    # Edit the layout
    fig.update_layout(title='',
                    xaxis_title='Districts Name',
                    yaxis_title='Normalized values in between 0 and 1',
                    plot_bgcolor='white'
                    )
    st.plotly_chart(fig)

    st.subheader("Line graph for India's top Rape Reported district to see if there any relation between Rape and Population.")
    st.write("Values are normalized using MinMax method, you can read about MinMax normalization on the Internet")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=temp_District_Total.DISTRICT, y=District_TotalMM.Rape,
                        mode='lines',
                        name='Rape',
                        hovertext="Rape"))

    fig.add_trace(go.Scatter(x=temp_District_Total.DISTRICT, y=District_TotalMM.Population,
                        mode='lines',
                        name='Population'))

    # Edit the layout
    fig.update_layout(title='',
                    xaxis_title='Districts Name',
                    yaxis_title='Normalized values in between 0 and 1', plot_bgcolor='white',)
    st.plotly_chart(fig)

    st.subheader("3D Scatter Plot for top 20 Rape Reported District!")
    fig = px.scatter_3d(District_Total, x='Rape', y='Literacy', z='Population',
              color='DISTRICT', symbol="State", )
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)', height=600, width=900)                    
    st.plotly_chart(fig)


    st.write("Hi there, if you have come so far, it shows your love for exploring things,\
     this whole project is made using four open-source libraries pandas, numpy, \
         plotly and streamlit.")
    st.subheader("Via - Satyampd(Username for Github, Kaggle and LinkedIn)")
if __name__ == "__main__":
	app()