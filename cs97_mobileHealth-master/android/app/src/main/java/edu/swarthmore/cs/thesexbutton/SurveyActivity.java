package edu.swarthmore.cs.thesexbutton;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

public class SurveyActivity extends Activity
{
    private JSONObject mSurveyJson;
    // private String mResponse;  // use to debug
    private String mSurveyBody;
    private TextView mTextView;
    private Button mButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_survey);

        try {
            mSurveyJson = new JSONObject(getIntent().getStringExtra("survey"));
        } catch (JSONException e) {
        }

        if(mSurveyJson != null) {
            try {
                mSurveyBody = mSurveyJson.getString("survey_body");
            } catch (JSONException e) {
            }
        }

        mButton = (Button) findViewById(R.id.survey_button);
        mButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Uri uri = Uri.parse(mSurveyBody);
                Intent i = new Intent(Intent.ACTION_VIEW, uri);
                startActivity(i);
            }
        });
    }
}