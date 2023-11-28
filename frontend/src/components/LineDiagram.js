import React from "react";
import {LineChart,LineSeries} from "reaviz"

export default function LineDiagram(props) {
    
    return (
        <div>
            <LineChart
            width={700}
            height={400}
            series={
            <LineSeries
                type="grouped"
                />
            }
            data={props.data}
            />
        </div>
    )
}