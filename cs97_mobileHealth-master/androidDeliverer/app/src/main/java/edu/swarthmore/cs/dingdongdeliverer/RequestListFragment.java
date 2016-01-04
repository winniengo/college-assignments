package edu.swarthmore.cs.dingdongdeliverer;

import android.app.ListFragment;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.CheckBox;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;

/**
 * Created by wngo1 on 12/2/14.
 */
public class RequestListFragment extends ListFragment{ // displays all condom requests
    String mSessionToken;
    ArrayList<CondomRequest> mCondomRequests;
    CondomRequestAdapter mCondomRequestAdapter;
    private static final String TAG = "RequestListFragment";

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Log.i(TAG, "created");

        Bundle bundle = getArguments();
        mSessionToken = bundle.getString("session_token", null);

        // POST delivery/requests/all
        CondomRequestStore store = CondomRequestStore.get(mSessionToken);
        mCondomRequests = store.getCondomRequests();

        Log.i(TAG, "Got list of condom requests");

        mCondomRequestAdapter = new CondomRequestAdapter(mCondomRequests);
        setListAdapter(mCondomRequestAdapter);
    }

    @Override
    public void onResume() {
        super.onResume();

        CondomRequestStore store = CondomRequestStore.update(mSessionToken);
        mCondomRequests = store.getCondomRequests();

        Log.i(TAG, "Got updated list of condom requests " + mCondomRequests.size());

        mCondomRequestAdapter = new CondomRequestAdapter(mCondomRequests);
        setListAdapter(mCondomRequestAdapter);
    }

    @Override
    public void onListItemClick(ListView l, View v, int pos, long id) {
        CondomRequestAdapter adapter = (CondomRequestAdapter)getListAdapter();
        CondomRequest cr = adapter.getItem(pos);
        Log.d(TAG, cr.getOrderNumber() + "was clicked");

        // start an instance of CondomRequest Activity
        Intent i = new Intent(getActivity(), RequestActivity.class);
        i.putExtra("order_number", cr.getOrderNumber());
        i.putExtra("session_token", mSessionToken);
        startActivity(i);
    }

    // Condom Request Adapter
    private class CondomRequestAdapter extends ArrayAdapter<CondomRequest> {
        public CondomRequestAdapter(ArrayList<CondomRequest> condomRequests) {
            super(getActivity(), 0, condomRequests);
            Log.i(TAG, "Create CondomRequestAdapter " + condomRequests.size());
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            // check to see if a recycled view was passed in, if not inflate one
            if (convertView == null) {
                convertView = getActivity().getLayoutInflater()
                        .inflate(R.layout.fragment_request_list, null);
            }
            Log.i(TAG, "Adapter getView " + position);
            CondomRequest cr = getItem(position); // get CondomRequest for current view

            // fill view with condom request details
            TextView orderNumber, dateRequested, destination;
            CheckBox accepted, delivered, failed;

            orderNumber = (TextView)convertView.findViewById(R.id.requestListOrderNumber);
            dateRequested = (TextView)convertView.findViewById(R.id.requestListDateRequested);
            destination = (TextView)convertView.findViewById(R.id.requestListDestination);
            accepted = (CheckBox)convertView.findViewById(R.id.requestListAccepted);
            delivered = (CheckBox)convertView.findViewById(R.id.requestListDelivered);
            failed = (CheckBox)convertView.findViewById(R.id.requestListFailed);

            orderNumber.setText(cr.getOrderNumber());
            dateRequested.setText(cr.getDateRequested().toString());
            destination.setText(cr.getDeliveryDestination());
            accepted.setChecked(cr.isOrderAccepted());
            delivered.setChecked(cr.isOrderDelivered());
            failed.setChecked(cr.isOrderFailed());

            return convertView; // return the view object
        }
    }
}
