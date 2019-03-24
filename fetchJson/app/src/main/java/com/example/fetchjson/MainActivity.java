package com.example.fetchjson;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    public  static TextView attended;
    public static TextView total;
    public static EditText input;
    public static Button click;
    static String roll;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        click = (Button) findViewById(R.id.button);
        attended = (TextView) findViewById(R.id.textView);
        input = (EditText)findViewById(R.id.editText);

        click.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                roll = input.getText().toString();
                fetchData process = new fetchData(roll);
                process.execute();
            }
        });

    }
}