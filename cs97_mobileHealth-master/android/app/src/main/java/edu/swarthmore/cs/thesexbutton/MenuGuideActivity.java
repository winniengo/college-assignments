package edu.swarthmore.cs.thesexbutton;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;

public class MenuGuideActivity extends Activity
{
    private static String TAG = "MenuGuideActivity";

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
        setContentView(R.layout.activity_menu_guide);

        Log.i(TAG, "onCreate");
    }
}
