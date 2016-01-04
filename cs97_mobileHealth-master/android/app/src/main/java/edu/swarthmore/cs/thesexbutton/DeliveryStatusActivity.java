package edu.swarthmore.cs.thesexbutton;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.widget.TextView;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class DeliveryStatusActivity extends Activity
{
    private ProgressDialog mProgressDialog;
    private Handler mHandler = new Handler();  // used to queue code execution on thread
    private int mProgressDialogStatus;
    String mOrderNumber, mSessionToken;
    SharedPreferences mSharedPreferences;
    int mDeliveryEstimate;
    boolean mAccepted;
    boolean mDelivered;
    boolean mFailed;
    String status;

    /**
     * Disable back button
     */
    @Override
    public void onBackPressed() {
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_delivery_status);

        mSharedPreferences = getSharedPreferences("SharedPreferences", MODE_PRIVATE);
        mSessionToken = mSharedPreferences.getString("session_token", null);
        mOrderNumber = mSharedPreferences.getString("order_number", null);
        TextView orderNum = (TextView) findViewById(R.id.text_order_number_status);
        orderNum.setText("Order " + mOrderNumber);

        status = getIntent().getStringExtra("status");
        if (status != null) {
        // Means this activity was called by GCMIntentService
            if (status.equals("success")) {
                handleDeliveryComplete();
            } else if (status.equals("fail")) {
                handleDeliveryFail();
            }
        } else {
        // Means this activity was called by Request Condom Service
            new Thread(new Runnable() {
                @Override
                public void run() {
                    // Poll the server every 5 sec until order accepted or fails
                    while (!mAccepted && !mFailed) {
                        checkDeliveryStatus();
                        mySleep(5000);
                    }

                    // Check if failed or accepted
                    if (mFailed) {
                        handleDeliveryFail();
                    } else {
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                launchProgressDialog(DeliveryStatusActivity.this);
                            }
                        });
                    }
                }
            }).start();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        checkDeliveryStatus();

        if(mDelivered) {
            handleDeliveryComplete();
        } else if(mFailed) {
            handleDeliveryFail();
        }
    }

    /**
     * Shows user that the condoms have been delivered
     */
    public void handleDeliveryComplete()
    {
        try {
            mProgressDialog.dismiss();
        } catch(NullPointerException e) {
        }

        SharedPreferences.Editor edit = mSharedPreferences.edit();
        edit.putBoolean("order_failed", false);
        edit.commit();

        Intent i = new Intent(DeliveryStatusActivity.this, DeliveryCompleteActivity.class);
        startActivity(i);
        finish();
    }

    /**
     * Upon order fail, allow user to reorder condom
     */
    public void handleDeliveryFail()
    {
        try {
            mProgressDialog.dismiss();
        } catch(NullPointerException e) {
        }

        SharedPreferences.Editor edit = mSharedPreferences.edit();
        edit.putBoolean("order_failed", true);
        edit.putString("order_number", mOrderNumber);
        edit.commit();

        Intent i = new Intent(DeliveryStatusActivity.this, RequestCondomActivity.class);
        startActivity(i);
        finish();
    }

    /**
     * Launches and loads progress bar
     */
    public void launchProgressDialog(Context context) {
        // Prepare for a progress bar dialog
        mProgressDialog = new ProgressDialog(context);
        mProgressDialog.setProgressStyle(ProgressDialog.STYLE_HORIZONTAL);
        mProgressDialog.setTitle("Delivering Order " + mOrderNumber + "...");
        mProgressDialog.setMessage("Condoms are on their way!\nEstimated delivery time: " +
                mDeliveryEstimate + " min.");
        mProgressDialog.setCancelable(false);  // dialog can't be cancelled by pressing back
        mProgressDialog.setIndeterminate(false);
        mProgressDialog.setMax(mDeliveryEstimate);
        mProgressDialog.setProgress(0);  // set the current progress to zero
        mProgressDialog.show();

        mProgressDialogStatus = 0;
        Thread thread = new Thread(new Runnable() {  // used to execute in parallel with UI thread
            public void run() {
                int counter = 1;

                // Check delivery status every 10 seconds
                while(!mDelivered && !mFailed) {
                    checkDeliveryStatus();
                    if(mDelivered) {
                        mProgressDialogStatus = mProgressDialog.getMax();
                    } else { // if loading bar isn't full, update progress
                        if(mProgressDialogStatus < mProgressDialog.getMax() && counter%6 == 0) {
                            mHandler.post(new Runnable() {
                                public void run() {
                                    mProgressDialog.setProgress(mProgressDialogStatus);
                                }
                            });
                            mProgressDialogStatus++;
                        }
                        mySleep(10000);
                        counter++;
                    }
                }
                mProgressDialog.dismiss();

                // Determine failed or completed delivery
                if(mFailed) {
                    handleDeliveryFail();
                } else {
                    mySleep(1500);
                    handleDeliveryComplete();
                }
            }
        });
        thread.start();
    }

    /**
     * Thread.sleep wrapper
     */
    private void mySleep(int time) {
        try {
            Thread.sleep(time);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    /**
     * Hits our server to determine delivery status of order
     */
    public void checkDeliveryStatus()
    {
        List<NameValuePair> params = new ArrayList<NameValuePair>();
        params.add(new BasicNameValuePair("session_token", mSessionToken));
        params.add(new BasicNameValuePair("order_number", mOrderNumber));

        ServerRequest serverRequest = new ServerRequest(getApplicationContext());
        JSONObject json = serverRequest.getJSON("https://tsb.sccs.swarthmore.edu:8443/api/delivery/status", params);

        if(json != null) {
            try {
                mAccepted = json.getBoolean("order_accepted");
                mDelivered = json.getBoolean("order_delivered");
                mFailed = json.getBoolean("order_failed");
                mDeliveryEstimate = json.getInt("delivery_estimate");

                if(mDeliveryEstimate == -1) {
                    mDeliveryEstimate = 15;
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }
}