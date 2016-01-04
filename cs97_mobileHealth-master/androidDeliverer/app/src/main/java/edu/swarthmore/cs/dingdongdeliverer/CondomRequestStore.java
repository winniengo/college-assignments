package edu.swarthmore.cs.dingdongdeliverer;

import android.util.Log;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by wngo1 on 12/1/14.
 */
public class CondomRequestStore {
    private static CondomRequestStore sCondomRequestStore;
    private ArrayList<CondomRequest> mCondomRequests;

    private static final String TAG = "CondomRequestStore";
    private static final String mAPI = "http://tsb.sccs.swarthmore.edu:8080/api/";

    List<NameValuePair> mParams;

    private CondomRequestStore(String sessionToken) {
        try {
            mParams = new ArrayList<NameValuePair>();
            final ServerRequest serverRequest = new ServerRequest();

            Log.i(TAG, "SessionToken: " + sessionToken);
            mParams.add(new BasicNameValuePair("session_token", sessionToken));
            JSONObject json = serverRequest.getJSON(mAPI + "delivery/request/all", mParams);
            if (json != null) {
                try {
                    // retrieves array of orders and parses it into list of Condom Requests
                    JSONArray jsonArray = json.getJSONArray("orders");
                    mCondomRequests = new ArrayList<CondomRequest>();
                    if(jsonArray!=null) {
                        Log.i(TAG, "Total orders " + jsonArray.length());
                        JSONObject jsonObject;
                        Boolean delivered;
                        CondomRequest cr;
                        for(int i=0; i < jsonArray.length(); i++) {
                            jsonObject = jsonArray.getJSONObject(i);
                            delivered = jsonObject.getBoolean("order_delivered");
                            Log.i(TAG, "order " + i + " delivered: " + delivered);

                            // only add and view undelivered orders
                            if (delivered.equals(false)) {
                                Log.i(TAG, jsonObject.toString());
                                cr = new CondomRequest((jsonObject));
                                mCondomRequests.add(cr);
                            }
                        }
                        Log.i(TAG, mCondomRequests.size() + " total undelivered orders");
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        } catch (Exception e) {
            mCondomRequests = new ArrayList<CondomRequest>();
            Log.e(TAG, "No condom requests to load");
        }
    }


    public static CondomRequestStore get(String sessionToken) {
        if(sCondomRequestStore == null) {
            sCondomRequestStore = new CondomRequestStore(sessionToken);
        }
        return sCondomRequestStore;
    }


    public static CondomRequestStore update(String sessionToken) {
        sCondomRequestStore = new CondomRequestStore(sessionToken);
        return sCondomRequestStore;
    }


    public ArrayList<CondomRequest> getCondomRequests() {
        return mCondomRequests;
    }


    public CondomRequest getCondomRequest(String orderNumber) {
        for(CondomRequest condomRequest : mCondomRequests) {
            if(condomRequest.getOrderNumber().equals(orderNumber)) {
                return condomRequest;
            }
        }
        return null; // no CondomRequest exists with given order number
    }
}
