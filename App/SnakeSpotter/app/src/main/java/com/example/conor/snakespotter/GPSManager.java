package com.example.conor.snakespotter;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;

import com.example.conor.snakespotter.MainActivity;

/**
 * Created by conor on 4/20/2017.
 */

public class GPSManager implements LocationListener {
    MainActivity mainActivity;
    LocationManager locationManager;
    String LOCATION_PROVIDER = LocationManager.GPS_PROVIDER;

    public GPSManager(MainActivity mainActivity) {
        this.mainActivity = mainActivity;
        locationManager = (LocationManager) mainActivity.getSystemService(Context.LOCATION_SERVICE);
    }

    public void register() {
        if((ActivityCompat.checkSelfPermission(mainActivity, Manifest.permission.ACCESS_COARSE_LOCATION)
                == PackageManager.PERMISSION_GRANTED)
                &&
                (ActivityCompat.checkSelfPermission(mainActivity, Manifest.permission.ACCESS_FINE_LOCATION)
                        == PackageManager.PERMISSION_GRANTED)) {
            locationManager.requestLocationUpdates(LOCATION_PROVIDER, 5000, 0, this);
            mainActivity.updateGPSLocation(locationManager.getLastKnownLocation(LOCATION_PROVIDER));
        }

    }

    public void unregister() {
        if((ActivityCompat.checkSelfPermission(mainActivity, Manifest.permission.ACCESS_COARSE_LOCATION)
                == PackageManager.PERMISSION_GRANTED)
                &&
                (ActivityCompat.checkSelfPermission(mainActivity, Manifest.permission.ACCESS_FINE_LOCATION)
                        == PackageManager.PERMISSION_GRANTED)) {
            locationManager.removeUpdates(this);
        }
    }

    @Override
    public void onLocationChanged(Location location) {
        mainActivity.updateGPSLocation(location);
    }

    @Override
    public void onStatusChanged(String provider, int status, Bundle extras) {

    }

    @Override
    public void onProviderEnabled(String provider) {

    }

    @Override
    public void onProviderDisabled(String provider) {

    }
}
