package com.example.fetchjson;

import android.os.AsyncTask;
import android.util.Log;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class fetchData extends AsyncTask<Void,Void,Void> {
    String roll;
    String data;
    String url1;
    String line = "";
    static double per;
    double tot;
    double att;
    public static String fin;
    fetchData(String roll1){
        roll = roll1;
    Log.i("inside","inside cons");
    }
    @Override
    protected Void doInBackground(Void... voids) {
        try {
            url1 = "http://3.83.147.110/getattendence/";
            url1+= roll;
            Log.i("uuu",url1);
            URL url = new URL(url1);
            try{
                HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();
                InputStream inputStream = httpURLConnection.getInputStream();
                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
                line = bufferedReader.readLine();
                Log.i("data",line);

            }catch (Exception e){
                Log.i("Ex",e.toString());
            }
            JSONArray JA = new JSONArray(line);
            for(int i =0 ;i <JA.length(); i++){
                JSONObject JO = (JSONObject) JA.get(i);
                att =  Double.valueOf(JO.get("attended").toString());
                tot =  Double.valueOf(JO.get("total").toString());
                per = att/tot;
                per *=100;
                        //;att/tot;
                fin =  "Roll No: " + JO.get("roll").toString() + "\n"+
                        "Lectures attended: " + JO.get("attended").toString() + "\n"+
                        "Lectures Delivered: " + JO.get("total").toString() + "\n" +
                        "Your Attendance: " + per  +"%"+ "\n";
                Log.i("fin",fin);
            }

        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (JSONException e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    protected void onPostExecute(Void aVoid) {
        super.onPostExecute(aVoid);
        MainActivity.attended.setText(this.fin);
    }
}
