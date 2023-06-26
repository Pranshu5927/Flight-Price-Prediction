from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
from sklearn import preprocessing
import sys
# from __future__ import print_function
app = Flask(__name__)
rf = pickle.load(open("reg_rf_final.pkl", "rb"))
df=pickle.load(open("dataframe", "rb"))
# lst=[['Vistara','UK','963','08:50','Delhi','02h 20m','11:10','Mumbai','Economy','0']]
def prediction2(lst):
    df_test = pd.DataFrame(lst,columns =['AIRLINE', 'CH_CODE','NUM_CODE','DEP_TIME', 'FROM', 'TIME_TAKEN', 'ARR_TIME','TO','CLASS','NUMBER_OF_STOPS'])
    df_test
    import pickle
    dbfile = open('dataframe', 'rb')     
    df_back_final = pickle.load(dbfile)
    df_back_final=pd.DataFrame(df_back_final)
    df_back_final_user=pd.concat([df_back_final,df_test])
    df_back_final_user
    df_back_final_user=df_back_final_user.drop(columns=['PRICE'])
    # label_encoder object knows 
    # ho/w to understand word labels.
    label_encoder = preprocessing.LabelEncoder()
    # Encode labels in column 'species'.
    categorical_columns = df.select_dtypes(include=['object']).columns
    for column in categorical_columns:
        df_back_final_user[column]= label_encoder.fit_transform(df_back_final_user[column])
    df_test_final=df_back_final_user.tail(1)
    df_test_final
    y_pred_rf = rf.predict(df_test_final)
    return y_pred_rf
    


@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/prediction")
@cross_origin()
def prediction():
    return render_template("prediction.html")

@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        #  date_dep = request.form["Dep_Time"]
        #  Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        #  Journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
         # print("Journey Date : ",Journey_day, Journey_month)

        #  
        # # Departure
        # date_dep = request.form["Dep_Time"]
        # dep_datetime = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M")
        # dep_hour = dep_datetime.hour
        # dep_min = dep_datetime.minute
        # dep_time = f"{dep_hour:02d}:{dep_min:02d}"

        # # Arrival
        # date_arr = request.form["Arrival_Time"]
        # arr_datetime = pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M")
        # arr_hour = arr_datetime.hour
        # arr_min = arr_datetime.minute
        # arr_time = f"{arr_hour:02d}:{arr_min:02d}"

        # # Duration
        # dur_hour = abs(arr_hour - dep_hour)
        # dur_min = abs(arr_min - dep_min)
        # dur_time = f"{dur_hour}h {dur_min}m"
        # Departure
        date_dep = request.form["Dep_Time"]
        dep_datetime = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M")
        dep_time = dep_datetime.strftime("%H:%M")

        # Arrival
        date_arr = request.form["Arrival_Time"]
        arr_datetime = pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M")
        arr_time = arr_datetime.strftime("%H:%M")

        # Duration
        duration = (arr_datetime - dep_datetime).total_seconds() // 60
        dur_hours = int(duration // 60)
        if(dur_hours<10):
            dur_hours = "0"+str(dur_hours)
            # dur_hours=int(dur_hours)
        dur_minutes = int(duration % 60)
        dur_time = f"{dur_hours}h {dur_minutes}m"
         # Total Stops
        Total_stops = request.form["stops"]
         # print(Total_stops)
         
         # Airline
        Airline = request.form["airline"]
         
          # Source
        
        Source = request.form["Source"]
         # Destination
        
        Destination = request.form["Destination"]
         # Class
        
        Class = request.form["class"]
         # Class
        
        Ch_code = request.form["ch_code"]
         # Class
        
        num_code = request.form["num_code"]
        lst1=[[Airline,Ch_code,num_code,dep_time,Source,dur_time,arr_time,Destination,Class,Total_stops]]
        print(lst1,file=sys.stderr)
        output=round(prediction2(lst1)[0],2)
        return render_template('prediction.html',prediction_text="Your Flight price is Rs. {}".format(output))
    return render_template("prediction.html")


if __name__ == "__main__":
    app.run(debug=True)