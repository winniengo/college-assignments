package edu.swarthmore.cs.thesexbutton;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class DeliveryCompleteActivity extends Activity {
    String mSessionToken, mOrderNumber;
    SharedPreferences mSharedPreferences;

    /**
     * Disable back button
     */
    @Override
    public void onBackPressed() {
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        setContentView(R.layout.delivery_arrival);
        super.onCreate(savedInstanceState);

        mSharedPreferences = getSharedPreferences("SharedPreferences", MODE_PRIVATE);
        mSessionToken = mSharedPreferences.getString("session_token", null);
        mOrderNumber = mSharedPreferences.getString("order_number", null);

        TextView orderNum = (TextView) findViewById(R.id.text_order_number_arrival);
        orderNum.setText("Order " + mOrderNumber);

        Button guide = (Button) findViewById(R.id.guideButton);
        guide.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent i = new Intent(DeliveryCompleteActivity.this, MenuGuideActivity.class);
                startActivity(i);
                finish();
            }
        });
    }
}
