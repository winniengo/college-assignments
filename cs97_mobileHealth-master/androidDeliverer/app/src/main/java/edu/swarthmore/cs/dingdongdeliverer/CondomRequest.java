package edu.swarthmore.cs.dingdongdeliverer;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by wngo1 on 12/1/14.
 */
public class CondomRequest { // constructor
    private String mOrderNumber;
    private String mDeliveryDestination;

    private boolean mOrderAccepted;
    private boolean mOrderDelivered;
    private boolean mOrderFailed;

    private String mDateRequested;
    private String mDateAccepted;
    private String mDateDelivered;

    private int mDeliveryEstimate;

    public CondomRequest(JSONObject json) throws JSONException {
        mOrderNumber = json.getString("order_number");
        mOrderAccepted = json.getBoolean("order_accepted");
        mOrderDelivered = json.getBoolean("order_delivered");
        mOrderFailed = json.getBoolean("order_failed");

        mDateRequested = json.getString("date_requested");
        mDateAccepted = json.getString("date_accepted");
        mDateDelivered = json.getString("date_delivered");

        mDeliveryEstimate = json.getInt("delivery_estimate");

        // parse destination object into string
        JSONObject des = json.getJSONObject("delivery_destination");
        mDeliveryDestination = des.getString("dorm_name") +
                " - " + des.getString("delivery_type") +
                " - " + des.getString("dorm_room");

        Log.i("CondomRequest", "" + mOrderNumber + mDeliveryDestination + mOrderAccepted + mOrderDelivered);

    }

    public String getOrderNumber() {
        return mOrderNumber;
    }

    public void setOrderNumber(String orderNumber) {
        mOrderNumber = orderNumber;
    }

    public String getDeliveryDestination() {
        return mDeliveryDestination;
    }

    public void setDeliveryDestination(String deliveryDestination) {
        mDeliveryDestination = deliveryDestination;
    }

    public boolean isOrderAccepted() {
        return mOrderAccepted;
    }

    public void setOrderAccepted(boolean orderAccepted) {
        mOrderAccepted = orderAccepted;
    }

    public boolean isOrderDelivered() {
        return mOrderDelivered;
    }

    public void setOrderDelivered(boolean orderDelivered) {
        mOrderDelivered = orderDelivered;
    }

    public boolean isOrderFailed() {
        return mOrderFailed;
    }

    public void setOrderFailed(boolean orderFailed) {
        mOrderFailed = orderFailed;
    }

    public String getDateRequested() {
        return mDateRequested;
    }

    public void setDateRequested(String dateRequested) {
        mDateRequested = dateRequested;
    }

    public String getDateAccepted() {
        return mDateAccepted;
    }

    public void setDateAccepted(String dateAccepted) {
        mDateAccepted = dateAccepted;
    }

    public String getDateDelivered() {
        return mDateDelivered;
    }

    public void setDateDelivered(String dateDelivered) {
        mDateDelivered = dateDelivered;
    }

    public int getDeliveryEstimate() {
        return mDeliveryEstimate;
    }

    public void setDeliveryEstimate(int deliveryEstimate) {
        mDeliveryEstimate = deliveryEstimate;
    }
}
