package edu.swarthmore.cs.thesexbutton;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.StrictMode;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class RequestCondomActivity extends Activity implements AdapterView.OnItemSelectedListener
{
    String mSessionToken = null;
    String mDormName = null;
    String mDeliveryType = null;
    EditText mDormNumber;
    String mDormNumberString = null;
    boolean mDeliveryTypeFilled = false;
    boolean mDormFilled = false;
    boolean mDeliveryFailed = false;
    Button mRequestButton;
    List<NameValuePair> mParams;
    SharedPreferences mSharedPreferences;
    private static String TAG = "RequestCondomActivity";
    Boolean mOpenForBusiness;
    int requestButtonCounter = 0;

    /**
     * Disable back button
     */
    @Override
    public void onBackPressed() {
    }

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_request_condom);

        Log.i(TAG, "onCreate");

        mSharedPreferences = getSharedPreferences("SharedPreferences", MODE_PRIVATE);
        mSessionToken = mSharedPreferences.getString("session_token", null);
        mDeliveryFailed = mSharedPreferences.getBoolean("order_failed", false);

        if(mDeliveryFailed) { // if previous ordered failed, change display texts
            TextView failedBlurb = (TextView)findViewById(R.id.request_condom_text);
            TextView failedBlurb2 = (TextView)findViewById(R.id.request_condom_text_details);
            failedBlurb.setText("Oops! Your order couldn't be completed.\nPlease try again!");
            failedBlurb.setBackgroundColor(getResources().getColor(R.color.red));
            failedBlurb2.setText(R.string.request_condom_text);

            // Clear out failure data
            SharedPreferences.Editor edit = mSharedPreferences.edit();
            edit.putBoolean("order_failed", false);
            edit.putString("order_number", "");
            edit.commit();
        }

        // Allow networking in the main thread
        if (android.os.Build.VERSION.SDK_INT > 9)
        {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        // Generate dorm name spinner
        Spinner spinner = (Spinner) findViewById(R.id.dorms_spinner);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
                R.array.dorms_array, android.R.layout.simple_spinner_dropdown_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner.setAdapter(adapter);
        spinner.setOnItemSelectedListener(this);

        // Dorm number field
        mDormNumber = (EditText)findViewById(R.id.dorm_number);
        mDormNumber.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
                // do nothing
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                mDormNumberString = s.toString();
                if (s.length() > 0) {
                    mDormFilled = true;
                }
                enableButton();
            }

            @Override
            public void afterTextChanged(Editable s) {
                if (s.length() <= 0) {
                    mDormFilled = false;
                }
                enableButton();
            }
        });

        // set the open for business text
        TextView openForBusinessText = (TextView) findViewById(R.id.open_for_business);
        setOpenForBusiness(openForBusinessText);

        mRequestButton = (Button) findViewById(R.id.request_condom_button);
        mRequestButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (requestButtonCounter == 0) {
                    Toast.makeText(getApplication(), "Are you sure? You only get 1 request per night.", Toast.LENGTH_LONG).show();
                    requestButtonCounter = 1;
                } else {
                    mRequestButton.setEnabled(false);

                    mParams = new ArrayList<NameValuePair>();
                    mParams.add(new BasicNameValuePair("session_token", mSessionToken));
                    mParams.add(new BasicNameValuePair("dorm_name", mDormName));
                    mParams.add(new BasicNameValuePair("dorm_room", mDormNumberString));
                    mParams.add(new BasicNameValuePair("delivery_type", mDeliveryType));

                    ServerRequest serverRequest = new ServerRequest(getApplicationContext());
                    JSONObject json = serverRequest.getJSON("https://tsb.sccs.swarthmore.edu:8443/api/delivery/request", mParams);
                    Log.i("RequestCondomActivity", mSessionToken + mDormName + mDormNumberString + mDeliveryType);
                    if (json != null) {
                        try {
                            String jsonString = json.getString("response");
                            String orderNumber = "";
                            try {
                                orderNumber = json.getString("order_number");
                            } catch (Exception e) {
                            }

                            // Check for rate limit
                            if(jsonString.equals("DELIVERY_REQUEST_ERROR_TOO_MANY_REQUESTS")) {
                                Toast.makeText(getApplication(), "Sorry! You've already reached your limit for tonight.", Toast.LENGTH_LONG).show();
                                mRequestButton.setEnabled(true);
                            } else {
                                // save current order details
                                SharedPreferences.Editor edit = mSharedPreferences.edit();
                                edit.putString("order_number", orderNumber);
                                edit.commit();

                                // call Delivery Status Activity
                                Intent i = new Intent(RequestCondomActivity.this, DeliveryStatusActivity.class);
                                startActivity(i);
                                finish();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                }
            }
        });
    }

    // Set open for business text
    public void setOpenForBusiness (TextView openForBusiness)
    {
        ServerRequest serverRequest = new ServerRequest(getApplicationContext());
        ArrayList<NameValuePair> reqParams = new ArrayList<NameValuePair>();
        reqParams.add(new BasicNameValuePair("session_token", mSessionToken));
        JSONObject response = serverRequest.getJSON("https://tsb.sccs.swarthmore.edu:8443/api/broadcast/announcement/get", reqParams);
        if (response != null) {
            try {
                String open = response.getString("open_for_business");
                openForBusiness.setText(response.getString("message"));
                if (open.equals("yes")) {
                    mOpenForBusiness = true;
                } else {
                    mOpenForBusiness = false;
                }
            } catch (JSONException e) {
                e.printStackTrace();
                //mOpenForBusiness = false;
            }
            Log.i(TAG, "mOpenForBusiness : "+mOpenForBusiness.toString());
        }
    }

    // Radio Button method
    public void onRadioButtonClicked(View view)
    {
        mDeliveryTypeFilled = ((RadioButton) view).isChecked();

        // Check which radio button was clicked
        switch(view.getId()) {
            case R.id.request_condom_delivery_type_radio_to_lounge:
                if (mDeliveryTypeFilled)
                    mDeliveryType = "Lounge";
                break;
            case R.id.request_condom_delivery_type_radio_to_room:
                if (mDeliveryTypeFilled)
                    mDeliveryType = "Room";
                break;
        }

        enableButton();
    }

    /**
     * Button enable method. Only enable orders when app is open and proper fields are filled
     */
    public void enableButton()
    {
        if (mDeliveryTypeFilled && mDormFilled && mOpenForBusiness) {
            mRequestButton.setEnabled(true);
            mRequestButton.setBackgroundResource(R.drawable.btn_green);
        } else {
            mRequestButton.setEnabled(false);
            mRequestButton.setBackgroundResource(R.drawable.btn_grey);
        }
    }

    // Spinner methods
    public void onItemSelected(AdapterView<?> parent, View view, int pos, long id)
    {
        mDormName = (String) parent.getItemAtPosition(pos);
    }

    public void onNothingSelected(AdapterView<?> parent)
    {
        mDormName = null;
    }

    // Menu methods
    @Override
    public boolean onCreateOptionsMenu(Menu menu)
    {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.request_condom_menu, menu);
        return true;
    }


    @Override
    public boolean onOptionsItemSelected(MenuItem item)
    {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        switch (item.getItemId()) {
            case R.id.menu_guide:
                startActivity(new Intent(RequestCondomActivity.this, MenuGuideActivity.class));
                return true;
            case R.id.menu_our_service:
                startActivity(new Intent(RequestCondomActivity.this, MenuServiceActivity.class));
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

    @Override
    protected void onResume()
    {
        super.onResume();
        // once you resume, check if we're still delivering
        TextView openForBusinessText = (TextView) findViewById(R.id.open_for_business);
        setOpenForBusiness(openForBusinessText);
    }
}
