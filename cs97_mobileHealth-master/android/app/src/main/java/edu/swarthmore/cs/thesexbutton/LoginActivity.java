package edu.swarthmore.cs.thesexbutton;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.StrictMode;
import android.util.Log;
import android.widget.Toast;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GooglePlayServicesUtil;
import com.google.android.gms.gcm.GoogleCloudMessaging;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class LoginActivity extends Activity {
    String mSessionToken, mSessionTokenExpires, mDeviceUUID, mPassphrase, mOrderNumber;
    SharedPreferences mSharedPreferences;
    Boolean mHasPlayServices;

    // GCM vars
    public static final String PROPERTY_REG_ID = "registration_id";
    private static final String PROPERTY_APP_VERSION = "appVersion";
    private final static int PLAY_SERVICES_RESOLUTION_REQUEST = 9000;
    private static String TAG = "LoginActivity";
    String SENDER_ID = "764780160177";  // GCM project number
    GoogleCloudMessaging gcm;
    //AtomicInteger msgId = new AtomicInteger();
    SharedPreferences prefs;
    Context context;
    String mRegid;

    /**
     * Disable back button
     */
    @Override
    public void onBackPressed() {
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        Log.i(TAG, "onCreate");

        context = getApplicationContext();
        gcm = GoogleCloudMessaging.getInstance(this);

        // Allow networking in the main thread
        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        new Thread(new Runnable() {
            @Override
            public void run() {
            try {  // sleep 1.5 seconds
                Thread.sleep(1500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    // Make sure device has internet connectivity
                    if (!checkInternet()) {
                        Log.i(TAG, "No internet connection!");
                        Toast.makeText(context, "Please connect to the internet.", Toast.LENGTH_LONG).show();
                    }

                    // Make sure device has Play Services APK and register for GCM
                    if (checkPlayServices()) {
                        mRegid = getRegistrationId(context);
                        if (mRegid.isEmpty()) {
                            registerInBackground();
                            mHasPlayServices = true;
                        } else {
                            Log.i(TAG, "Prev gcm regid found: " + mRegid);
                            mHasPlayServices = true;
                        }
                    } else {
                        Log.i(TAG, "No valid Google Play Services APK found.");
                        mHasPlayServices = false;
                    }

                    Log.i(TAG, "Play services status: " + mHasPlayServices);

                    if (mHasPlayServices) {
                        // Retrieve from previous registration
                        mSharedPreferences = getSharedPreferences("SharedPreferences", MODE_PRIVATE);
                        mSessionToken = mSharedPreferences.getString("session_token", null);
                        mSessionTokenExpires = mSharedPreferences.getString("session_token_expires", null);
                        mDeviceUUID = mSharedPreferences.getString("device_uuid", null);
                        mPassphrase = mSharedPreferences.getString("passphrase", null);
                        mOrderNumber = mSharedPreferences.getString("order_number", null);

                        Log.i(TAG, "onCreate: " + mSessionToken + " " + mOrderNumber + " " + mDeviceUUID);

                        if (mSessionToken == null) {
                            if (mDeviceUUID == null) {
                                // New user; call Register Activity
                                Log.i(TAG, "starting Register Activity");
                                Intent i = new Intent(LoginActivity.this, RegisterActivity.class);
                                i.putExtra("push_id", mRegid);
                                startActivity(i);
                                finish();
                            }
                        } else {
                            Log.i(TAG, "logging in");
                            Login(mDeviceUUID, mPassphrase, mRegid); // also handles request and status
                        }
                    }
                }
            });
            }
        }).start();
    }

    @Override
    public void onResume() {
        super.onResume();
        Log.i(TAG, "onResume");
    }

    /**
     * Requests login to our server, sending deviceID, passphrase, and gcm regid.
     * Server sends back an authorization token that is stored in sharedPreferences.
     */
    public void Login(String deviceUUID, String passphrase, String regid) {
        Log.i(TAG, "Login " + deviceUUID);
        List<NameValuePair> params = new ArrayList<NameValuePair>();
        params.add(new BasicNameValuePair("device_uuid", deviceUUID));
        params.add(new BasicNameValuePair("passphrase", passphrase));
        params.add(new BasicNameValuePair("push_id", regid));

        ServerRequest serverRequest = new ServerRequest(getApplicationContext());
        JSONObject json = serverRequest.getJSON("https://tsb.sccs.swarthmore.edu:8443/api/login", params);

        if (json != null) {
            try {
                mSessionToken = json.getString("session_token");
                //mSessionTokenExpires = json.getString("session_token_expires");

                SharedPreferences.Editor edit = mSharedPreferences.edit();
                edit.putString("session_token", mSessionToken);
                //edit.putString("session_token_expires", mSessionTokenExpires);
                edit.commit();
                Log.i(TAG, "Obtained session token: " + mSessionToken);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

        // Check if user has an open order
        if(mOrderNumber != null) {
            if (CheckOrderStatus(mSessionToken, mOrderNumber)) {
                Intent i = new Intent(LoginActivity.this, DeliveryStatusActivity.class);
                startActivity(i);
                finish();
            }
        }

        // If no open order, go to request condom activity
        Log.i(TAG, "starting Request Condom Activity");
        Intent i = new Intent(LoginActivity.this, RequestCondomActivity.class);
        startActivity(i);
        finish();
    }

    public boolean CheckOrderStatus(String sessionToken, String orderNumber) {
        Log.d(TAG, "CheckOrderStatus: " + orderNumber + " for " + sessionToken);
        boolean delivered = false;
        //boolean failed = false;

        List<NameValuePair> params = new ArrayList<NameValuePair>();
        params.add(new BasicNameValuePair("session_token", sessionToken));
        params.add(new BasicNameValuePair("order_number", orderNumber));

        ServerRequest serverRequest = new ServerRequest(getApplicationContext());
        JSONObject json = serverRequest.getJSON("https://tsb.sccs.swarthmore.edu:8443/api/delivery/status", params);

        if (json != null) {
            try {
                delivered = json.getBoolean("order_delivered");
                //failed = json.getBoolean("order_failed");
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

        return !delivered;
    }

    /**
     * Check the device's connectivity status.
     */
    private boolean checkInternet() {
        ConnectivityManager cm =
                (ConnectivityManager)context.getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
        return (activeNetwork != null && activeNetwork.isConnected());
    }

    /**
     * Check the device to make sure it has the Google Play Services APK. If it doesn't, display a
     * dialog that allows users to enable it or download it from the Play Store.
     */
    private boolean checkPlayServices() {
        int resultCode = GooglePlayServicesUtil.isGooglePlayServicesAvailable(this);
        if (resultCode != ConnectionResult.SUCCESS) {
            if (GooglePlayServicesUtil.isUserRecoverableError(resultCode)) {
                GooglePlayServicesUtil.getErrorDialog(resultCode, this,
                        PLAY_SERVICES_RESOLUTION_REQUEST).show();
            } else {
                Log.i(TAG, "This device is not supported.");
                finish();
            }
            return false;
        }
        return true;
    }

    /**
     * Gets the current registration ID for application on GCM service.
     * If result is empty, the app needs to register.
     */
    private String getRegistrationId(Context context) {
        prefs = getGCMPreferences();
        String registrationId = prefs.getString(PROPERTY_REG_ID, "");
        if (registrationId.isEmpty()) {
            Log.i(TAG, "Registration not found.");
            return "";
        }

        // If app was updated, it must clear the registration ID since the existing regID
        // is not guaranteed to work with the new app version
        int registeredVersion = prefs.getInt(PROPERTY_APP_VERSION, Integer.MIN_VALUE);
        int currentVersion = getAppVersion(context);
        if (registeredVersion != currentVersion) {
            Log.i(TAG, "App version changed.");
            return "";
        }

        return registrationId;
    }

    /**
     * return Application's sharedPreferences.
     */
    private SharedPreferences getGCMPreferences() {
        return getSharedPreferences(RequestCondomActivity.class.getSimpleName(),
                Context.MODE_PRIVATE);
    }

    /**
     * return Application's version code from the PackageManager.
     */
    private static int getAppVersion(Context context) {
        try {
            PackageInfo packageInfo = context.getPackageManager()
                    .getPackageInfo(context.getPackageName(), 0);
            return packageInfo.versionCode;
        } catch (PackageManager.NameNotFoundException e) {
            throw new RuntimeException("Could not get package name: " + e);  // should never happen
        }
    }

    /**
     * Registers the application with GCM servers asynchronously.
     * Stores the registration ID and app versionCode in the application's shared preferences.
     */
    private void registerInBackground() {
        new AsyncTask<Void, Void, String>() {
            @Override
            protected String doInBackground(Void... params) {
                String msg;
                try {
                    if (gcm == null) {
                        gcm = GoogleCloudMessaging.getInstance(context);
                    }
                    mRegid = gcm.register(SENDER_ID);
                    msg = "Device registered; regid=" + mRegid;
                    storeRegistrationId(context, mRegid);  // persist the regID
                } catch (IOException ex) {
                    msg = "Error :" + ex.getMessage();
                    // If there is an error, don't just keep trying to register.
                    // Require the user to click a button again, or perform
                    // exponential back-off.
                    finish();
                }
                Log.i(TAG, msg);
                return msg;
            }
        }.execute(null, null, null);
    }

    /**
     * Stores the registration ID and app versionCode in the application's
     * SharedPreferences
     */
    private void storeRegistrationId(Context context, String regId) {
        prefs = getGCMPreferences();
        int appVersion = getAppVersion(context);
        Log.i(TAG, "Saving regId on app version " + appVersion);
        SharedPreferences.Editor editor = prefs.edit();
        editor.putString(PROPERTY_REG_ID, regId);
        editor.putInt(PROPERTY_APP_VERSION, appVersion);
        editor.commit();
    }
}