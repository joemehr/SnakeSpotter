package com.example.conor.snakespotter;

import android.icu.text.DateFormat;
import android.os.AsyncTask;
import android.os.Build;
import android.provider.MediaStore;
import android.support.annotation.RequiresApi;
import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.Date;

import okhttp3.FormBody;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import static android.R.attr.bitmap;
import static android.R.attr.data;
import static android.provider.ContactsContract.CommonDataKinds.Website.URL;

/**
 * Created by conor on 4/21/2017.
 */

class PostHandler extends AsyncTask<String, Void, String> {

    OkHttpClient client = new OkHttpClient();
    public static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");
    private AsyncResponse delegate = null;
    String bitmapString;
    String loc;
    String URL = "http://192.168.1.7:5000";

    public PostHandler() {
        Log.d("Upload Debug", "Entered PostHandler Constructor");
    }

    public void setBitmapString(String str) {
        bitmapString = str;
    }

    public void setLoc(String str) {
        loc = str;
    }

    public void setDelegate(AsyncResponse a) {
        this.delegate = a;
    }

    @RequiresApi(api = Build.VERSION_CODES.N)
    @Override
    protected String doInBackground(String... params) {

        Log.d("Upload Debug", "Entered doInBackground");

        String date = DateFormat.getDateTimeInstance().format(new Date());

        JSONObject jobj = new JSONObject();
        try {
            jobj.put("image", bitmapString);
            jobj.put("time", date);
            jobj.put("location", loc);
            jobj.put("species", "Unknown");
            jobj.put("observer", "Unknown");
        } catch (Exception e) {
            e.printStackTrace();
        }

        /**
        RequestBody formBody = new FormBody.Builder()
                .add("image", bitmapString)
                .add("time", date)
                .add("location", loc)
                .add("species", "Unknown")
                .add("observer", "Unknown")
                .build();
         */

        RequestBody body = RequestBody.create(JSON, jobj.toString());

        Request request = new Request.Builder()
                .url(URL+"/sighting/")
                .post(body)
                .header("Content-type", "application/json")
                .build();

        Log.d("Upload Debug", "Built Request");
        Log.d("Upload Debug", ""+URL+"/sighting/");
        try {

            Response response = client.newCall(request).execute();


            Log.d("Upload Debug", "Response Received");
            if (!response.isSuccessful()) {
                Log.d("Upload Debug", "Response was not successful");
                throw new IOException("Unexpected code " + response.toString());
            }
            Log.d("Upload Debug", "Response Successful");
            return response.body().string();
        } catch (IOException e) {
            Log.d("Upload Debug", "Caught Exception: "+e.toString());
            e.printStackTrace();
        }
        return null;
    }

    @Override
    protected void onPostExecute(String result) {
        delegate.processFinish(result);
    }
}
