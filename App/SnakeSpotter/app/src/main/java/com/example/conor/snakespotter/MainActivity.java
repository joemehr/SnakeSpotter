package com.example.conor.snakespotter;

import android.Manifest;
import android.content.Intent;
import android.graphics.Bitmap;
import android.location.Location;
import android.provider.MediaStore;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

import static android.R.attr.data;

/**
 * MainActivity, opens when the app starts.
 * Makes use of Location Services through a GPSManager to inform the user of
 * their current Longitude and Latitude.
 * Starts Image Capture using Phone's Front-Facing Camera.
 * Packages Image Captured into JSON Object which it sends to a Server
 * connected to a Machine-Learning AI.
 * On return from Server, parses JSON which contains the name of a snake
 * species that the image resembles.
 */
public class MainActivity extends AppCompatActivity implements AsyncResponse {

    GPSManager gpsManager;
    PostHandler ph;
    TextView latitude;
    TextView longitude;
    TextView sV;
    EditText eT;
    ImageView iv;
    Button pB;
    Button gB;
    Button uB;
    int requestCode = 0;
    Bitmap bm;
    Location loc;
    boolean imageSet;

    String URL = "http://192.168.1.7:5000";
    String species;
    OkHttpClient client;

    /**
     * Lifecycle Event.
     * When the app boots, the following code runs.
     * This app connects the Activity to UI elements, sets onClickListeners
     * for Buttons, sets default text for TextViews, and initializes a
     * GPSManager to utilize LocationServices.
     * @param savedInstanceState
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        imageSet = false;

        iv = (ImageView) findViewById(R.id.imageView);
        pB = (Button)findViewById(R.id.photoButton);
        gB = (Button)findViewById(R.id.getButton);
        uB = (Button)findViewById(R.id.uploadButton);
        sV = (TextView)findViewById(R.id.speciesView);
        eT = (EditText)findViewById(R.id.editText);
        pB.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                startActivityForResult(intent, 0);
            }
        });
        gB.setOnClickListener(new View.OnClickListener() {

            /**
             * OnClickListener for the UploadButton.  Assembles an HTTPPost
             * request with a JSONObject in its body.
             * @param v
             */
            @Override
            public void onClick(View v) {

                client = new OkHttpClient();
                String snakeName = eT.getText().toString();
                Log.d("onClick Debug", snakeName);

                final Request request = new Request.Builder()
                        .url(URL + "/snake/" + snakeName).build();
                Log.d("onClick Debug", "built request");
                Log.d("onClick Debug", URL+"/snake/"+snakeName);

                client.newCall(request).enqueue(new Callback() {
                    @Override
                    public void onFailure(Call call, IOException e) {
                        Log.d("onClick Debug", "onFailure");
                        e.printStackTrace();
                    }

                    @Override
                    public void onResponse(Call call, final Response response) throws IOException {
                        Log.d("onClick Debug", "onResponse");
                        if (!response.isSuccessful()) {
                            Log.d("onClick Debug", "Response Is Not Successful");
                            throw new IOException("Unexpected code " + response);
                        } else {
                            Log.d("onClick Debug", "Response Is Successful");
                            final String responseData = response.body().string();
                            //Log.d(TAG, responseData);

                            // Run view-related code back on the main thread
                            MainActivity.this.runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    sV.setText(responseData);
                                }
                            });
                        }
                    }
                });
            }
        });

        uB.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                if (imageSet) {
                    Log.d("Upload Debug", "in onClick");
                    String bitmapString = bitMapToString(bm);
                    String locString = ""+latitude+", "+latitude;
                    ph.setBitmapString(bitmapString);
                    ph.setLoc(locString);
                    ph.execute();
                }
            }
        });

        latitude = (TextView)findViewById(R.id.latitude);
        longitude = (TextView)findViewById(R.id.longitude);
        loc = null;
        gpsManager = new GPSManager(this);
        ph = new PostHandler();
        ph.setDelegate(this);
    }

    private String bitMapToString(Bitmap bm) {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bm.compress(Bitmap.CompressFormat.JPEG, 100, baos);
        byte[] b = baos.toByteArray();
        String temp = Base64.encodeToString(b, Base64.DEFAULT);
        Log.d("bitmap debug", temp);
        return temp;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        bm = (Bitmap) data.getExtras().get("data");
        imageSet = true;
        iv.setImageBitmap(bm);

    }

    @Override
    protected void onStart() {
        super.onStart();
        ActivityCompat.requestPermissions(this, new String[]{
                Manifest.permission.ACCESS_COARSE_LOCATION,
                Manifest.permission.ACCESS_FINE_LOCATION}, requestCode);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        gpsManager.register();

    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        gpsManager.unregister();
    }

    public void updateGPSLocation(Location location) {
        this.loc = location;
        if (latitude!=null) {
            latitude.setText("Latitude: "+location.getLatitude());
        }
        if (longitude!=null) {
            longitude.setText("Longitude: "+location.getLongitude());
        }
    }

    String run (String url) throws IOException {
        Request request = new Request.Builder()
                .url(url)
                .build();

        Log.d("onClick Debug", "request built");

        try (Response response = client.newCall(request).execute()) {
            Log.d("onClick Debug", "calling response.execute()");
            return response.body().string();
        }
        catch (Exception ex) {
            Log.d("onClick Debug", "caught excpetion");
            Log.d("onClick Debug", ex.toString());
            return null;
        }
    }

    @Override
    public void processFinish(String output) {
        sV.setText(output);
    }
}
