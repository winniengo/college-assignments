package edu.swarthmore.cs.dingdongdeliverer;

import android.app.Application;

/**
 * Created by dfeista1 on 12/7/14.
 */
public class Globals extends Application {

    private String api_path = "http://tsb.sccs.swarthmore.edu:8080/api/";

    public String getApiPath () {
        return this.api_path;
    }

}
