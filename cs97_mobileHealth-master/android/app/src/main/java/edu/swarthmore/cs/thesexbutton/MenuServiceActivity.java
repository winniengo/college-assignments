package edu.swarthmore.cs.thesexbutton;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;

public class MenuServiceActivity extends Activity
{
    private static String TAG = "MenuServiceActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu_service);
        Log.i(TAG, "onCreate");
    }

}
