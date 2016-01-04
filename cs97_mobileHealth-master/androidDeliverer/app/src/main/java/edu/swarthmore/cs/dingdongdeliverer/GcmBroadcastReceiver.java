package edu.swarthmore.cs.dingdongdeliverer;

import android.app.Activity;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.support.v4.content.WakefulBroadcastReceiver;
import android.util.Log;

/**
 * This WakefulBroadcastReceiver creates and manages a partial wake lock. It passes the work of
 * processing the GCM message to an IntentService, while ensuring that the device does not go back
 * to sleep in the transition. The IntentService calls GcmBroadcastReceiver.completeWakefulIntent()
 * when it is ready to release the wake lock.
 */

public class GcmBroadcastReceiver extends WakefulBroadcastReceiver
{
    @Override
    public void onReceive(Context context, Intent intent)
    {
        // Specify that GcmIntentService will handle the intent
        ComponentName comp =
                new ComponentName(context.getPackageName(), GcmIntentService.class.getName());

        Log.d("Broadcast received:", "GCM msg");

        startWakefulService(context, (intent.setComponent(comp)));
        setResultCode(Activity.RESULT_OK);
    }
}