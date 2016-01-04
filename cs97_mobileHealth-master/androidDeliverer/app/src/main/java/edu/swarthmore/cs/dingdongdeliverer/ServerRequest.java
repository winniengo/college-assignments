/**
 * Created by wngo1 on 11/23/14.
 */

package edu.swarthmore.cs.dingdongdeliverer;

import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.List;
import java.util.concurrent.ExecutionException;

public class ServerRequest {
    static InputStream mInputStream = null;
    static JSONObject mJsonObject = null;
    static String mJson = "";
    private Context context;

    public ServerRequest() {

    }

    public JSONObject getJSONFromUrl(String url, List<NameValuePair> params) {
        try {
            DefaultHttpClient httpClient = new DefaultHttpClient();
            HttpPost httpPost = new HttpPost(url);
            httpPost.setEntity(new UrlEncodedFormEntity(params));
            HttpResponse httpResponse = httpClient.execute(httpPost);
            HttpEntity httpEntity = httpResponse.getEntity();
            mInputStream = httpEntity.getContent();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (ClientProtocolException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(
                    mInputStream, "iso-8859-1"), 8);
            StringBuilder stringBuilder = new StringBuilder();
            String line;

            while ((line = reader.readLine()) != null) {
                stringBuilder.append(line + "\n");
            }
            mInputStream.close();
            mJson = stringBuilder.toString();
            Log.e("JSON", mJson);
        } catch (Exception e) {
            Log.e("Buffer Error", "Error converting result " + e.toString());
        }
        try {
            mJsonObject = new JSONObject(mJson);
        } catch (JSONException e) {
            Log.e("JSON Parser", "Error parsing data " + e.toString());
        }
        return mJsonObject;
    }

    JSONObject jsonObject;
    public JSONObject getJSON(String url, List<NameValuePair> params) {
        Params param = new Params(url,params);
        Request myTask = new Request();
        try{
            jsonObject= myTask.execute(param).get();
        }catch (InterruptedException e) {
            e.printStackTrace();
        }catch (ExecutionException e){
            e.printStackTrace();
        }
        return jsonObject;
    }

    private static class Params {
        String url;
        List<NameValuePair> params;
        Params(String url, List<NameValuePair> params) {
            this.url = url;
            this.params = params;
        }
    }

    private class Request extends AsyncTask<Params, String, JSONObject> {
        @Override
        protected JSONObject doInBackground(Params... args) {
            ServerRequest request = new ServerRequest();
            JSONObject json = request.getJSONFromUrl(args[0].url,args[0].params);
            return json;
        }
        @Override
        protected void onPostExecute(JSONObject json) {
            super.onPostExecute(json);
        }
    }
}