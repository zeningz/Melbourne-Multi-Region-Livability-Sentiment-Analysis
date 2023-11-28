import React from "react";
import {BarChart} from "reaviz"



export default function BarDiagram(props){
    return (
        <BarChart
            width={700}
            height={400}
            data={props.data}
            margins={22.25}
        />
    )
}