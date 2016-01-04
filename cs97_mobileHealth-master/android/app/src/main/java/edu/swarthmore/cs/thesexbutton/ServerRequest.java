package edu.swarthmore.cs.thesexbutton;

import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.HttpVersion;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.conn.ClientConnectionManager;
import org.apache.http.conn.scheme.PlainSocketFactory;
import org.apache.http.conn.scheme.Scheme;
import org.apache.http.conn.scheme.SchemeRegistry;
import org.apache.http.conn.ssl.SSLSocketFactory;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.conn.tsccm.ThreadSafeClientConnManager;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpParams;
import org.apache.http.params.HttpProtocolParams;
import org.apache.http.protocol.HTTP;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.List;
import java.util.concurrent.ExecutionException;

//our custom SSL enabled HTTP client
import edu.swarthmore.cs.thesexbutton.tsbHTTPSClient;

public class ServerRequest {
    static InputStream mInputStream = null;
    static JSONObject mJsonObject = null;
    static String mJson = "";
    final Context context;

    public ServerRequest(Context c) {
        this.context = c;
    }
    public JSONObject getJSONFromUrl(String url, List<NameValuePair> params) {
        try {
            DefaultHttpClient httpClient = new tsbHTTPSClient(context);
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
                stringBuilder.append(line).append("\n");
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
            ServerRequest request = new ServerRequest(context);
            return request.getJSONFromUrl(args[0].url,args[0].params);
        }
        @Override
        protected void onPostExecute(JSONObject json) {
            super.onPostExecute(json);
        }
    }

}