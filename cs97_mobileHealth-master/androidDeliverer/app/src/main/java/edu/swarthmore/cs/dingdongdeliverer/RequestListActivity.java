package edu.swarthmore.cs.dingdongdeliverer;

import android.app.Activity;
import android.app.Fragment;
import android.app.FragmentManager;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;

/**
 * Created by wngo1 on 12/2/14.
 */
public class RequestListActivity extends Activity {
    SharedPreferences mSharedPreferences;
    String mSessionToken = null;

    String mApiPath = "http://tsb.sccs.swarthmore.edu:8080/api/";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_fragment);

        Log.i("FUCK", "RequestListActivity start");

        mSharedPreferences = getSharedPreferences("SharedPreferences", MODE_PRIVATE);
        mSessionToken = mSharedPreferences.getString("session_token", null);

        if(mSessionToken==null) {
            //List<NameValuePair> params = new ArrayList<NameValuePair>();
            mSessionToken = "186086b4eebcb65236aa5e7519cd19376eeec17bb9348967d52da094f140bbec10b024f136ab9f771408a8b5fbb0313f012ac8cf16e2a6ec0a4eeb50fe02ec8c9b734d03dce598ceec6d0a75f214d5403ff25074aab3da95f8095c5d9c3e38f2ad1ab0e4a07113197e21afe26e1c8cd54a342fa9168c1868b91363cb00885a0c";
            Log.i("RequestListActivity", "Fell back to hardcoded mSessionToken");
            //TODO: login as deliverer, obtain valid session token
        }

//        // set the refresh thing
//        final SwipeRefreshLayout swipeLayout = (SwipeRefreshLayout) findViewById(R.id.swipe_container);
//        swipeLayout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
//            @Override
//            public void onRefresh() {
//                new Handler().postDelayed(new Runnable() {
//                    @Override
//                    public void run() {
//                        CondomRequestStore store = CondomRequestStore.update(mSessionToken);
//                        swipeLayout.setRefreshing(false);
//                    }
//                }, 1000);
//            }
//        });
//        swipeLayout.setColorScheme(android.R.color.holo_blue_bright,
//                android.R.color.holo_green_light,
//                android.R.color.holo_orange_light,
//                android.R.color.holo_red_light);

        FragmentManager fm = getFragmentManager();
        Fragment fragment = fm.findFragmentById(R.id.fragmentContainer);

        if(fragment == null) {
            fragment = new RequestListFragment();
            Bundle args = new Bundle();
            args.putString("session_token", mSessionToken);
            fragment.setArguments(args);

            fm.beginTransaction().add(R.id.fragmentContainer, fragment).commit();
        }

    }
}
