package edu.swarthmore.cs.thesexbutton;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class RegisterActivity extends Activity {
    EditText mSignupToken;
    Button mRegister;
    String mSignupTokenString, mDeviceUUID, mDeviceOS, mPassphrase, mRegid;
    List<NameValuePair> mParams;
    SharedPreferences mSharedPreferences;
    private static String TAG = "RegisterActivity";

    /**
     * Disable back button
     */
    @Override
    public void onBackPressed() {
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        Log.i(TAG, "onCreate");

        mSignupToken = (EditText)findViewById(R.id.signupToken);
        mRegister = (Button)findViewById(R.id.registerButton);

        mSharedPreferences = getSharedPreferences("SharedPreferences", MODE_PRIVATE);

        mRegister.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mSignupTokenString = mSignupToken.getText().toString();
                mDeviceOS = "ANDROID_OS";
                mPassphrase = UUID.randomUUID().toString();
                mDeviceUUID = UUID.randomUUID().toString();

                //TODO
                /*mDeviceUUID = Secure.getString(getContentResolver(), Secure.ANDROID_ID);
                if(mDeviceUUID == null) {
                    mDeviceUUID = UUID.randomUUID().toString();
                }*/
                mRegid = getIntent().getStringExtra("push_id");

                mParams = new ArrayList<NameValuePair>();
                mParams.add(new BasicNameValuePair("signup_token", mSignupTokenString));
                mParams.add(new BasicNameValuePair("device_uuid", mDeviceUUID));
                mParams.add(new BasicNameValuePair("device_os", mDeviceOS));
                mParams.add(new BasicNameValuePair("passphrase", mPassphrase));
                mParams.add(new BasicNameValuePair("push_id", mRegid));

                ServerRequest serverRequest = new ServerRequest(getApplicationContext());
                JSONObject json = serverRequest.getJSON("https://tsb.sccs.swarthmore.edu:8443/api/register", mParams);

                if (json != null) {
                    try {
                        String jsonString = json.getString("response");
                        String sessionToken = json.getString("session_token");
                        String sessionTokenExpires = json.getString("session_token_expires");

                        SharedPreferences.Editor edit = mSharedPreferences.edit();
                        edit.putString("session_token", sessionToken);
                        edit.putString("session_token_expires", sessionTokenExpires);
                        edit.putString("device_uuid", mDeviceUUID);
                        edit.putString("passphrase", mPassphrase);
                        edit.commit();

                        // switch to Request Condom Activity
                        Intent i = new Intent(RegisterActivity.this, RequestCondomActivity.class);
                        startActivity(i);

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            }
        });
    }
}